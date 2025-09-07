# 📖 AzGelir Kurulum Kılavuzu

## 🎯 Genel Bakış

AzGelir, PyQt5 tabanlı modern bir gelir/gider takip uygulamasıdır. Bu kılavuz, uygulamayı farklı işletim sistemlerinde kurma ve paketleme süreçlerini detaylı olarak açıklar.

## 📋 İçindekiler

- [Sistem Gereksinimleri](#sistem-gereksinimleri)
- [Linux Kurulumu](#linux-kurulumu)
- [Windows Kurulumu](#windows-kurulumu)
- [Geliştirici Kurulumu](#geliştirici-kurulumu)
- [Paket Formatları](#paket-formatları)
- [Sorun Giderme](#sorun-giderme)
- [SSS](#sık-sorulan-sorular)

---

## 🖥️ Sistem Gereksinimleri

### Minimum Gereksinimler

#### Linux:
- **İşletim Sistemi**: Ubuntu 18.04+, Debian 10+, Fedora 30+, CentOS 7+
- **Python**: 3.6 veya üzeri
- **RAM**: 512 MB
- **Disk Alanı**: 200 MB
- **Display Server**: X11 veya Wayland

#### Windows:
- **İşletim Sistemi**: Windows 7 SP1+ / Windows Server 2008 R2 SP1+
- **Framework**: .NET Framework 4.6.1+
- **RAM**: 512 MB  
- **Disk Alanı**: 200 MB
- **Mimari**: 32-bit veya 64-bit

### Önerilen Gereksinimler

#### Linux:
- **İşletim Sistemi**: Ubuntu 20.04+, Fedora 35+
- **Python**: 3.8+
- **RAM**: 1 GB
- **Disk Alanı**: 500 MB
- **SSD**: Performans için önerilir

#### Windows:
- **İşletim Sistemi**: Windows 10/11
- **Framework**: .NET Framework 4.8
- **RAM**: 1 GB
- **Disk Alanı**: 500 MB
- **SSD**: Performans için önerilir

---

## 🐧 Linux Kurulumu

### 🚀 Hızlı Kurulum (Önerilen)

**En kolay yöntem:**

```bash
# Repository'yi klonlayın
git clone https://github.com/Tamerefe/AzGelir.git
cd AzGelir

# Kurulum sihirbazını başlatın
chmod +x setup_linux.sh
./setup_linux.sh
```

Kurulum sihirbazı açılacak ve size rehberlik edecektir.

### 📦 Paket Formatlarına Göre Kurulum

#### 1. Standart Linux Paketi

```bash
# Bağımlılıkları yükleyin
sudo apt update  # Ubuntu/Debian
sudo apt install python3 python3-pip python3-pyqt5

# Paketi oluşturun
python3 build_linux.py

# Kurun
cd dist
./install.sh
```

#### 2. AppImage (Taşınabilir)

```bash
# AppImage oluşturun
python3 build_appimage.py

# Çalıştırın
chmod +x AzGelir-x86_64.AppImage
./AzGelir-x86_64.AppImage
```

#### 3. Snap Paketi

```bash
# Snap paketi oluşturun
python3 build_snap.py

# Kurun
sudo snap install azgelir_1.0.0_amd64.snap --dangerous --devmode

# Çalıştırın
azgelir
```

#### 4. Flatpak

```bash
# Flatpak manifest oluşturun
python3 build_all_linux.py --format flatpak

# Build edin
flatpak-builder build-dir io.github.tamerefe.AzGelir.json
flatpak build-export repo build-dir
flatpak --user remote-add --no-gpg-verify azgelir-repo repo
flatpak --user install azgelir-repo io.github.tamerefe.AzGelir
```

### 📋 Dağıtım Bazlı Kurulum

#### Ubuntu/Debian:

```bash
# Sistem paketleri
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-pyqt5 \
                 python3-pyqt5.qtwidgets python3-pyqt5.qtcore \
                 python3-pyqt5.qtgui fonts-liberation fonts-dejavu

# Python paketleri
pip3 install --user -r requirements.txt

# Hızlı kurulum
./setup_linux.sh --quick
```

#### Fedora:

```bash
# Sistem paketleri
sudo dnf install python3 python3-pip python3-qt5 python3-qt5-devel \
                 liberation-fonts dejavu-fonts

# Python paketleri
pip3 install --user -r requirements.txt

# Hızlı kurulum
./setup_linux.sh --quick
```

#### CentOS/RHEL:

```bash
# EPEL repository ekleyin
sudo yum install epel-release

# Sistem paketleri
sudo yum install python3 python3-pip python3-qt5 python3-qt5-devel

# Python paketleri
pip3 install --user -r requirements.txt

# Hızlı kurulum
./setup_linux.sh --quick
```

#### Arch Linux:

```bash
# Sistem paketleri
sudo pacman -S python python-pip python-pyqt5 ttf-liberation ttf-dejavu

# Python paketleri
pip install --user -r requirements.txt

# Hızlı kurulum
./setup_linux.sh --quick
```

---

## 🪟 Windows Kurulumu

### 🚀 Hızlı Kurulum (Önerilen)

**En kolay yöntem:**

```cmd
# Repository'yi klonlayın
git clone https://github.com/Tamerefe/AzGelir.git
cd AzGelir

# Kurulum sihirbazını başlatın
setup_windows.bat
```

### 📦 Paket Formatlarına Göre Kurulum

#### 1. Windows Executable

```cmd
# Python gereksinimlerini yükleyin
pip install -r requirements.txt

# Executable oluşturun
python build_windows.py

# PowerShell ile kurun (Yönetici olarak)
powershell -ExecutionPolicy Bypass -File "dist\install.ps1"
```

#### 2. MSI Installer (Enterprise)

```cmd
# WiX Toolset gerekli: https://wixtoolset.org/

# MSI oluşturun
python build_msi.py

# Kurun
msiexec /i AzGelir_Setup.msi

# Veya sessiz kurulum
msiexec /i AzGelir_Setup.msi /quiet
```

#### 3. NSIS Installer

```cmd
# NSIS gerekli: https://nsis.sourceforge.io/

# NSIS installer oluşturun
python build_all_windows.py --format nsis

# Kurun
AzGelir_Setup.exe
```

#### 4. Portable Sürüm

```cmd
# Portable sürüm oluşturun
python build_all_windows.py --format portable

# ZIP'i açın ve çalıştırın
# AzGelir_Portable.zip -> AzGelir_Baslat.bat
```

#### 5. Chocolatey Paketi

```powershell
# Chocolatey gerekli: https://chocolatey.org/

# Paket oluşturun
python build_all_windows.py --format chocolatey

# Kurun (gelecekte)
choco install azgelir
```

### 🔧 Ön Gereksinimler

#### Python Kurulumu:

1. https://www.python.org/downloads/ adresinden Python 3.6+ indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu doğrulayın:
   ```cmd
   python --version
   pip --version
   ```

#### Visual C++ Redistributable:

Bazı paketler için gerekli olabilir:
- https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## 👨‍💻 Geliştirici Kurulumu

### Kaynak Koddan Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/Tamerefe/AzGelir.git
cd AzGelir

# Virtual environment oluşturun (önerilen)
python3 -m venv azgelir_env
source azgelir_env/bin/activate  # Linux
# azgelir_env\Scripts\activate   # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python main.py
```

### Development Ortamı

```bash
# Geliştirme bağımlılıkları
pip install -r requirements.txt
pip install black flake8 pytest  # Code formatting ve testing

# Pre-commit hooks (opsiyonel)
pip install pre-commit
pre-commit install

# Test çalıştırma
python -m pytest tests/

# Code formatting
black main.py
flake8 main.py
```

---

## 📦 Paket Formatları Detayı

### Linux Paket Formatları

| Format | Dosya | Avantajlar | Kullanım |
|--------|-------|------------|----------|
| **Standart** | `dist/AzGelir` | Hızlı, küçük boyut | Geleneksel kurulum |
| **AppImage** | `AzGelir-x86_64.AppImage` | Taşınabilir, kurulum gerektirmez | USB, test ortamları |
| **Snap** | `azgelir_1.0.0_amd64.snap` | Otomatik güncelleme, güvenlik | Ubuntu, modern dağıtımlar |
| **Flatpak** | `io.github.tamerefe.AzGelir.json` | Evrensel, sandbox | Çapraz platform |

### Windows Paket Formatları

| Format | Dosya | Avantajlar | Kullanım |
|--------|-------|------------|----------|
| **Executable** | `dist/AzGelir.exe` | Tek dosya, hızlı | Hızlı test, geliştirme |
| **MSI** | `AzGelir_Setup.msi` | Enterprise, Group Policy | Kurumsal ortamlar |
| **NSIS** | `AzGelir_Setup.exe` | Özelleştirilebilir UI | Son kullanıcı dağıtımı |
| **Portable** | `AzGelir_Portable.zip` | Kurulum gerektirmez | USB, taşınabilir |
| **Chocolatey** | `azgelir.nuspec` | Package manager | Otomatik güncelleme |

---

## 🔧 Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

#### Linux Sorunları

**Problem**: `ImportError: No module named 'PyQt5'`
```bash
# Çözüm - Ubuntu/Debian:
sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets

# Çözüm - Fedora:
sudo dnf install python3-qt5

# Çözüm - pip ile:
pip3 install --user PyQt5
```

**Problem**: Font sorunları (Türkçe karakterler görünmüyor)
```bash
# Çözüm:
sudo apt install fonts-liberation fonts-dejavu fonts-noto
fc-cache -f -v
```

**Problem**: AppImage çalışmıyor
```bash
# Çözüm - FUSE yükleyin:
sudo apt install fuse

# İzin verin:
chmod +x AzGelir-x86_64.AppImage

# Wayland sorunu:
QT_QPA_PLATFORM=xcb ./AzGelir-x86_64.AppImage
```

**Problem**: Snap çalışmıyor
```bash
# Çözüm - Snap desteği:
sudo apt install snapd

# Manuel bağlantı:
sudo snap connect azgelir:home
sudo snap connect azgelir:desktop
```

#### Windows Sorunları

**Problem**: `MSVCP140.dll eksik`
```
Çözüm: Visual C++ Redistributable yükleyin
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

**Problem**: Windows Defender uyarısı
```
Çözüm:
1. Windows Defender > Virüs ve tehdit koruması
2. İstisnalar > İstisna ekle > Dosya
3. AzGelir.exe dosyasını seçin
```

**Problem**: Uygulama başlamıyor
```
Çözüm kontrolü:
1. Python kurulu mu? python --version
2. Bağımlılıklar yüklü mü? pip list
3. Yönetici olarak çalıştırmayı deneyin
4. Windows güncellemelerini kontrol edin
```

**Problem**: PyQt5 import hatası
```cmd
# Çözüm:
pip uninstall PyQt5
pip install PyQt5==5.15.7

# Alternatif:
pip install --force-reinstall PyQt5
```

### Debug ve Log

#### Linux Debug:
```bash
# Verbose çıktı
python3 main.py --verbose

# X11 debug
export QT_LOGGING_RULES=qt.qpa.*=true
python3 main.py

# Wayland debug
export QT_QPA_PLATFORM=wayland
export QT_WAYLAND_SHELL_INTEGRATION=xdg-shell
python3 main.py
```

#### Windows Debug:
```cmd
# Console çıktı
python main.py

# Environment variables
set QT_DEBUG_PLUGINS=1
python main.py

# PyInstaller debug
python -c "import sys; print(sys.path)"
```

---

## ❓ Sık Sorulan Sorular

### Genel Sorular

**S: AzGelir açık kaynak mı?**
C: Evet, MIT lisansı ile tamamen açık kaynak.

**S: Verilerim güvende mi?**
C: Evet, tüm veriler yerel SQLite veritabanında saklanır.

**S: İnternet bağlantısı gerekir mi?**
C: Hayır, tamamen offline çalışır.

**S: Veritabanı dosyası nerede?**
C: 
- Linux: `~/.local/share/AzGelir/records.db`
- Windows: Uygulama klasöründe `records.db`

### Kurulum Soruları

**S: Python bilmiyorum, yine de kurabilir miyim?**
C: Evet, kurulum sihirbazları otomatik olarak her şeyi halleder.

**S: Hangi paket formatını seçmeliyim?**
C: 
- **Yeni kullanıcılar**: Hızlı kurulum
- **Taşınabilirlik**: AppImage (Linux) veya Portable (Windows)
- **Enterprise**: MSI (Windows) veya Snap (Linux)

**S: Güncelleme nasıl yapılır?**
C: Yeni sürüm çıktığında aynı kurulum adımlarını tekrarlayın.

**S: Birden fazla bilgisayarda kullanabilir miyim?**
C: Evet, portable sürümleri USB ile taşıyabilirsiniz.

### Teknik Sorular

**S: Python 2 ile çalışır mı?**
C: Hayır, Python 3.6+ gereklidir.

**S: Qt4 ile çalışır mı?**
C: Hayır, PyQt5 gereklidir.

**S: 32-bit sistemlerde çalışır mı?**
C: Evet, hem 32-bit hem 64-bit desteklenir.

**S: ARM işlemcilerde çalışır mı?**
C: Raspberry Pi gibi ARM Linux sistemlerde çalışabilir.

---

## 🆘 Destek

### Yardım Alma

1. **GitHub Issues**: https://github.com/Tamerefe/AzGelir/issues
2. **Dokümantasyon**: Bu kılavuzu tekrar inceleyin
3. **Community**: GitHub Discussions bölümü

### Bug Raporu

Sorun bildirirken şunları ekleyin:

```
- İşletim sistemi ve versiyonu
- Python versiyonu
- Hata mesajı (tam metin)
- Adım adım tekrar etme yöntemi
- Beklenen davranış
- Gerçek davranış
```

### Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun
3. Değişiklikleri commit edin
4. Pull request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE.txt) dosyasını inceleyin.

---

## 🙏 Teşekkürler

AzGelir kullandığınız için teşekkürler! Uygulama işinize yarayacağını umuyoruz.

**İyi kullanımlar!** 🚀
