import os
import rasterio
import numpy as np
import cv2
import matplotlib.pyplot as plt
from rasterio.warp import reproject, Resampling
from skimage.registration import phase_cross_correlation

############################
# 1) Yardımcı Fonksiyonlar
############################

def read_band(folder):
    """ Belirtilen klasördeki image.tif dosyasını okur. """
    path = os.path.join(folder, "image.tif")
    with rasterio.open(path) as src:
        data = src.read(1).astype(np.float32)
        profile = src.profile
    return data, profile

def min_max_normalize(arr):
    """ Min-Max Normalizasyonu: 0-1 aralığına çeker. """
    min_val = arr.min()
    max_val = arr.max()
    if max_val - min_val < 1e-6:
        return np.zeros_like(arr, dtype=np.float32)
    return (arr - min_val) / (max_val - min_val + 1e-6)

def apply_histogram_equalization(image):
    """ CLAHE ile Kontrast Artırma. """
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    return clahe.apply(image)

def co_register_in_memory(ref_profile, tgt_data, tgt_profile):
    """ Multispektral görüntüleri Pankromatik görüntü boyutuna getirir. """
    out_arr = np.zeros((ref_profile['height'], ref_profile['width']), dtype=np.float32)
    reproject(
        source=tgt_data,
        destination=out_arr,
        src_transform=tgt_profile['transform'],
        src_crs=tgt_profile['crs'],
        dst_transform=ref_profile['transform'],
        dst_crs=ref_profile['crs'],
        resampling=Resampling.cubic  # Daha iyi interpolasyon
    )
    return out_arr

def refine_registration(ref_img, tgt_img):
    """ Faz korelasyonu ile ince kayma düzeltmesi. """
    shift, error, diffphase = phase_cross_correlation(ref_img, tgt_img, upsample_factor=10)
    print("Calculated shift (y, x):", shift)
    rows, cols = tgt_img.shape
    M = np.float32([[1, 0, shift[1]], [0, 1, shift[0]]])
    corrected = cv2.warpAffine(tgt_img, M, (cols, rows), flags=cv2.INTER_CUBIC)  # Daha iyi interpolasyon
    return corrected

def brovey_transform(ms_bands, pan, bands_factor=3):
    """ Brovey yöntemi: MS_i' = MS_i * (bands_factor * PAN / (R+G+B)) """
    sum_ms = np.sum(ms_bands, axis=0)
    mask = sum_ms < 1e-6
    sum_ms[mask] = 1e-6  # Sıfıra bölmeyi önlemek için
    sharpened = ms_bands * (bands_factor * pan / sum_ms)
    sharpened[:, mask] = 0.0
    return sharpened

def save_rgb_tif(rgb_array, output_path, profile):
    """ RGB dizisini GeoTIFF olarak kaydeder. """
    profile.update({
        'count': 3,
        'dtype': 'uint8',
        'height': rgb_array.shape[0],
        'width': rgb_array.shape[1]
    })
    
    with rasterio.open(output_path, 'w', **profile) as dst:
        for i in range(3):  # R, G, B kanalları
            dst.write(rgb_array[:, :, i], i + 1)

############################
# 2) Ana İşlem Fonksiyonu
############################

def main():
    base_dir = r"C:\Tubitak\RST_20200915_e74_2_L1"

    # Klasör yolları:
    pan_folder = os.path.join(base_dir, "0")
    band1_folder = os.path.join(base_dir, "1")
    band2_folder = os.path.join(base_dir, "2")
    band3_folder = os.path.join(base_dir, "3")

    # 1) **Veri Okuma**
    pan, pan_profile = read_band(pan_folder)
    ms1, ms1_profile = read_band(band1_folder)
    ms2, ms2_profile = read_band(band2_folder)
    ms3, ms3_profile = read_band(band3_folder)

    # **Çözünürlük farkı giderme: MS bantlarını PAN boyutuna getiriyoruz!**
    ms1_resized = co_register_in_memory(pan_profile, ms1, ms1_profile)
    ms2_resized = co_register_in_memory(pan_profile, ms2, ms2_profile)
    ms3_resized = co_register_in_memory(pan_profile, ms3, ms3_profile)

    # **Faz korelasyonu ile kayma düzeltme**
    ms1_refined = refine_registration(pan, ms1_resized)
    ms2_refined = refine_registration(pan, ms2_resized)
    ms3_refined = refine_registration(pan, ms3_resized)

    # 2) **Normalizasyon**
    pan_norm = min_max_normalize(pan)
    ms1_norm = min_max_normalize(ms1_refined)
    ms2_norm = min_max_normalize(ms2_refined)
    ms3_norm = min_max_normalize(ms3_refined)

    # 3) **Brovey Transform**
    ms_bands = np.stack([ms1_norm, ms2_norm, ms3_norm], axis=0)
    sharpened = brovey_transform(ms_bands, pan_norm, bands_factor=3)

    # 4) **RGB Görselleştirme ve Kaydetme**
    sharpened_vis = []
    for i in range(sharpened.shape[0]):
        band = min_max_normalize(sharpened[i])  # Normalize et
        vis = (band * 255).astype(np.uint8)
        vis = apply_histogram_equalization(vis)  # Histogram dengeleme ekle
        sharpened_vis.append(vis)

    sharpened_vis = np.array(sharpened_vis)
    rgb_image = np.dstack((sharpened_vis[0], sharpened_vis[1], sharpened_vis[2]))

    # 5) **Matplotlib ile Görselleştirme**
    plt.figure(figsize=(8,8))
    plt.imshow(rgb_image)
    plt.title("Brovey Transform Result (RGB) - with Phase Correction & Histogram Equalization")
    plt.axis('off')
    plt.show()

    # 6) **RGB TIFF olarak kaydetme**
    out_rgb_path = os.path.join(base_dir, "brovey_rgb.tif")
    save_rgb_tif(rgb_image, out_rgb_path, pan_profile)
    print(f"✅ **Düzeltilmiş RGB TIFF dosyası kaydedildi:** {out_rgb_path}")

if __name__ == "__main__":
    main()
