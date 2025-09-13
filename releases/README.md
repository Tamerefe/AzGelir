# AzGelir - Release Paketi

## 📦 Cross-Platform Dağıtım

Bu klasörde AzGelir uygulamasının tüm platformlar için hazır release dosyaları bulunmaktadır.

### 🗂️ Klasör Yapısı

```
releases/
├── windows/          # Windows için tüm dosyalar
│   ├── AzGelir.exe              # Ana executable (38.5 MB)
│   ├── AzGelir_Portable.zip     # Portable paket (39.6 MB)
│   ├── AzGelir_Portable/        # Portable klasör
│   ├── install.ps1              # PowerShell kurulum
│   ├── installer.nsi            # NSIS installer
│   ├── chocolatey/              # Chocolatey paketi
│   ├── LICENSE.txt              # Lisans
│   └── README.md                # Windows rehberi
│
├── linux/            # Linux için tüm dosyalar
│   ├── AzGelir/                 # Binary klasörü (1.6 MB)
│   ├── install.sh               # Kurulum scripti
│   ├── uninstall.sh             # Kaldırma scripti
│   ├── AzGelir.desktop          # Desktop entry
│   ├── io.github.tamerefe.AzGelir.json    # Flatpak manifest
│   ├── AzGelir.AppDir/          # AppImage yapı klasörü
│   └── README.md                # Linux rehberi
│
└── README.md         # Bu dosya
```

### 🚀 Platform Seçimi

#### Windows Kullanıcıları
**👉 `windows/` klasörüne gidin**
- **Hızlı kullanım**: `AzGelir_Portable.zip` indirin
- **Tam kurulum**: `AzGelir.exe` indirin
- **Detaylar**: `windows/README.md` okuyun

#### Linux Kullanıcıları  
**👉 `linux/` klasörüne gidin**
- **Otomatik kurulum**: `install.sh` çalıştırın
- **Manuel kurulum**: `AzGelir/AzGelir` binary'sini çalıştırın
- **Detaylar**: `linux/README.md` okuyun

### ✨ Sürüm Bilgileri

**Versiyon**: v1.0.0  
**Çıkış Tarihi**: Eylül 2025  
**Hesap Yönetimi**: ✅ Yeni!

#### 🆕 Bu Sürümdeki Yenilikler

- ➕ **Yeni Hesap Ekleme**: Kullanıcılar artık kendi hesap kodlarını tanımlayabilir
- 🗑️ **Hesap Silme**: İstenmeyen hesaplar güvenli şekilde silinebilir
- 🔒 **Güvenlik Kontrolleri**: Duplicate kod kontrolü ve işlem varken silme uyarısı
- 💾 **Veritabanı Yenilemeleri**: Hesaplar artık ayrı tabloda tutuluyor
- 🎨 **Modern Arayüz**: Yeni buton tasarımları ve tooltip'ler

### 📊 Platform Karşılaştırması

| Özellik | Windows | Linux |
|---------|---------|-------|
| Boyut | 38.5 MB | 1.6 MB |
| Kurulum | Tek tık | Script |
| Portable | ✅ | ✅ |
| Store | Chocolatey | Flatpak |
| Bağımlılık | Yok | PyQt5 |

### 🔄 Güncelleme Notları

**Önceki sürümden gelen kullanıcılar:**
- Veritabanı otomatik olarak yeni formata dönüştürülür
- Mevcut veriler korunur
- Yeni hesap yönetimi özellikleri etkinleşir

### 📋 Kalite Kontrol

**Test Edilen Platformlar:**
- ✅ Windows 10 (64-bit)
- ✅ Windows 11 (64-bit)
- ✅ Ubuntu 20.04 LTS
- ✅ Ubuntu 22.04 LTS
- ⚠️ Diğer Linux dağıtımları (PyQt5 gerekebilir)

### 📞 Destek ve Katkı

- **GitHub Repository**: [Tamerefe/AzGelir](https://github.com/Tamerefe/AzGelir)
- **Issues**: Bug raporları ve özellik istekleri
- **Discussions**: Genel sorular ve tartışmalar
- **Wiki**: Detaylı dokumentasyon

### 📝 Lisans

MIT License - Özgürce kullanın, değiştirin ve dağıtın.

---

**İndirme Önerileri:**
- **Windows**: `windows/AzGelir_Portable.zip` (en pratik)
- **Linux**: `linux/` klasörünü tamamen indirin
- **Geliştiriciler**: Tüm `releases/` klasörünü klonlayın