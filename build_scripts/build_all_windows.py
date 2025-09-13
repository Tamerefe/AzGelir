#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Windows Paketleme Merkezi
Tüm Windows paket formatları için tek script
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

def print_banner():
    """Başlık banner'ını yazdır"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                   AzGelir Windows Paketleme                  ║
║                   Gelir/Gider Takip Uygulaması               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 veya üzeri gerekli!")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")

def install_dependencies():
    """Gerekli bağımlılıkları yükle"""
    print("📦 Gerekli Python paketleri yükleniyor...")
    
    required_packages = [
        "pyinstaller",
        "PyQt5",
        "pywin32"  # Windows kısayolları için
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} zaten yüklü")
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} yüklendi")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} yükleme hatası: {e}")

def build_executable():
    """PyInstaller ile exe oluştur"""
    print("\n💻 Windows exe dosyası oluşturuluyor...")
    try:
        subprocess.check_call([sys.executable, "build_scripts/build_windows.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Exe oluşturma hatası: {e}")
        return False

def build_msi():
    """MSI installer oluştur"""
    print("\n📦 MSI installer oluşturuluyor...")
    try:
        subprocess.check_call([sys.executable, "build_scripts/build_msi.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ MSI oluşturma hatası: {e}")
        return False

def build_nsis():
    """NSIS installer oluştur"""
    print("\n🛠️ NSIS installer oluşturuluyor...")
    
    # NSIS kontrol
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe",
        "makensis.exe"  # PATH'te varsa
    ]
    
    nsis_exe = None
    for path in nsis_paths:
        if shutil.which(path) or os.path.exists(path):
            nsis_exe = path
            break
    
    if not nsis_exe:
        print("⚠️ NSIS bulunamadı. NSI script oluşturuldu ancak derlenemedi.")
        print("   NSIS indirmek için: https://nsis.sourceforge.io/")
        return False
    
    try:
        subprocess.check_call([nsis_exe, "installer.nsi"])
        print("✅ NSIS installer oluşturuldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ NSIS derleme hatası: {e}")
        return False

def build_portable():
    """Portable sürüm oluştur"""
    print("\n🎒 Portable sürüm hazırlanıyor...")
    
    portable_dir = "AzGelir_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Dosyaları kopyala
    files_to_copy = [
        ("dist/AzGelir.exe", "AzGelir.exe"),
        ("logo.png", "logo.png"),
        ("README_Windows.md", "README.md"),
        ("LICENSE.txt", "LICENSE.txt")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(portable_dir, dst))
            print(f"✓ {dst} kopyalandı")
    
    # Portable başlatıcı
    batch_content = """@echo off
chcp 65001 >nul
title AzGelir Portable

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        AzGelir Portable                       ║
echo ║               Gelir/Gider Takip Uygulaması                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if not exist "records.db" (
    echo İlk çalıştırma - Veritabanı oluşturuluyor...
)

echo AzGelir başlatılıyor...
start "" "AzGelir.exe"

if errorlevel 1 (
    echo.
    echo HATA: Uygulama başlatılamadı!
    echo.
    pause
) else (
    echo ✓ Uygulama başlatıldı
    timeout /t 2 /nobreak >nul
)
"""
    
    with open(os.path.join(portable_dir, "AzGelir_Baslat.bat"), "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    # Portable README
    portable_readme = """# AzGelir Portable Sürüm

## Kullanım
1. `AzGelir_Baslat.bat` dosyasını çalıştırın
2. Veya doğrudan `AzGelir.exe` dosyasını çalıştırın

## Özellikler
- Kurulum gerektirmez
- USB bellekte taşınabilir
- Sistem kayıtlarını değiştirmez
- Veriler aynı klasörde saklanır

## Sistem Gereksinimleri
- Windows 7 SP1 veya üzeri
- .NET Framework 4.6.1 veya üzeri

Tüm veriler bu klasörde tutulur. Klasörü kopyalayarak 
uygulamayı başka bilgisayarlara taşıyabilirsiniz.
"""
    
    with open(os.path.join(portable_dir, "PORTABLE_README.txt"), "w", encoding="utf-8") as f:
        f.write(portable_readme)
    
    # ZIP arşivi oluştur
    try:
        shutil.make_archive("AzGelir_Portable", "zip", portable_dir)
        print("✓ Portable ZIP arşivi oluşturuldu")
    except Exception as e:
        print(f"⚠️ ZIP oluşturma hatası: {e}")
    
    print("✅ Portable sürüm hazır!")
    return True

def build_chocolatey():
    """Chocolatey paket scripti oluştur"""
    print("\n🍫 Chocolatey paket scripti oluşturuluyor...")
    
    choco_dir = "chocolatey"
    if os.path.exists(choco_dir):
        shutil.rmtree(choco_dir)
    
    os.makedirs(f"{choco_dir}/tools")
    
    # Chocolatey nuspec dosyası
    nuspec_content = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <id>azgelir</id>
    <version>1.0.0</version>
    <packageSourceUrl>https://github.com/Tamerefe/AzGelir</packageSourceUrl>
    <owners>Tamerefe</owners>
    <title>AzGelir</title>
    <authors>Tamerefe</authors>
    <projectUrl>https://github.com/Tamerefe/AzGelir</projectUrl>
    <licenseUrl>https://github.com/Tamerefe/AzGelir/blob/main/LICENSE</licenseUrl>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <projectSourceUrl>https://github.com/Tamerefe/AzGelir</projectSourceUrl>
    <tags>finance accounting income expense tracking turkish</tags>
    <summary>Gelir ve Gider Takip Uygulaması</summary>
    <description>
AzGelir, PyQt5 kullanılarak geliştirilmiş modern bir gelir/gider takip sistemidir. 
Muhasebe odaklı, erişilebilir ve kullanıcı dostu arayüzü ile finansal kayıtlarınızı 
kolayca takip edebilirsiniz.

## Özellikler
- Gelir ve gider kayıtları
- KDV hesaplama (%1, %10, %18)  
- Tarih aralığı filtresi
- CSV dışa aktarma
- SQLite veritabanı
- Modern ve responsive arayüz

## Kullanım
Kurulumdan sonra Başlat menüsünden "AzGelir" uygulamasını arayın.
    </description>
    <releaseNotes>İlk sürüm</releaseNotes>
  </metadata>
  <files>
    <file src="tools\\**" target="tools" />
  </files>
</package>"""
    
    with open(f"{choco_dir}/azgelir.nuspec", "w", encoding="utf-8") as f:
        f.write(nuspec_content)
    
    # Chocolatey install script
    install_script = """$ErrorActionPreference = 'Stop'
$toolsDir = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$packageName = 'azgelir'
$url = 'https://github.com/Tamerefe/AzGelir/releases/download/v1.0.0/AzGelir_Setup.exe'

$packageArgs = @{
  packageName   = $packageName
  unzipLocation = $toolsDir
  fileType      = 'EXE'
  url           = $url
  silentArgs    = '/S'
  validExitCodes= @(0)
  softwareName  = 'AzGelir*'
  checksum      = ''
  checksumType  = 'sha256'
}

Install-ChocolateyPackage @packageArgs"""
    
    with open(f"{choco_dir}/tools/chocolateyinstall.ps1", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    # Chocolatey uninstall script
    uninstall_script = """$ErrorActionPreference = 'Stop'
$packageArgs = @{
  packageName = 'azgelir'
  softwareName = 'AzGelir*'
  fileType = 'EXE'
  silentArgs = '/S'
  validExitCodes = @(0)
}

$uninstalled = $false
[array]$key = Get-UninstallRegistryKey -SoftwareName $packageArgs['softwareName']

if ($key.Count -eq 1) {
  $key | % { 
    $packageArgs['file'] = "$($_.UninstallString)"
    if ($packageArgs['fileType'] -eq 'MSI') {
      $packageArgs['silentArgs'] = "$($_.PSChildName) $($packageArgs['silentArgs'])"
      $packageArgs['file'] = ''
    }
    Uninstall-ChocolateyPackage @packageArgs
  }
} elseif ($key.Count -eq 0) {
  Write-Warning "$packageName has already been uninstalled by other means."
} elseif ($key.Count -gt 1) {
  Write-Warning "$($key.Count) matches found!"
  Write-Warning "To prevent accidental data loss, no programs will be uninstalled."
  Write-Warning "Please alert package maintainer the following keys were matched:"
  $key | % {Write-Warning "- $($_.DisplayName)"}
}"""
    
    with open(f"{choco_dir}/tools/chocolateyuninstall.ps1", "w", encoding="utf-8") as f:
        f.write(uninstall_script)
    
    print("✅ Chocolatey paket scripti oluşturuldu!")
    print("📋 Chocolatey'e yayınlamak için:")
    print(f"   cd {choco_dir}")
    print("   choco pack")
    print("   choco push azgelir.1.0.0.nupkg --source https://push.chocolatey.org/")
    
    return True

def create_distribution_readme():
    """Dağıtım README'si oluştur"""
    readme_content = """# AzGelir - Windows Dağıtım Paketleri

Bu dizin, AzGelir uygulamasının farklı Windows paket formatlarını içerir.

## 📦 Paket Formatları

### 1. Windows Executable (dist/)
- **Dosya**: `dist/AzGelir.exe`
- **Kullanım**: Doğrudan çalıştırılabilir
- **Kurulum**: `install.ps1` ile otomatik kurulum
- **Avantajlar**: Tek dosya, hızlı

### 2. MSI Installer
- **Dosya**: `AzGelir_Setup.msi`
- **Kullanım**: Windows Installer teknolojisi
- **Kurulum**: Çift tıklayın veya `msiexec /i`
- **Avantajlar**: Enterprise dağıtım, otomatik kaldırma

### 3. NSIS Installer
- **Dosya**: `AzGelir_Setup.exe`
- **Kullanım**: Geleneksel Windows installer
- **Kurulum**: Çift tıklayın
- **Avantajlar**: Özelleştirilebilir UI, küçük boyut

### 4. Portable Sürüm
- **Dosya**: `AzGelir_Portable.zip`
- **Kullanım**: Sıkıştırılmış dosyayı açın
- **Kurulum**: Kurulum gerektirmez
- **Avantajlar**: USB taşınabilir, sistem değişikliği yok

### 5. Chocolatey Paketi
- **Dizin**: `chocolatey/`
- **Kullanım**: `choco install azgelir`
- **Kurulum**: Chocolatey package manager
- **Avantajlar**: Otomatik güncelleme, bağımlılık yönetimi

## 🚀 Hızlı Başlangıç

### En Kolay: Portable Sürüm
```
1. AzGelir_Portable.zip dosyasını indirin
2. Klasöre çıkartın
3. AzGelir_Baslat.bat dosyasını çalıştırın
```

### En Yaygın: NSIS Installer
```
1. AzGelir_Setup.exe dosyasını çalıştırın
2. Kurulum sihirbazını takip edin
3. Masaüstü kısayolundan başlatın
```

### Enterprise: MSI Installer
```
msiexec /i AzGelir_Setup.msi /quiet
```

### Chocolatey Kullanıcıları:
```powershell
choco install azgelir
```

## 📋 Sistem Gereksinimleri

### Minimum:
- Windows 7 SP1 / Windows Server 2008 R2 SP1
- .NET Framework 4.6.1
- 512 MB RAM
- 100 MB disk alanı

### Önerilen:
- Windows 10 / Windows 11
- .NET Framework 4.8
- 1 GB RAM
- 200 MB disk alanı

## 🛠️ Geliştirici Bilgileri

### Build Gereksinimleri:
- Python 3.6+
- PyInstaller
- PyQt5
- pywin32

### MSI Build:
- WiX Toolset 3.11+

### NSIS Build:
- NSIS 3.08+

### Build Komutları:
```bash
# Tüm formatlar
python build_all_windows.py

# Sadece exe
python build_windows.py

# MSI installer
python build_msi.py

# Belirli format
python build_all_windows.py --format portable
```

## 🔧 Sorun Giderme

### Visual C++ Redistributable Eksik:
- https://aka.ms/vs/17/release/vc_redist.x64.exe

### .NET Framework Eksik:
- https://dotnet.microsoft.com/download/dotnet-framework

### Windows Defender Uyarısı:
1. Windows Security > Virus & threat protection
2. Manage settings > Add or remove exclusions
3. Add an exclusion > File > AzGelir.exe

## 📞 Destek

- **GitHub**: https://github.com/Tamerefe/AzGelir
- **Issues**: Sorunlar için GitHub'da issue açın
- **Wiki**: Detaylı dokümantasyon

## 📄 Lisans

MIT License - Detaylar için LICENSE.txt dosyasını inceleyin.
"""
    
    with open("README_Distribution_Windows.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Windows dağıtım README'si oluşturuldu")

def show_summary():
    """Oluşturulan dosyaların özetini göster"""
    print("\n🎉 Windows paketleme tamamlandı!")
    print("=" * 50)
    
    # Dosya listesi ve boyutları
    files_to_check = [
        ("dist/AzGelir.exe", "Windows Executable"),
        ("AzGelir_Setup.msi", "MSI Installer"),
        ("AzGelir_Setup.exe", "NSIS Installer"),
        ("AzGelir_Portable.zip", "Portable ZIP"),
        ("chocolatey/azgelir.nuspec", "Chocolatey Package")
    ]
    
    print("\n📦 Oluşturulan paketler:")
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            if file_path.endswith(('.exe', '.msi', '.zip')):
                size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"   ✅ {description}: {file_path} ({size:.1f} MB)")
            else:
                print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} (oluşturulamadı)")
    
    print("\n📋 Dağıtım rehberi: README_Distribution_Windows.md")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description="AzGelir Windows Paketleme Aracı")
    parser.add_argument("--format", 
                       choices=["exe", "msi", "nsis", "portable", "chocolatey", "all"],
                       default="all", 
                       help="Paket formatı seçin")
    parser.add_argument("--no-deps", action="store_true", 
                       help="Bağımlılık kurulumunu atla")
    
    args = parser.parse_args()
    
    print_banner()
    check_python_version()
    
    if not args.no_deps:
        install_dependencies()
    
    success_count = 0
    total_count = 0
    
    # Ana exe dosyası her zaman gerekli
    if args.format != "chocolatey":
        total_count += 1
        if build_executable():
            success_count += 1
        else:
            print("❌ Exe oluşturulamadığı için diğer paketler oluşturulamaz!")
            sys.exit(1)
    
    if args.format in ["msi", "all"]:
        total_count += 1
        if build_msi():
            success_count += 1
    
    if args.format in ["nsis", "all"]:
        total_count += 1
        if build_nsis():
            success_count += 1
    
    if args.format in ["portable", "all"]:
        total_count += 1
        if build_portable():
            success_count += 1
    
    if args.format in ["chocolatey", "all"]:
        total_count += 1
        if build_chocolatey():
            success_count += 1
    
    # Dağıtım README'si oluştur
    create_distribution_readme()
    
    # Özet göster
    show_summary()
    
    print(f"\n✅ Başarılı: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🚀 Tüm Windows paketleri başarıyla oluşturuldu!")
    else:
        print("⚠️ Bazı paketlerde sorun oluştu. Detaylar için yukarıdaki logları inceleyin.")

if __name__ == "__main__":
    main()
