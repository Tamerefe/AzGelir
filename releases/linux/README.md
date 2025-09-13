# AzGelir - Linux Sürümü

## 📦 Paket İçeriği

Bu klasörde AzGelir uygulamasının Linux sürümü ve kurulum dosyaları bulunmaktadır.

### 🚀 Hızlı Başlangıç

**En Kolay Yol - Otomatik Kurulum:**
```bash
chmod +x install.sh
./install.sh
```

**Manuel Kurulum:**
```bash
chmod +x AzGelir/AzGelir
./AzGelir/AzGelir
```

### 📁 Dosya Açıklamaları

- **`AzGelir/`** - Ana uygulama klasörü (binary dahil)
- **`install.sh`** - Otomatik kurulum scripti
- **`uninstall.sh`** - Kaldırma scripti
- **`AzGelir.desktop`** - Desktop entry dosyası
- **`io.github.tamerefe.AzGelir.json`** - Flatpak manifest
- **`io.github.tamerefe.AzGelir.desktop`** - Flatpak desktop entry
- **`io.github.tamerefe.AzGelir.metainfo.xml`** - Uygulama metadatası
- **`AzGelir.AppDir/`** - AppImage yapı klasörü

### 🔧 Sistem Gereksinimleri

- **İşletim Sistemi**: Ubuntu 18.04+, Debian 10+, Fedora 30+, openSUSE 15+
- **Mimari**: x86_64 (64-bit)
- **RAM**: Minimum 512 MB
- **Disk Alanı**: 50 MB
- **Bağımlılıklar**: PyQt5 (otomatik yüklenir)

### ✨ Yeni Özellikler

Bu sürümde eklenen hesap yönetimi özellikleri:
- ➕ Yeni hesap ekleme
- 🗑️ Hesap silme
- Dinamik hesap listesi
- Gelişmiş güvenlik kontrolleri

### 🛠️ Kurulum Seçenekleri

#### 1. Otomatik Kurulum (Önerilen)
```bash
# Kurulum scriptini çalıştırır
chmod +x install.sh
./install.sh

# Uygulama menüsünden veya terminal'den çalıştırılabilir
azgelir
```

#### 2. Manuel Kurulum
```bash
# Binary'yi istediğiniz konuma kopyalayın
sudo cp -r AzGelir /opt/
sudo chmod +x /opt/AzGelir/AzGelir

# Desktop entry'yi kurun
sudo cp AzGelir.desktop /usr/share/applications/

# Çalıştırın
/opt/AzGelir/AzGelir
```

#### 3. Flatpak İle Kurulum
```bash
# Flatpak build (geliştiriciler için)
flatpak-builder build-dir io.github.tamerefe.AzGelir.json
flatpak-builder --user --install --force-clean build-dir io.github.tamerefe.AzGelir.json

# Çalıştırma
flatpak run io.github.tamerefe.AzGelir
```

#### 4. AppImage Oluşturma
```bash
# AppImage build (Linux sistemde)
# AzGelir.AppDir klasörü hazır
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage AzGelir.AppDir
```

### 📱 Desktop Entegrasyonu

Kurulum sonrası:
- Uygulama menüsünde "AzGelir" adıyla görünür
- Aktiviteler/Launcher'dan aranabilir
- Masaüstü kısayolu oluşturulabilir

### 🔄 Güncelleme

```bash
# Kaldırma
./uninstall.sh

# Yeni sürümü kurma
./install.sh
```

### 🗑️ Kaldırma

```bash
chmod +x uninstall.sh
./uninstall.sh
```

### 🐧 Dağıtım Spesifik Notlar

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pyqt5
```

**Fedora:**
```bash
sudo dnf install python3-qt5
```

**Arch Linux:**
```bash
sudo pacman -S python-pyqt5
```

**openSUSE:**
```bash
sudo zypper install python3-qt5
```

### 🆘 Sorun Giderme

**PyQt5 hatası:**
```bash
pip3 install --user PyQt5
```

**İzin hatası:**
```bash
chmod +x AzGelir/AzGelir
```

**Desktop entry görünmüyor:**
```bash
sudo update-desktop-database
```

### 📞 Destek

- **GitHub**: [Tamerefe/AzGelir](https://github.com/Tamerefe/AzGelir)
- **Issues**: Sorunları GitHub Issues'da bildirin
- **Wiki**: Detaylı dokumentasyon için GitHub Wiki

---
**Sürüm**: v1.0.0 | **Platform**: Linux x86_64 | **Tarih**: Eylül 2025