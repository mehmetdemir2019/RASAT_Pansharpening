RASAT Pansharpening

📌 Proje Tanıtımı

Bu proje, RASAT uydusundan elde edilen L1 seviyesindeki görüntüler için Pansharpening yöntemlerini kullanarak görüntü iyileştirme yapmayı amaçlamaktadır. Projede Brovey Transform yöntemi kullanılarak görüntülerin uzamsal çözünürlüğü artırılmıştır.

🔍 Kullanılan Yöntemler

Brovey Transform yöntemi kullanılarak multispektral (MS) ve pankromatik (PAN) görüntüler birleştirilmiştir.

Faz Korelasyonu (Phase Correlation) ile kayma düzeltmesi yapılmıştır.

Min-Max Normalizasyon ve Histogram Kırpma ile kontrast ve renk iyileştirmesi sağlanmıştır.

💻 Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki yazılımlar ve kütüphaneler gereklidir:

1️⃣ Yazılım Gereksinimleri:

Python 3.8+

Git

Visual Studio Code veya Jupyter Notebook (Opsiyonel)

2️⃣ Python Kütüphaneleri:

Aşağıdaki komut ile bağımlılıkları yükleyebilirsiniz:

pip install numpy rasterio matplotlib opencv-python scikit-image

🚀 Kurulum Adımları

1️⃣ Projeyi Klonla

Aşağıdaki komutla projeyi bilgisayarına klonla:

git clone https://github.com/mehmetdemir2019/RASAT_Pansharpening.git
cd RASAT_Pansharpening

2️⃣ Python Ortamını Kur

Sanallaştırılmış bir Python ortamı oluştur ve etkinleştir:

python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate    # Windows

Bağımlılıkları yükle:

pip install -r requirements.txt

3️⃣ Kodları Çalıştır

Proje içindeki pansharpen.py dosyasını çalıştır:

python pansharpen.py

Çalıştırıldığında Brovey Transform uygulanmış RGB görüntü oluşturulacak ve brovey_rgb.tif adıyla kaydedilecektir.

📊 Çıktı Örnekleri

Aşağıda projeden elde edilen örnek çıktılar yer almaktadır:

🔹 Kaynak Görseller

PAN Görüntüsü: Yüksek çözünürlüklü gri tonlamalı görüntü.

MS Görüntüleri: Kırmızı, Yeşil ve Mavi bantları içeren görüntüler.
📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına göz atabilirsiniz.

🔗 Kaynakça

Teke, M. ve diğ., "Uzaktan Algılama ve Pansharpening Yöntemleri," Türkiye Uzay Ajansı Raporu, 2021.

Pohl, C., & Genderen, J. L. V. (1998). "Review article: Multisensor image fusion in remote sensing: Concepts, methods and applications." International Journal of Remote Sensing.

Liu, Y., Yuan, X., Tang, P., & Liu, Y. (2020). "Pan-Sharpening With Color-Aware Perceptual Loss And Guided Re-Colorization," IEEE IGARSS 2020.