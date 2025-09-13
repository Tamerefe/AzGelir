# AzGelir - Proje Yapısı

## 📁 Klasör Organizasyonu

```
AzGelir/
├── 📄 main.py                 # Ana uygulama kodu
├── 📄 requirements.txt        # Python bağımlılıkları
├── 📄 README.md              # Proje ana dökümanı
├── 📄 records.db             # SQLite veritabanı
├── 🖼️ logo.png               # Uygulama ikonu
├── 📄 .gitattributes         # Git yapılandırması
│
├── 📁 releases/              # 🆕 Dağıtım Dosyaları
│   ├── 📄 README.md         # Platform seçim rehberi
│   ├── 📁 windows/          # Windows dağıtımı
│   │   ├── 📄 AzGelir.exe           # Windows executable (38.5 MB)
│   │   ├── 📄 AzGelir_Portable.zip  # Portable paket (39.6 MB)
│   │   ├── 📁 AzGelir_Portable/     # Portable klasör
│   │   ├── 📄 install.ps1           # PowerShell kurulum
│   │   ├── 📄 installer.nsi         # NSIS installer script
│   │   ├── 📁 chocolatey/           # Chocolatey paketi
│   │   ├── 📄 LICENSE.txt           # Lisans dosyası
│   │   └── 📄 README.md            # Windows kurulum rehberi
│   │
│   └── 📁 linux/            # Linux dağıtımı
│       ├── 📁 AzGelir/              # Linux binary klasörü (1.6 MB)
│       ├── 📄 install.sh            # Otomatik kurulum scripti
│       ├── 📄 uninstall.sh          # Kaldırma scripti
│       ├── 📄 AzGelir.desktop       # Desktop entry
│       ├── 📄 io.github.tamerefe.AzGelir.json     # Flatpak manifest
│       ├── 📄 io.github.tamerefe.AzGelir.desktop  # Flatpak desktop
│       ├── 📄 io.github.tamerefe.AzGelir.metainfo.xml # App metadata
│       ├── 📁 AzGelir.AppDir/       # AppImage yapı klasörü
│       └── 📄 README.md            # Linux kurulum rehberi
│
├── 📁 build_scripts/        # Paketleme Scriptleri
│   ├── 📄 build_windows.py         # Windows PyInstaller build
│   ├── 📄 build_linux.py           # Linux PyInstaller build
│   ├── 📄 build_all_windows.py     # Windows toplu build
│   ├── 📄 build_all_linux.py       # Linux toplu build
│   ├── 📄 build_msi.py             # MSI installer
│   ├── 📄 build_appimage.py        # AppImage builder
│   ├── 📄 build_snap.py            # Snap package builder
│   ├── 📄 create_full_installer.py # Gelişmiş installer
│   ├── 📄 create_simple_setup.py   # Basit setup
│   ├── 📄 create_single_exe_installer.bat # Tek dosya installer
│   ├── 📄 create_ultimate_installer.py    # Ultimate installer
│   └── 📄 README.md                # Build script rehberi
│
├── 📁 docs/                 # Dokümantasyon
│   ├── 📄 KURULUM_KILAVUZU.md      # Detaylı kurulum rehberi
│   ├── 📄 KURULUM_SISTEMI_README.md # Kurulum sistemi detayları
│   ├── 📄 KURULUM_SONUÇ_RAPORU.md  # Test raporları
│   ├── 📄 LICENSE.txt              # Lisans detayları
│   └── 📄 README_Windows.md        # Windows spesifik notlar
│
└── 📁 installers/          # Kurulum Scriptleri (Kaynak)
    ├── 📄 install_linux.sh         # Linux manuel kurulum
    ├── 📄 installer.nsi            # NSIS template
    ├── 📄 setup_linux.sh           # Linux otomatik setup
    ├── 📄 setup_windows.bat        # Windows otomatik setup
    ├── 📄 snapcraft.yaml           # Snap paketi tanımı
    └── 📄 README.md                # Installer rehberi
```

## 🎯 Yeni Organizasyon Mantığı

### 🔄 Ana Değişiklikler

1. **📁 releases/ Klasörü Eklendi**
   - Tüm kullanıma hazır dosyalar burda
   - Platform bazlı ayrım (windows/, linux/)
   - Her platform için ayrı README

2. **🧹 Ana Dizin Temizlendi**
   - Sadece kaynak kod ve geliştirme dosyaları
   - Build artefaktları releases/ klasörüne taşındı
   - Daha temiz repository görünümü

3. **📋 Gelişmiş Dokümantasyon**
   - Platform spesifik README'ler
   - Net kurulum talimatları
   - Kullanıcı dostu yönlendirmeler

## 📦 Platform Dosya Dağılımı

### Windows (`releases/windows/`)
- **Ana Dosya**: `AzGelir.exe` (38.5 MB standalone)
- **Portable**: `AzGelir_Portable.zip` (39.6 MB)
- **Kurulum**: PowerShell script, NSIS installer
- **Paket Yöneticisi**: Chocolatey support

### Linux (`releases/linux/`)
- **Ana Dosya**: `AzGelir/AzGelir` (1.6 MB)
- **Kurulum**: Bash script (`install.sh`)
- **Desktop**: `.desktop` entry dosyaları
- **Paket Formatları**: Flatpak manifest, AppImage yapısı

## 🔧 Geliştirici Notları

### Build İşlemi
1. **Kaynak geliştirme**: Ana dizinde `main.py` üzerinde çalış
2. **Build çalıştırma**: `build_scripts/` klasöründeki scriptleri kullan
3. **Release oluşturma**: Build sonuçları otomatik olarak `releases/` klasörüne gider

### Yeni Sürüm Çıkarma
1. `main.py`'de değişiklikleri yap
2. Windows build: `python build_scripts/build_all_windows.py`
3. Linux build: `python build_scripts/build_all_linux.py`
4. `releases/` klasörü GitHub'da dağıtıma hazır

## ✨ Kullanıcı Deneyimi

**Yeni kullanıcılar için:**
- `releases/README.md` → Platform seçimi
- `releases/windows/README.md` → Windows kurulum
- `releases/linux/README.md` → Linux kurulum

**Geliştiriciler için:**
- Ana `README.md` → Proje genel bilgisi
- `build_scripts/README.md` → Build süreçleri
- Bu dosya → Proje yapısı

### 📊 Dosya Boyutları
- **Windows Executable**: 38.5 MB
- **Windows Portable**: 39.6 MB  
- **Linux Binary**: 1.6 MB
- **Kaynak Kod**: ~50 KB

---
**Güncelleme**: Eylül 2025 - Hesap Yönetimi Sürümü v1.0.0