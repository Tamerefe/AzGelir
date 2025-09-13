# AzGelir - Windows Sürümü

## 📦 Paket İçeriği

Bu klasörde AzGelir uygulamasının Windows sürümü ve kurulum dosyaları bulunmaktadır.

### 🚀 Hızlı Başlangıç

**En Kolay Yol - Portable Sürüm:**
1. `AzGelir_Portable.zip` dosyasını indirin
2. Herhangi bir klasöre çıkarın
3. `AzGelir.exe` dosyasına çift tıklayın

**Tam Kurulum:**
1. `AzGelir.exe` dosyasını indirin
2. Dosyaya çift tıklayın ve çalıştırın
3. İsteğe bağlı: Masaüstü kısayolu için `install.ps1` scriptini çalıştırın

### 📁 Dosya Açıklamaları

- **`AzGelir.exe`** - Ana uygulama (tek dosya, 38.5 MB)
- **`AzGelir_Portable.zip`** - Portable sürüm paketi (39.6 MB)
- **`AzGelir_Portable/`** - Portable sürüm klasörü
- **`install.ps1`** - PowerShell kurulum scripti
- **`installer.nsi`** - NSIS installer scripti
- **`chocolatey/`** - Chocolatey paket dosyaları
- **`LICENSE.txt`** - Lisans dosyası

### 🔧 Sistem Gereksinimleri

- **İşletim Sistemi**: Windows 7, 8, 10, 11 (64-bit)
- **RAM**: Minimum 512 MB
- **Disk Alanı**: 50 MB
- **Ek Yazılım**: Gerekli değil (standalone)

### ✨ Yeni Özellikler

Bu sürümde eklenen hesap yönetimi özellikleri:
- ➕ Yeni hesap ekleme
- 🗑️ Hesap silme
- Dinamik hesap listesi
- Gelişmiş güvenlik kontrolleri

### 🛠️ Kurulum Seçenekleri

#### 1. Portable Kullanım
```
1. AzGelir_Portable.zip'i çıkarın
2. Klasörde AzGelir.exe'yi çalıştırın
3. Kurulum gerektirmez!
```

#### 2. PowerShell İle Kurulum
```powershell
# PowerShell'i yönetici olarak açın
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

#### 3. Chocolatey İle Kurulum
```cmd
# Gelecekte kullanılabilir
choco install azgelir
```

### 🔄 Güncelleme

Yeni sürüm çıktığında:
1. Eski `AzGelir.exe` dosyasını silin
2. Yeni dosyayı indirin
3. Aynı klasöre koyun
4. Verileriniz korunur (`records.db`)

### 🆘 Sorun Giderme

**Uygulama açılmıyor:**
- Windows Defender'dan "Daha fazla bilgi" → "Yine de çalıştır"
- Dosyayı sağ tık → "Yönetici olarak çalıştır"

**Veriler görünmüyor:**
- `records.db` dosyasının aynı klasörde olduğundan emin olun

### 📞 Destek

- **GitHub**: [Tamerefe/AzGelir](https://github.com/Tamerefe/AzGelir)
- **Issues**: Sorunları GitHub Issues'da bildirin
- **Dokumentasyon**: Ana README.md dosyasını inceleyin

---
**Sürüm**: v1.0.0 | **Platform**: Windows x64 | **Tarih**: Eylül 2025