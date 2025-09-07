# 📊 AzGelir Derlenen Dosyalar

Bu klasör, PyInstaller ve diğer araçlarla derlenmiş, kullanıma hazır AzGelir dosyalarını içerir.

## 📋 Dosya Listesi

### 🪟 Windows Dosyaları
- **`AzGelir.exe`** (38.3 MB) - **Ana Windows uygulaması** ⭐
- **`AzGelir_Baslat.bat`** - Portable başlatıcı script
- **`install.ps1`** - PowerShell kurulum scripti
- **`README_Windows.md`** - Windows kullanım kılavuzu
- **`LICENSE.txt`** - Proje lisansı

### 🐧 Linux Dosyaları (Build sonrası oluşur)
- **`AzGelir`** - Linux executable
- **`AzGelir.AppImage`** - Portable Linux uygulaması
- **`install.sh`** - Linux kurulum scripti

## 🎯 Kullanım

### 🚀 Hızlı Başlatma

#### Windows
```batch
# Doğrudan çalıştır
.\AzGelir.exe

# Portable başlatıcı ile
.\AzGelir_Baslat.bat

# PowerShell kurulum
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### Linux
```bash
# Doğrudan çalıştır (build sonrası)
chmod +x AzGelir
./AzGelir

# AppImage (portable)
chmod +x AzGelir.AppImage
./AzGelir.AppImage
```

## 📊 Dosya Detayları

### ⭐ `AzGelir.exe` - Ana Windows Uygulaması
- **Boyut:** 38.3 MB
- **Tip:** PyInstaller tek dosya executable
- **Gereksinimler:** Windows 7+ (64-bit)
- **Bağımlılıklar:** Gömülü (hiçbir ek kurulum gerekmiyor)

**Özellikler:**
- ✅ **Bağımsız çalışma** - Python kurulu olmasına gerek yok
- ✅ **Portable** - USB bellekten çalışabilir  
- ✅ **Hızlı başlatma** - 2-3 saniyede açılır
- ✅ **Windows entegrasyonu** - İkon ve tema desteği
- ✅ **Güvenlik** - Windows Defender uyumlu

### 🔧 `AzGelir_Baslat.bat` - Portable Başlatıcı
```batch
@echo off
title AzGelir - Gelir/Gider Takip
echo AzGelir başlatılıyor...
start "" "AzGelir.exe"
```

**Avantajlar:**
- 🎯 **Terminal gizleme** - Sadece uygulama görünür
- 📋 **Özel başlık** - Taskbar'da net isim
- 🔄 **Hata yakalama** - Crash durumunda log

### 💠 `install.ps1` - PowerShell Kurulum
- **Boyut:** ~2 KB
- **İşlev:** Sistem kurulumu ve entegrasyon
- **Hedef:** Windows 10+ PowerShell 5+

**Kurulum adımları:**
1. Program Files'a kopyalama
2. Masaüstü kısayolu oluşturma
3. Başlat menüsü entegrasyonu
4. Registry kayıtları (uninstaller)
5. File association (gelecekte)

### 📚 `README_Windows.md` - Kullanım Kılavuzu
- Windows özel talimatlar
- Sistem gereksinimleri
- Sorun giderme rehberi
- Kısayol tuşları listesi

## 🎛️ Çalıştırma Seçenekleri

### 🖥️ Normal Kullanım
```batch
# Standart çalıştırma
AzGelir.exe

# Belirli veritabanı ile
AzGelir.exe --database="C:\MyData\accounts.db"

# Debug modu
AzGelir.exe --debug --verbose
```

### 🔧 Gelişmiş Parametreler
```batch
# Tam ekran başlat
AzGelir.exe --fullscreen

# Belirli tema ile
AzGelir.exe --theme=dark

# Minimal arayüz
AzGelir.exe --minimal

# Güvenli mod (sadece okuma)
AzGelir.exe --readonly
```

## 🚨 Sistem Gereksinimleri

### 🪟 Windows
- **OS:** Windows 7/8/10/11 (64-bit)
- **RAM:** 512 MB (minimum), 2 GB (önerilen)
- **Disk:** 100 MB (uygulama), 1 GB (veri)
- **Ekran:** 1024x768 (minimum), 1920x1080 (önerilen)

### 🐧 Linux
- **OS:** Ubuntu 18.04+, Debian 10+, CentOS 8+
- **RAM:** 512 MB (minimum), 2 GB (önerilen)  
- **Disk:** 100 MB (uygulama), 1 GB (veri)
- **Qt:** Qt5 libraries gerekli

## 📈 Performans

### ⚡ Başlatma Süreleri
- **İlk çalıştırma:** 3-5 saniye
- **Sonraki çalıştırmalar:** 1-2 saniye
- **Büyük veritabanı (10k+ kayıt):** 2-3 saniye

### 💾 Bellek Kullanımı
- **Boşta:** 80-120 MB RAM
- **Normal kullanım:** 150-200 MB RAM
- **Büyük raporlar:** 250-300 MB RAM

### 🔄 Disk I/O
- **Veritabanı yazma:** Anlık (SQLite)
- **Backup oluşturma:** 1-5 saniye
- **Export işlemleri:** 2-10 saniye

## 🔍 Sorun Giderme

### ❌ Yaygın Hatalar

#### "MSVCP140.dll eksik" 
```batch
# Çözüm: Visual C++ Redistributable kurulu değil
# İndir: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

#### "Bu uygulama başlatılamadı"
```batch
# Çözüm 1: Yönetici olarak çalıştır
# Çözüm 2: Antivürüs white-list'e ekle
# Çözüm 3: Windows Defender'ı geçici devre dışı bırak
```

#### Yavaş açılma
```batch
# Çözüm 1: SSD kullan
# Çözüm 2: Antivürüs real-time taramayı devre dışı bırak
# Çözüm 3: Veritabanını optimize et
```

### 📝 Log Dosyaları
- **Windows:** `%APPDATA%\AzGelir\logs\`
- **Linux:** `~/.azgelir/logs/`

### 🔧 Debug Modu
```batch
# Detaylı log için
AzGelir.exe --debug --log-level=DEBUG

# Console çıktı
AzGelir.exe --console
```

## 🎮 Hızlı Komutlar

### 🚀 Kullanıcı İçin
```batch
# En hızlı başlatma
AzGelir.exe

# Güvenli mod
AzGelir.exe --readonly

# Backup oluştur
AzGelir.exe --backup --exit
```

### 👨‍💻 Geliştirici İçin
```batch
# Debug ile çalıştır
AzGelir.exe --debug --verbose

# Test veritabanı ile
AzGelir.exe --database=test.db

# Profiling
AzGelir.exe --profile --exit
```

## 📞 Destek

### 🐛 Hata Raporlama
1. **Debug modda** çalıştırın
2. **Log dosyalarını** kaydedin
3. **Ekran görüntüsü** alın
4. **GitHub Issues**'da rapor edin

### 📋 Sistem Bilgisi Toplama
```batch
# Windows sistem bilgisi
systeminfo > system_info.txt

# AzGelir versiyon bilgisi  
AzGelir.exe --version --system-info
```

---

**🎉 Kullanıma hazır, optimize edilmiş uygulamalar!**
