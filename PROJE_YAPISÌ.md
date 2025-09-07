# 📁 AzGelir Proje Klasör Yapısı

## 🏗️ Ana Proje Dosyaları
```
/AzGelir/
├── main.py                  # Ana uygulama kodu
├── logo.png                 # Uygulama logosu
├── records.db               # Veritabanı dosyası
├── requirements.txt         # Python bağımlılıkları
├── README.md               # Ana dokümantasyon
├── .gitattributes          # Git yapılandırması
└── AzGelir_Setup.exe       # Sıfırdan kurulum dosyası (53 MB)
```

## 📂 Klasör Açıklamaları

### 🔨 `/build_scripts/` - Derleme Araçları
- **Tüm platform derleyicileri** 
- **Kurulum dosyası oluşturucuları**
- **Otomatik build scriptleri**

**Dosyalar:**
```
build_linux.py              # Linux için PyInstaller
build_windows.py             # Windows için PyInstaller
build_appimage.py           # Linux AppImage
build_snap.py               # Ubuntu Snap paketi
build_msi.py                # Windows MSI kurulum
build_all_linux.py          # Tüm Linux formatları
build_all_windows.py        # Tüm Windows formatları
create_simple_setup.py      # Ana kurulum exe oluşturucu
create_ultimate_installer.py # Gelişmiş kurulum sistemi
create_full_installer.py    # Tam özellikli kurulum
create_single_exe_installer.bat # Batch kurulum oluşturucu
```

### 🚀 `/installers/` - Kurulum Dosyaları
- **Platform özel kurucular**
- **Otomatik kurulum scriptleri**
- **Paket yöneticisi dosyaları**

**Dosyalar:**
```
setup_linux.sh             # Linux otomatik kurulum
setup_windows.bat          # Windows otomatik kurulum
install_linux.sh           # Linux manuel kurulum
installer.nsi               # NSIS Windows installer
snapcraft.yaml             # Snap paketi manifest
```

### 📊 `/dist/` - Derlenen Dosyalar
- **PyInstaller çıktıları**
- **Platform özel executable'lar**
- **Dağıtım için hazır dosyalar**

**İçerik:**
```
AzGelir.exe                 # Windows ana uygulama
AzGelir_Baslat.bat         # Windows portable başlatıcı
install.ps1                # PowerShell kurulum
README_Windows.md          # Windows kullanım kılavuzu
LICENSE.txt                # Lisans dosyası
```

### 🛠️ `/tools/` - Yardımcı Araçlar
- **Proje yönetim araçları**
- **Test ve dağıtım utilities**
- **Kullanıcı araçları**

**Planlanan dosyalar:**
```
kurulum_yoneticisi.bat     # Kurulum test ve yönetim
basla.bat                  # Hızlı başlatıcı
update_checker.py          # Güncelleme kontrolü
project_manager.py         # Proje yöneticisi
```

### 📚 `/docs/` - Dokümantasyon
- **Kullanım kılavuzları**
- **Teknik dokümantasyon**
- **Kurulum rehberleri**

**Planlanan dosyalar:**
```
KURULUM_KILAVUZU.md        # Kapsamlı kurulum rehberi
KURULUM_SISTEMI_README.md  # Sıfırdan kurulum kılavuzu
KURULUM_SONUÇ_RAPORU.md    # Tamamlanan özellikler
README_Windows.md          # Windows özel dokümantasyon
LICENSE.txt                # Proje lisansı
API_DOCUMENTATION.md       # Geliştirici dokümantasyonu
USER_MANUAL.md             # Kullanıcı kılavuzu
TROUBLESHOOTING.md         # Sorun giderme rehberi
```

## 🎯 Kullanım Rehberi

### 👤 Son Kullanıcı İçin
```bash
# Tek tık kurulum
AzGelir_Setup.exe          # Sağ tık → Yönetici olarak çalıştır

# Platform özel kurulum
./installers/setup_linux.sh    # Linux
./installers/setup_windows.bat # Windows
```

### 👨‍💻 Geliştirici İçin
```bash
# Ana uygulamayı çalıştır
python main.py

# Platform için derle
python build_scripts/build_windows.py  # Windows
python build_scripts/build_linux.py    # Linux

# Kurulum dosyası oluştur
python build_scripts/create_simple_setup.py

# Tüm formatları derle
python build_scripts/build_all_windows.py
python build_scripts/build_all_linux.py
```

### 🧪 Test ve Geliştirme
```bash
# Kurulum test et
./tools/kurulum_yoneticisi.bat

# Hızlı başlat
./tools/basla.bat

# Dağıtım paketi oluştur
python build_scripts/create_distribution.py
```

## 📋 Dosya Boyutları ve Türleri

### 🔢 Ana Dosyalar
- **main.py:** 29 KB (Ana uygulama kodu)
- **logo.png:** 1.4 MB (Yüksek kalite logo)
- **records.db:** 12 KB (Veritabanı)
- **AzGelir_Setup.exe:** 53.1 MB (Tam kurulum)

### 📦 Derlenen Dosyalar
- **dist/AzGelir.exe:** 38.3 MB (Windows executable)
- **Linux builds:** 35-45 MB (çeşitli formatlar)

### 🔧 Build Scripts
- **Toplam:** ~150 KB (11 script dosyası)
- **En büyük:** create_full_installer.py (41 KB)

## 🎮 Hızlı Komutlar

### 🚀 En Hızlı Başlangıç
```bash
# Uygulamayı çalıştır
python main.py

# Kurulum exe'si oluştur
python build_scripts/create_simple_setup.py

# Dağıtım için hazırla
./tools/kurulum_yoneticisi.bat
```

### 🔄 Güncelleme Süreci
```bash
# 1. Kodu güncelle
git pull origin main

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Test et
python main.py

# 4. Derle ve dağıt
python build_scripts/build_all_windows.py
```

## 📞 Destek ve Geliştirme

### 🐛 Hata Raporlama
- **Ana uygulama hataları:** main.py logs
- **Kurulum sorunları:** setup logs
- **Build hataları:** build_scripts/ logs

### 🔧 Geliştirme Ortamı
- **Python 3.8+** gerekli
- **PyQt5** GUI framework
- **PyInstaller** derleme için
- **Windows 10+** test için

---

**🎉 Düzenli ve profesyonel proje yapısı hazır!**
