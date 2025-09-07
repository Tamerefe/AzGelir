# 🚀 AzGelir Kurulum Dosyaları

Bu klasör, AzGelir uygulamasının farklı platformlarda kurulması için gerekli tüm kurulum dosyalarını içerir.

## 📋 Dosya Listesi

### 🐧 Linux Kurulum
- **`setup_linux.sh`** (21.2 KB) - **Otomatik Linux kurulum** ⭐
- **`install_linux.sh`** (10.0 KB) - Manuel Linux kurulum

### 🪟 Windows Kurulum  
- **`setup_windows.bat`** (13.1 KB) - **Otomatik Windows kurulum** ⭐

### 📦 Paket Yöneticisi Dosyaları
- **`snapcraft.yaml`** (2.4 KB) - Ubuntu Snap paketi manifest
- **`installer.nsi`** (4.3 KB) - NSIS Windows installer script

## 🎯 Kullanım Rehberi

### 🚀 Hızlı Kurulum (Önerilen)

#### Linux
```bash
# Otomatik kurulum (internet gerekli)
curl -sSL https://raw.githubusercontent.com/Tamerefe/AzGelir/main/installers/setup_linux.sh | bash

# Veya yerel dosya ile
chmod +x setup_linux.sh
./setup_linux.sh
```

#### Windows
```batch
# Otomatik kurulum (yönetici gerekli)
setup_windows.bat

# Veya PowerShell ile
powershell -ExecutionPolicy Bypass -File setup_windows.bat
```

### 📦 Platform Özel Kurulum

#### Ubuntu Snap
```bash
# Snap paketi kur
sudo snap install azgelir --devmode

# Snap ile çalıştır
snap run azgelir
```

#### Manuel Linux Kurulum
```bash
# Bağımlılıkları elle yükle
./install_linux.sh

# Python sanal ortam oluştur
python3 -m venv azgelir_env
source azgelir_env/bin/activate
pip install -r requirements.txt
```

## 📊 Kurulum Detayları

### ⭐ `setup_linux.sh` - Linux Otomatik Kurulum
- **Boyut:** 21.2 KB
- **Özellikler:**
  - 🎨 Renkli terminal arayüzü
  - 📊 İlerleme çubukları
  - 🔍 Sistem uyumluluk kontrolü
  - 📦 Otomatik bağımlılık kurulumu
  - 🖥️ Desktop entry oluşturma
  - 🔗 Uygulama menüsü entegrasyonu

```bash
# Desteklenen kurulum türleri
[1] PyInstaller Binary (Önerilen)
[2] AppImage (Portable)
[3] Snap Package (Ubuntu)
[4] Flatpak (Universal)
[5] Python Source (Geliştirici)
```

### ⭐ `setup_windows.bat` - Windows Otomatik Kurulum
- **Boyut:** 13.1 KB
- **Özellikler:**
  - 🎨 ANSI renkli çıktı
  - ✅ Python/pip otomatik kontrolü
  - 📦 PyQt5 otomatik kurulumu
  - 🔗 Masaüstü kısayolu oluşturma
  - 📋 Başlat menüsü entegrasyonu
  - 🗑️ Temiz kaldırma seçeneği

```batch
# Desteklenen kurulum türleri
[1] PyInstaller Executable (Önerilen) 
[2] MSI Installer Package
[3] NSIS Setup (Advanced)
[4] Portable ZIP Package
[5] Python Source Installation
```

### 🔧 `install_linux.sh` - Manuel Linux Kurulum
- **Boyut:** 10.0 KB
- **Kullanım:** Özelleştirilmiş kurulum
- **Hedef:** Geliştiriciler ve ileri kullanıcılar

### 📦 `snapcraft.yaml` - Snap Paketi
- **Platform:** Ubuntu ve türevleri
- **Avantajlar:** 
  - Otomatik güncelleme
  - Sandbox güvenlik
  - Bağımlılık izolasyonu

### 🪟 `installer.nsi` - NSIS Installer
- **Platform:** Windows
- **Avantajlar:**
  - Profesyonel kurulum deneyimi
  - Uninstaller desteği
  - Registry entegrasyonu

## 🎛️ Kurulum Seçenekleri

### 🔧 Gelişmiş Parametreler

#### Linux Setup
```bash
# Sessiz kurulum
./setup_linux.sh --silent

# Özel dizin
./setup_linux.sh --install-dir="/opt/azgelir"

# Sadece bağımlılık kontrolü
./setup_linux.sh --check-only

# Kaldırma
./setup_linux.sh --uninstall
```

#### Windows Setup
```batch
# Sessiz kurulum
setup_windows.bat /silent

# Özel dizin
setup_windows.bat /dir="C:\MyApps\AzGelir"

# Kısayol oluşturma
setup_windows.bat /desktop /startmenu
```

## 🚨 Sistem Gereksinimleri

### 🐧 Linux
- **Ubuntu 18.04+** / **Debian 10+** / **CentOS 8+**
- **Python 3.8+**
- **Qt5 libraries**
- **2 GB RAM**
- **500 MB disk alanı**

### 🪟 Windows
- **Windows 7/8/10/11** (64-bit)
- **Python 3.8+** (otomatik kurulur)
- **Visual C++ Redistributable** (otomatik kurulur)
- **2 GB RAM**
- **500 MB disk alanı**

## 🔍 Sorun Giderme

### ❌ Yaygın Hatalar

#### Linux
```bash
# Python bulunamadı
sudo apt update && sudo apt install python3 python3-pip

# Qt5 bağımlılık hatası
sudo apt install python3-pyqt5

# İzin hatası
chmod +x setup_linux.sh
```

#### Windows
```batch
# Python bulunamadı
# setup_windows.bat otomatik Python kurumu yapar

# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Yönetici yetkisi
# Sağ tık → "Yönetici olarak çalıştır"
```

### 📝 Log Dosyaları
- **Linux:** `/tmp/azgelir_install.log`
- **Windows:** `%TEMP%\azgelir_install.log`

## 🎮 Hızlı Komutlar

### 🚀 En Hızlı Kurulum
```bash
# Linux
curl -sSL https://github.com/Tamerefe/AzGelir/raw/main/installers/setup_linux.sh | bash

# Windows (PowerShell)
iwr https://github.com/Tamerefe/AzGelir/raw/main/installers/setup_windows.bat | iex
```

### 🗑️ Tamamen Kaldırma
```bash
# Linux
./setup_linux.sh --uninstall --purge

# Windows
setup_windows.bat /uninstall /purge
```

## 📞 Destek

### 🐛 Hata Raporlama
1. **Log dosyasını** kaydedin
2. **Sistem bilgilerini** toplayın
3. **Hata ekran görüntüsü** alın
4. **GitHub Issues**'da rapor edin

### 📧 İletişim
- **GitHub:** [AzGelir Issues](https://github.com/Tamerefe/AzGelir/issues)
- **Platform:** Windows 10+, Ubuntu 20.04+

---

**🎉 Her platformda kolay kurulum deneyimi!**
