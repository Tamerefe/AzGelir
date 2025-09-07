#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows için PyInstaller build scripti
AzGelir uygulamasını Windows .exe dosyası olarak paketler
"""

import os
import subprocess
import sys
import shutil
import winreg
from pathlib import Path

def check_dependencies():
    """Gerekli bağımlılıkları kontrol et"""
    try:
        import PyInstaller
        print("✓ PyInstaller bulundu")
    except ImportError:
        print("✗ PyInstaller bulunamadı. Yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller yüklendi")

def check_upx():
    """UPX sıkıştırıcısını kontrol et"""
    try:
        result = subprocess.run(["upx", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ UPX bulundu (dosya boyutu küçültülecek)")
            return True
    except FileNotFoundError:
        pass
    
    print("ℹ️ UPX bulunamadı (dosya boyutu optimizasyonu yapılamayacak)")
    print("   UPX indirmek için: https://upx.github.io/")
    return False

def clean_build():
    """Önceki build dosyalarını temizle"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ {dir_name} temizlendi")
    
    # .spec dosyalarını temizle
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✓ {spec_file} temizlendi")

def build_application(use_upx=False):
    """Uygulamayı paketle"""
    print("🚀 Windows için uygulama paketleniyor...")
    
    # PyInstaller komut parametreleri
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tek dosya halinde paketleme
        "--windowed",                   # GUI uygulaması (console gizle)
        "--name=AzGelir",              # Uygulama adı
        "--icon=logo.png",             # Uygulama ikonu
        "--add-data=logo.png;.",       # Logo dosyasını dahil et (Windows için ; kullan)
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=sqlite3",
        "--hidden-import=csv",
        "--clean",                     # Önceki build'i temizle
        "--optimize=2",                # Python optimizasyonu
    ]
    
    # Veritabanı dosyası varsa ekle
    if os.path.exists("records.db"):
        cmd.append("--add-data=records.db;.")
    
    # UPX kullan
    if use_upx:
        cmd.append("--upx-dir=.")
    
    cmd.append("main.py")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Paketleme başarılı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paketleme hatası: {e}")
        return False

def create_shortcut():
    """Masaüstü kısayolu oluştur"""
    try:
        import win32com.client
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "AzGelir.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.abspath("dist/AzGelir.exe")
        shortcut.WorkingDirectory = os.path.abspath("dist")
        shortcut.IconLocation = os.path.abspath("dist/AzGelir.exe")
        shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
        shortcut.save()
        
        print("✓ Masaüstü kısayolu oluşturuldu")
        return True
    except ImportError:
        print("⚠️ pywin32 bulunamadı, kısayol oluşturulamadı")
        print("   Yüklemek için: pip install pywin32")
        return False
    except Exception as e:
        print(f"⚠️ Kısayol oluşturma hatası: {e}")
        return False

def create_installer_script():
    """NSIS installer scripti oluştur"""
    installer_script = """
; AzGelir Windows Installer Script (NSIS)
; Modern UI kullanır

!include "MUI2.nsh"

; Program bilgileri
!define PRODUCT_NAME "AzGelir"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Tamerefe"
!define PRODUCT_WEB_SITE "https://github.com/Tamerefe/AzGelir"
!define PRODUCT_DIR_REGKEY "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\AzGelir.exe"
!define PRODUCT_UNINST_KEY "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}"

; Installer ayarları
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "AzGelir_Setup.exe"
InstallDir "$PROGRAMFILES\\${PRODUCT_NAME}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

; Modern UI ayarları
!define MUI_ABORTWARNING
!define MUI_ICON "logo.ico"
!define MUI_UNICON "logo.ico"

; Sayfalar
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Diller
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "English"

; Ana bölüm
Section "AzGelir (Gerekli)" SEC01
  SectionIn RO
  SetOutPath "$INSTDIR"
  File "dist\\AzGelir.exe"
  File "logo.png"
  
  ; Registry kayıtları
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\\AzGelir.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\\AzGelir.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  
  ; Uninstaller oluştur
  WriteUninstaller "$INSTDIR\\uninst.exe"
SectionEnd

; Masaüstü kısayolu
Section "Masaüstü Kısayolu" SEC02
  CreateShortCut "$DESKTOP\\AzGelir.lnk" "$INSTDIR\\AzGelir.exe"
SectionEnd

; Başlat Menüsü
Section "Başlat Menüsü Kısayolu" SEC03
  CreateDirectory "$SMPROGRAMS\\AzGelir"
  CreateShortCut "$SMPROGRAMS\\AzGelir\\AzGelir.lnk" "$INSTDIR\\AzGelir.exe"
  CreateShortCut "$SMPROGRAMS\\AzGelir\\Kaldır.lnk" "$INSTDIR\\uninst.exe"
SectionEnd

; Dosya uzantısı ilişkilendirme
Section "Dosya İlişkilendirme (.azg)" SEC04
  WriteRegStr HKCR ".azg" "" "AzGelir.Document"
  WriteRegStr HKCR "AzGelir.Document" "" "AzGelir Belgesi"
  WriteRegStr HKCR "AzGelir.Document\\DefaultIcon" "" "$INSTDIR\\AzGelir.exe,0"
  WriteRegStr HKCR "AzGelir.Document\\shell\\open\\command" "" '"$INSTDIR\\AzGelir.exe" "%1"'
SectionEnd

; Bölüm açıklamaları
LangString DESC_SEC01 ${LANG_TURKISH} "Ana uygulama dosyaları (gerekli)"
LangString DESC_SEC02 ${LANG_TURKISH} "Masaüstünde kısayol oluşturur"
LangString DESC_SEC03 ${LANG_TURKISH} "Başlat menüsünde kısayol oluşturur"
LangString DESC_SEC04 ${LANG_TURKISH} ".azg dosyalarını AzGelir ile ilişkilendirir"

LangString DESC_SEC01 ${LANG_ENGLISH} "Main application files (required)"
LangString DESC_SEC02 ${LANG_ENGLISH} "Create desktop shortcut"
LangString DESC_SEC03 ${LANG_ENGLISH} "Create start menu shortcuts"
LangString DESC_SEC04 ${LANG_ENGLISH} "Associate .azg files with AzGelir"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} $(DESC_SEC01)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} $(DESC_SEC02)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} $(DESC_SEC03)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} $(DESC_SEC04)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Kaldırıcı
Section Uninstall
  Delete "$INSTDIR\\AzGelir.exe"
  Delete "$INSTDIR\\logo.png"
  Delete "$INSTDIR\\uninst.exe"
  Delete "$DESKTOP\\AzGelir.lnk"
  Delete "$SMPROGRAMS\\AzGelir\\AzGelir.lnk"
  Delete "$SMPROGRAMS\\AzGelir\\Kaldır.lnk"
  RMDir "$SMPROGRAMS\\AzGelir"
  RMDir "$INSTDIR"

  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey HKCR ".azg"
  DeleteRegKey HKCR "AzGelir.Document"
SectionEnd
"""
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(installer_script)
    
    print("✓ NSIS installer scripti oluşturuldu")

def create_portable_batch():
    """Taşınabilir sürüm için batch dosyası oluştur"""
    batch_content = """@echo off
chcp 65001 >nul
title AzGelir - Gelir/Gider Takip Uygulaması

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        AzGelir                                ║
echo ║               Gelir/Gider Takip Uygulaması                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

:: Uygulama dizinine geç
cd /d "%~dp0"

:: Veritabanı dosyası var mı kontrol et
if not exist "records.db" (
    echo İlk çalıştırma tespit edildi...
    echo Veritabanı oluşturuluyor...
)

:: Uygulamayı başlat
echo AzGelir başlatılıyor...
start "" "AzGelir.exe"

:: Hata kontrolü
if errorlevel 1 (
    echo.
    echo HATA: Uygulama başlatılamadı!
    echo.
    echo Olası çözümler:
    echo - Windows Defender'da uygulama engellenmiş olabilir
    echo - Visual C++ Redistributable eksik olabilir
    echo - .NET Framework gerekli olabilir
    echo.
    pause
) else (
    echo ✓ Uygulama başlatıldı
    timeout /t 3 /nobreak >nul
)
"""
    
    with open("dist/AzGelir_Baslat.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ Portable başlatıcı batch dosyası oluşturuldu")

def create_powershell_installer():
    """PowerShell kurulum scripti oluştur"""
    ps_script = """# AzGelir Windows PowerShell Kurulum Scripti
# Yönetici ayrıcalıkları ile çalıştırın

param(
    [switch]$Uninstall,
    [switch]$Portable,
    [string]$InstallPath = "$env:ProgramFiles\\AzGelir"
)

# Renkli çıktı fonksiyonları
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }

# Banner
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║                   AzGelir Windows Kurulum                    ║" -ForegroundColor Blue
Write-Host "║                   Gelir/Gider Takip Uygulaması               ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Yönetici kontrolü
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Kaldırma fonksiyonu
function Uninstall-AzGelir {
    Write-Info "AzGelir kaldırılıyor..."
    
    # Programı durdur
    Get-Process -Name "AzGelir" -ErrorAction SilentlyContinue | Stop-Process -Force
    
    # Dosyaları kaldır
    if (Test-Path $InstallPath) {
        Remove-Item $InstallPath -Recurse -Force
        Write-Success "Program dosyaları kaldırıldı"
    }
    
    # Kısayolları kaldır
    $shortcuts = @(
        "$env:PUBLIC\\Desktop\\AzGelir.lnk",
        "$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir.lnk"
    )
    
    foreach ($shortcut in $shortcuts) {
        if (Test-Path $shortcut) {
            Remove-Item $shortcut -Force
            Write-Success "Kısayol kaldırıldı: $(Split-Path $shortcut -Leaf)"
        }
    }
    
    # Registry temizle
    $regPaths = @(
        "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir",
        "HKLM:\\SOFTWARE\\Classes\\.azg",
        "HKLM:\\SOFTWARE\\Classes\\AzGelir.Document"
    )
    
    foreach ($regPath in $regPaths) {
        if (Test-Path $regPath) {
            Remove-Item $regPath -Recurse -Force
            Write-Success "Registry temizlendi: $regPath"
        }
    }
    
    Write-Success "AzGelir başarıyla kaldırıldı!"
}

# Kurulum fonksiyonu
function Install-AzGelir {
    Write-Info "AzGelir kuruluyor..."
    
    # Kurulum dizini oluştur
    if (-not (Test-Path $InstallPath)) {
        New-Item $InstallPath -ItemType Directory -Force | Out-Null
        Write-Success "Kurulum dizini oluşturuldu: $InstallPath"
    }
    
    # Dosyaları kopyala
    if (Test-Path "AzGelir.exe") {
        Copy-Item "AzGelir.exe" $InstallPath -Force
        Write-Success "Ana uygulama kopyalandı"
    } else {
        Write-Error "AzGelir.exe bulunamadı!"
        return $false
    }
    
    if (Test-Path "logo.png") {
        Copy-Item "logo.png" $InstallPath -Force
        Write-Success "Logo dosyası kopyalandı"
    }
    
    # Masaüstü kısayolu
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut("$env:PUBLIC\\Desktop\\AzGelir.lnk")
    $shortcut.TargetPath = "$InstallPath\\AzGelir.exe"
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
    $shortcut.Save()
    Write-Success "Masaüstü kısayolu oluşturuldu"
    
    # Başlat menüsü kısayolu
    $startMenuShortcut = $WScriptShell.CreateShortcut("$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir.lnk")
    $startMenuShortcut.TargetPath = "$InstallPath\\AzGelir.exe"
    $startMenuShortcut.WorkingDirectory = $InstallPath
    $startMenuShortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
    $startMenuShortcut.Save()
    Write-Success "Başlat menüsü kısayolu oluşturuldu"
    
    # Registry kayıtları
    New-Item "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Force | Out-Null
    Set-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Name "DisplayName" -Value "AzGelir"
    Set-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Name "DisplayVersion" -Value "1.0.0"
    Set-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Name "Publisher" -Value "Tamerefe"
    Set-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Name "InstallLocation" -Value $InstallPath
    Set-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File \\"$InstallPath\\uninstall.ps1\\""
    Write-Success "Registry kayıtları oluşturuldu"
    
    # Kaldırma scripti oluştur
    $uninstallScript = @"
# AzGelir Kaldırma Scripti
Write-Host "AzGelir kaldırılıyor..." -ForegroundColor Yellow
& "$PSScriptRoot\\install.ps1" -Uninstall
Write-Host "Kaldırma tamamlandı!" -ForegroundColor Green
pause
"@
    $uninstallScript | Out-File "$InstallPath\\uninstall.ps1" -Encoding UTF8
    
    Write-Success "AzGelir başarıyla kuruldu!"
    Write-Info "Masaüstü kısayolundan veya Başlat menüsünden çalıştırabilirsiniz."
}

# Portable kurulum
function Install-Portable {
    Write-Info "Portable sürüm hazırlanıyor..."
    
    $portableDir = "AzGelir_Portable"
    if (-not (Test-Path $portableDir)) {
        New-Item $portableDir -ItemType Directory | Out-Null
    }
    
    # Dosyaları kopyala
    Copy-Item "AzGelir.exe" $portableDir -Force
    if (Test-Path "logo.png") {
        Copy-Item "logo.png" $portableDir -Force
    }
    
    # Portable batch dosyası
    $batchContent = @"
@echo off
title AzGelir Portable
cd /d "%~dp0"
start "" "AzGelir.exe"
"@
    $batchContent | Out-File "$portableDir\\AzGelir_Baslat.bat" -Encoding ASCII
    
    # README
    $readmeContent = @"
# AzGelir Portable Sürüm

Bu portable sürümdür. Kurulum gerektirmez.

## Kullanım:
- AzGelir_Baslat.bat dosyasını çalıştırın
- Veya doğrudan AzGelir.exe dosyasını çalıştırın

## Özellikler:
- Kurulum gerektirmez
- USB bellekte taşınabilir
- Sistem kayıtlarını değiştirmez
- Veriler aynı klasörde saklanır

Tüm veriler bu klasörde tutulur.
"@
    $readmeContent | Out-File "$portableDir\\README.txt" -Encoding UTF8
    
    Write-Success "Portable sürüm hazır: $portableDir"
}

# Ana işlem
if ($Uninstall) {
    if (-not (Test-Administrator)) {
        Write-Error "Kaldırma işlemi için yönetici ayrıcalıkları gerekli!"
        Write-Info "PowerShell'i yönetici olarak çalıştırın ve tekrar deneyin."
        pause
        exit 1
    }
    Uninstall-AzGelir
} elseif ($Portable) {
    Install-Portable
} else {
    if (-not (Test-Administrator)) {
        Write-Error "Kurulum için yönetici ayrıcalıkları gerekli!"
        Write-Info "PowerShell'i yönetici olarak çalıştırın ve tekrar deneyin."
        Write-Info "Veya portable sürüm için: .\\install.ps1 -Portable"
        pause
        exit 1
    }
    Install-AzGelir
}

Write-Info "İşlem tamamlandı!"
pause
"""
    
    with open("dist/install.ps1", "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    print("✓ PowerShell kurulum scripti oluşturuldu")

def create_windows_readme():
    """Windows README dosyası oluştur"""
    readme_content = """# AzGelir - Windows Sürümü

## 💾 Kurulum Seçenekleri

### 1. 🚀 Hızlı Kurulum (Önerilen)
```powershell
# PowerShell'i yönetici olarak çalıştırın
.\\install.ps1
```

### 2. 📦 NSIS Installer (Gelecekte)
```
AzGelir_Setup.exe dosyasını çalıştırın
```

### 3. 🎒 Portable Sürüm
```powershell
.\\install.ps1 -Portable
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
.\\install.ps1 -Uninstall
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
%PROGRAMFILES%\\AzGelir\\
```

### Portable Sürüm:
Uygulama klasörünün içinde

### Kullanıcı Verileri:
```
%APPDATA%\\AzGelir\\
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
"""
    
    with open("README_Windows.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ Windows README dosyası oluşturuldu")

def create_license_file():
    """MIT License dosyası oluştur"""
    license_content = """MIT License

Copyright (c) 2025 Tamerefe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open("LICENSE.txt", "w", encoding="utf-8") as f:
        f.write(license_content)
    
    print("✓ LICENSE.txt dosyası oluşturuldu")

def get_file_info():
    """Oluşturulan exe hakkında bilgi göster"""
    exe_path = "dist/AzGelir.exe"
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n📦 Windows uygulaması: {exe_path}")
        print(f"📏 Dosya boyutu: {size:.1f} MB")
        
        # Dosya versiyonu ve bilgileri (eğer mümkünse)
        try:
            import win32api
            info = win32api.GetFileVersionInfo(exe_path, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
            print(f"📋 Versiyon: {version}")
        except:
            pass

def main():
    """Ana fonksiyon"""
    print("🪟 Windows için AzGelir Paketleme Aracı")
    print("=" * 45)
    
    # Gerekli araçları kontrol et
    check_dependencies()
    has_upx = check_upx()
    
    # Temizlik
    clean_build()
    
    # UPX kullanım seçeneği
    use_upx = False
    if has_upx:
        response = input("\nUPX sıkıştırması kullanılsın mı? (dosya boyutunu küçültür) (y/N): ").lower()
        use_upx = response in ['y', 'yes', 'evet']
    
    # Exe oluştur
    if not build_application(use_upx):
        print("❌ Build başarısız!")
        sys.exit(1)
    
    # Ek dosyalar oluştur
    create_portable_batch()
    create_powershell_installer()
    create_installer_script()
    create_windows_readme()
    create_license_file()
    
    # Kısayol oluşturmayı dene
    create_shortcut()
    
    # Bilgileri göster
    get_file_info()
    
    print("\n🎉 Windows paketleme tamamlandı!")
    print(f"📦 Exe dosyası: {os.path.abspath('dist/AzGelir.exe')}")
    print("\n📋 Dağıtım için hazır dosyalar:")
    print("   • dist/AzGelir.exe (ana uygulama)")
    print("   • dist/AzGelir_Baslat.bat (portable başlatıcı)")
    print("   • dist/install.ps1 (PowerShell kurulum)")
    print("   • installer.nsi (NSIS installer script)")
    print("   • README_Windows.md (kullanım kılavuzu)")
    print("   • LICENSE.txt (lisans dosyası)")

if __name__ == "__main__":
    main()
