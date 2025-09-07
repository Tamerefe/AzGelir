# AzGelir Sıfırdan Kurulum Sistemi

Bu proje, AzGelir uygulamasını sıfırdan bilgisayarlarda kurabilmek için tam otomatik kurulum dosyaları sağlar.

## 🎯 Özellikler

### ✅ Tam Otomatik Kurulum
- **Python 3.11** otomatik kurulumu (embedded sürüm)
- **Visual C++ Redistributable** kontrolü ve kurulumu
- **PyQt5** ve gerekli kütüphaneler otomatik kurulumu
- **AzGelir** ana uygulaması kurulumu
- **Masaüstü ve Başlat menüsü** kısayolları
- **Sistem kayıtları** ve kaldırıcı oluşturma

### 🚀 Tek Dosya Çözüm
- **53 MB** boyutunda tek exe dosyası
- **Bağımsız çalışır** - hiçbir ek dosya gerektirmez
- **Grafik arayüzlü** kurulum sihirbazı
- **Yönetici yetkisi** kontrolü
- **Sistem uyumluluğu** kontrolü (64-bit Windows)

## 📁 Oluşturulan Dosyalar

### Ana Kurulum Dosyası
- **`AzGelir_Setup.exe`** (53.1 MB)
  - Sıfırdan bilgisayar kurulumu
  - Python dahil her şey gömülü
  - Grafik kurulum sihirbazı

### Oluşturucu Araçlar
- **`create_simple_setup.py`** - Ana kurulum exe oluşturucu
- **`create_ultimate_installer.py`** - Gelişmiş kurulum sistemi
- **`create_single_exe_installer.bat`** - Batch kurulum oluşturucu
- **`create_full_installer.py`** - Tam özellikli kurulum sistemi

## 💻 Sistem Gereksinimleri

### Hedef Sistem (Kurulacak Bilgisayar)
- **Windows 7/8/10/11** (64-bit)
- **2 GB RAM** (minimum)
- **500 MB** boş disk alanı
- **İnternet bağlantısı** (Python paketleri için)
- **Yönetici yetkisi** (kurulum için)

### Geliştirme Sistemi
- **Python 3.8+**
- **PyInstaller**
- **tkinter** (GUI için)
- **win32com.client** (kısayollar için)

## 🔧 Kurulum Dosyası Oluşturma

### Hızlı Yöntem
```batch
# Batch script ile
.\create_single_exe_installer.bat

# Veya Python ile
python create_simple_setup.py
```

### Manuel Adımlar
1. **Ana uygulamayı derle:**
   ```bash
   python build_windows.py
   ```

2. **Kurulum exe'si oluştur:**
   ```bash
   python create_simple_setup.py
   ```

## 🚀 Kullanım

### Kurulum Dosyasını Çalıştırma
1. **`AzGelir_Setup.exe`** dosyasını hedef bilgisayara kopyalayın
2. **Sağ tık** → **"Yönetici olarak çalıştır"**
3. **Kurulum sihirbazını** takip edin
4. **5-10 dakika** bekleyin (internet hızına göre)
5. **AzGelir** masaüstü kısayolundan çalıştırın

### Kurulum Aşamaları
1. **Sistem kontrolü** (Windows 64-bit)
2. **Kurulum dizini** hazırlama
3. **Python kontrolü** ve kurulumu
4. **VC++ Redistributable** kontrolü
5. **AzGelir dosyaları** kopyalama
6. **Python paketleri** kurulumu
7. **Kısayollar** oluşturma
8. **Sistem kayıtları** oluşturma

## 📋 Teknik Detaylar

### Kurulum İçeriği
```
C:\Program Files\AzGelir\
├── AzGelir.exe          # Ana uygulama
├── Python\              # Gömülü Python 3.11
│   ├── python.exe
│   ├── Scripts\
│   └── Lib\
└── logo.png             # Uygulama logosu
```

### Registry Kayıtları
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir
├── DisplayName: "AzGelir"
├── DisplayVersion: "1.0.0"
├── Publisher: "Tamerefe"
├── InstallLocation: "C:\Program Files\AzGelir"
└── UninstallString: ...
```

### Kısayollar
- **Masaüstü:** `%USERPROFILE%\Desktop\AzGelir.lnk`
- **Başlat Menüsü:** `%ProgramData%\Microsoft\Windows\Start Menu\Programs\AzGelir\`

## 🛠️ Geliştirici Notları

### Python Paketleri
- **PyQt5==5.15.9** - GUI framework
- **pywin32** - Windows API erişimi
- **base64** - Dosya gömme için
- **tkinter** - Kurulum GUI'si
- **urllib.request** - Dosya indirme
- **zipfile** - Arşiv işlemleri

### Güvenlik
- **Yönetici yetkisi** kontrolü
- **Sistem uyumluluğu** kontrolü
- **Hata yakalama** ve kullanıcı bilgilendirme
- **Temizlik** işlemleri (geçici dosyalar)

### Optimizasyonlar
- **Gömülü dosyalar** - Bağımlılık azaltma
- **Tek exe dosyası** - Dağıtım kolaylığı
- **Progress bar** - Kullanıcı deneyimi
- **Otomatik kurulum** - El değmeden kurulum

## 🎯 Kullanım Senaryoları

### Bireysel Kullanıcı
- **Teknik bilgi gerektirmez**
- **Çift tık ile kurulum**
- **Otomatik güncelleme** (gelecekte)

### Kurumsal Dağıtım
- **Sessiz kurulum** seçeneği
- **Toplu dağıtım** uyumluluğu
- **Registry tabanlı** yönetim

### Geliştirici Testi
- **Hızlı test ortamı** kurulumu
- **Temiz sistem** simülasyonu
- **Bağımlılık testi**

## 📞 Destek

### Kurulum Sorunları
1. **Yönetici yetkisi** var mı?
2. **İnternet bağlantısı** aktif mi?
3. **Antivürüs** engelliyor mu?
4. **64-bit Windows** sistemi mi?

### Hata Raporlama
- **Hata ekranı** screenshot'ı
- **Windows versiyonu**
- **Kurulum dizini**
- **İnternet hızı**

## 📜 Lisans

Bu kurulum sistemi MIT lisansı altında dağıtılmaktadır.

---

**🎉 AzGelir - Artık her bilgisayarda çalışır!**
