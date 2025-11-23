# 🏫 Automated Class Distributor Tool

Bu proje, ilkokul yönetimlerinin her yıl karşılaştığı karmaşık sınıf oluşturma sürecini otomatize etmek için geliştirilmiş bir **Python** masaüstü uygulamasıdır. Gerçek bir okul yöneticisinin (Müdür Yardımcısı) ihtiyaçları doğrultusunda tasarlanmış ve aktif olarak kullanılmıştır.

![GUI Screenshot](GUI.png)
*Programın kullanıcı dostu arayüzü.*

## 🎯 Problem
Okul yönetimleri, yüzlerce öğrenciyi sınıflara dağıtırken "homojenlik" sağlamak zorundadır. Manuel yapılan dağıtımlarda şunları dengelemek günler sürer:
* **Cinsiyet Dengesi:** Her sınıfta eşit sayıda kız/erkek öğrenci olması.
* **Akademik Başarı:** Not ortalamalarının sınıflar arasında adil dağılması.
* **Yabancı Uyruklu Öğrenci Dengesi:** Kaynaştırma ve yabancı öğrencilerin tek bir sınıfta toplanmaması.

## 💡 Çözüm ve Özellikler
Geliştirilen bu yazılım, Excel verilerini işleyerek saniyeler içinde optimize edilmiş sınıflar oluşturur.

* **📊 Akıllı Dağıtım Algoritması:** Öğrencileri başarı puanlarına göre sıralar ve "S-Dağılımı" (Snake Distribution) mantığıyla sınıflara yerleştirerek akademik dengeyi sağlar.
* **⚖️ Kota Kontrolü:** Kız/Erkek ve özel durumlu öğrenci sayılarını her sınıf için eşitler.
* **🖥️ Kolay Arayüz (GUI):** Kod bilmeyen bir kullanıcının (okul yöneticisinin) rahatça kullanabilmesi için `Tkinter` ile basit bir arayüz tasarlanmıştır.
* **files Excel Entegrasyonu:** `Pandas` kütüphanesi kullanılarak `.xlsx` dosyaları okunur ve sonuçlar yine Excel formatında raporlanır.

## 📸 Sonuçlar ve Analiz
Program çalıştırıldıktan sonra oluşturulan sınıfların dağılım grafiği aşağıdadır. Görüldüğü üzere öğrenci sayıları ve başarı ortalamaları sınıflar arasında dengelenmiştir.

![Student Distribution Graph](Student_distribution.png)
*Otomatik oluşturulan sınıfların öğrenci dağılım analizi.*

## 🛠️ Kullanılan Teknolojiler
* **Dil:** Python 3.x
* **Veri İşleme:** Pandas, Openpyxl
* **Arayüz:** Tkinter
* **Test Verisi:** Faker (Algoritma testi için binlerce satırlık sahte veri üretimi)

## 🚀 Kurulum ve Kullanım

1.  Repoyu klonlayın:
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/School-Class-Distributor.git](https://github.com/KULLANICI_ADIN/School-Class-Distributor.git)
    ```
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı başlatın:
    ```bash
    python class_distributor_gui.py
    ```
4.  Açılan pencereden öğrenci listesinin bulunduğu Excel dosyasını seçin ve **"Sınıfları Oluştur"** butonuna basın.

---
**Geliştirici Notu:** Bu proje, annemin (Okul Müdür Yardımcısı) iş yükünü azaltmak amacıyla geliştirilmiş, gerçek bir problemi çözen mühendislik uygulamasıdır.
