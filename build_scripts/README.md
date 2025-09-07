# 🛠️ AzGelir Build Scripts Klasörü

Bu klasör, AzGelir uygulamasının farklı platformlar için derlenmesi ve kurulum dosyalarının oluşturulması için gerekli tüm araçları içerir.

## 📋 Dosya Listesi

### 🐧 Linux Build Scripts
- **`build_linux.py`** (7.4 KB) - PyInstaller ile Linux executable
- **`build_appimage.py`** (8.1 KB) - AppImage paketi oluşturucu
- **`build_snap.py`** (7.7 KB) - Ubuntu Snap paketi
- **`build_all_linux.py`** (10.5 KB) - Tüm Linux formatları tek seferde

### 🪟 Windows Build Scripts  
- **`build_windows.py`** (25.3 KB) - PyInstaller ile Windows executable + extras
- **`build_msi.py`** (11.6 KB) - MSI kurulum paketi (WiX Toolset)
- **`build_all_windows.py`** (16.9 KB) - Tüm Windows formatları tek seferde

### 🚀 Kurulum Dosyası Oluşturucular
- **`create_simple_setup.py`** (12.2 KB) - **Ana kurulum exe oluşturucu** ⭐
- **`create_ultimate_installer.py`** (25.5 KB) - Gelişmiş kurulum sistemi
- **`create_full_installer.py`** (41.8 KB) - Tam özellikli kurulum sistemi
- **`create_single_exe_installer.bat`** (6.3 KB) - Batch kurulum oluşturucu

## 🎯 Kullanım Rehberi

### 🚀 Hızlı Başlangıç
```bash
# Ana kurulum exe'si oluştur (ÖNERİLEN)
python create_simple_setup.py

# Windows için derle
python build_windows.py

# Linux için derle  
python build_linux.py
```

### 📦 Platform Özel Derleme

#### Windows
```bash
# Tek dosya exe
python build_windows.py

# MSI kurulum paketi
python build_msi.py

# Tüm Windows formatları
python build_all_windows.py
```

#### Linux
```bash
# AppImage (portable)
python build_appimage.py

# Snap paketi (Ubuntu)
python build_snap.py

# Tüm Linux formatları
python build_all_linux.py
```

### 🏗️ Kurulum Sistemi Oluşturma

#### Sıfırdan Bilgisayar Kurulumu
```bash
# Ana kurulum dosyası (Python dahil her şey)
python create_simple_setup.py
# Çıktı: ../AzGelir_Setup.exe (53 MB)

# Gelişmiş kurulum (GUI + özelleştirme)
python create_ultimate_installer.py

# Batch ile kurulum oluştur
create_single_exe_installer.bat
```

## 📊 Script Detayları

### ⭐ `create_simple_setup.py` - Ana Kurulum Oluşturucu
- **Boyut:** 12.2 KB
- **Çıktı:** AzGelir_Setup.exe (53 MB)
- **Özellikler:**
  - Python 3.11 embedded gömülü
  - Grafik kurulum arayüzü (Tkinter)
  - Otomatik bağımlılık kurulumu
  - Sistem kontrolü ve uyumluluk
  - Masaüstü/Başlat menüsü kısayolları

```bash
# Kullanım
python create_simple_setup.py

# Çıktı dosyası
AzGelir_Setup.exe  # Sıfırdan bilgisayar kurulumu
```

### 🪟 `build_windows.py` - Windows Ana Derleyici
- **Boyut:** 25.3 KB  
- **Çıktı:** dist/AzGelir.exe (38 MB)
- **Özellikler:**
  - PyInstaller optimizasyonu
  - Windows tema desteği
  - Portable başlatıcı oluşturma
  - PowerShell kurulum scripti
  - NSIS installer template

### 🐧 `build_linux.py` - Linux Ana Derleyici
- **Boyut:** 7.4 KB
- **Çıktı:** dist/AzGelir (Linux executable)
- **Özellikler:**
  - Static linking
  - Dependencies check
  - Desktop entry oluşturma
  - Sistem entegrasyonu

### 🔧 `build_all_windows.py` - Toplu Windows Build
- **Çıktılar:**
  - AzGelir.exe (PyInstaller)
  - AzGelir_Setup.msi (MSI installer)
  - AzGelir_Portable.zip (Portable)
  - AzGelir_Setup.exe (NSIS)

### 🔧 `build_all_linux.py` - Toplu Linux Build
- **Çıktılar:**
  - AzGelir (PyInstaller executable)
  - AzGelir.AppImage (Portable)
  - azgelir.snap (Snap paketi)
  - azgelir.flatpak (Flatpak paketi)

## 🎛️ Konfigürasyon

### Gereksinimler
```python
# Python paketleri
PyInstaller>=6.0
pywin32 (Windows)
python-AppImage (Linux AppImage için)
snapcraft (Snap için)
```

### Sistem Gereksinimleri
- **Python 3.8+**
- **Windows 10+** (Windows build için)
- **Ubuntu 20.04+** (Linux build için)
- **2 GB RAM** (build sırasında)
- **5 GB disk alanı** (tüm çıktılar için)

## 🚨 Önemli Notlar

### ⚠️ Build Sırası
1. **İlk:** Ana uygulamayı derle (`build_windows.py`)
2. **Sonra:** Kurulum dosyası oluştur (`create_simple_setup.py`)

### 💡 İpuçları
- **create_simple_setup.py** en güncel ve önerilen yöntem
- **build_all_* scripts** batch işlemi için ideal
- **Antivürüs** yazılımı build'i yavaşlatabilir
- **Yönetici yetkisi** gerekebilir (Windows)

### 🔍 Hata Giderme
```bash
# Build hataları için log kontrol
# Windows
type build\AzGelir\warn-AzGelir.txt

# PyInstaller cache temizle
pyinstaller --clean AzGelir.spec
```

## 📈 Performans

### Build Süreleri (Ortalama)
- **build_windows.py:** 2-3 dakika
- **create_simple_setup.py:** 3-5 dakika  
- **build_all_windows.py:** 8-12 dakika

### Dosya Boyutları
- **Windows exe:** 38 MB
- **Kurulum exe:** 53 MB (Python dahil)
- **Linux executable:** 35 MB
- **AppImage:** 45 MB

---

**🎉 Tüm platformlar için profesyonel build sistemi hazır!**
