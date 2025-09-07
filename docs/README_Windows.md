# AzGelir - Windows Sürümü

## 💾 Kurulum Seçenekleri

### 1. 🚀 Hızlı Kurulum (Önerilen)
```powershell
# PowerShell'i yönetici olarak çalıştırın
.\install.ps1
```

### 2. 📦 NSIS Installer (Gelecekte)
```
AzGelir_Setup.exe dosyasını çalıştırın
```

### 3. 🎒 Portable Sürüm
```powershell
.\install.ps1 -Portable
```

### 4. 📁 Manuel Kurulum
1. `AzGelir.exe` dosyasını istediğiniz klasöre kopyalayın
2. `AzGelir_Baslat.bat` dosyasını çalıştırın

## 🎯 Kullanım

### Kurulumdan Sonra:
- Masaüstü kısayolundan çalıştırın
- Başlat menüsünde "AzGelir" arayın
- Veya doğrudan `AzGelir.exe` dosyasını çalıştırın

### Portable Sürüm:
- `AzGelir_Baslat.bat` dosyasını çalıştırın
- USB bellekte taşıyabilirsiniz

## ⚙️ Sistem Gereksinimleri

### Minimum:
- Windows 7 SP1 / Windows Server 2008 R2 SP1
- .NET Framework 4.6.1 veya üzeri
- 512 MB RAM
- 100 MB disk alanı

### Önerilen:
- Windows 10 / Windows 11
- 1 GB RAM
- 200 MB disk alanı

## 🔧 Sorun Giderme

### "MSVCP140.dll eksik" Hatası:
Microsoft Visual C++ Redistributable for Visual Studio 2015-2022 indirin:
- https://aka.ms/vs/17/release/vc_redist.x64.exe

### Windows Defender Uyarısı:
1. Windows Defender'ı açın
2. Virüs ve tehdit koruması > Ayarlar
3. İstisnalar > İstisna ekle
4. Dosya veya klasör seçip AzGelir.exe ekleyin

### Uygulama Başlamıyor:
1. Antivürüs yazılımınızı kontrol edin
2. Windows güncellemelerini yükleyin
3. .NET Framework'ü güncelleyin
4. Yönetici olarak çalıştırmayı deneyin

### Font Sorunları:
Windows Font ayarlarını kontrol edin:
- Ayarlar > Kişiselleştirme > Yazı tipleri

## 🗑️ Kaldırma

### PowerShell ile:
```powershell
# Yönetici olarak çalıştırın
.\install.ps1 -Uninstall
```

### Manuel:
1. Program dosyalarını silin
2. Masaüstü kısayolunu silin
3. Başlat menüsü kısayolunu silin

### Portable Sürüm:
Klasörü silmeniz yeterlidir.

## 📁 Veri Dosyaları

### Kurulu Sürüm:
```
%PROGRAMFILES%\AzGelir\
```

### Portable Sürüm:
Uygulama klasörünün içinde

### Kullanıcı Verileri:
```
%APPDATA%\AzGelir\
```

## 🔄 Güncelleme

Yeni sürüm çıktığında:
1. Eski sürümü kaldırın
2. Yeni sürümü kurun
3. Verileriniz korunacaktır

## 💡 İpuçları

- **Yedekleme**: Veritabanı dosyasını düzenli olarak yedekleyin
- **Taşınabilirlik**: Portable sürümü USB bellekte kullanın
- **Performans**: SSD diskten çalıştırın
- **Güvenlik**: Windows Defender'ı güncel tutun

## 📞 Destek

- **GitHub**: https://github.com/Tamerefe/AzGelir
- **Issues**: Sorunlar için GitHub'da issue açın
- **Wiki**: Detaylı kullanım kılavuzu

## 📄 Lisans

MIT License - Detaylar için LICENSE dosyasını inceleyin.
