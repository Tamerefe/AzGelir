# AzGelir Windows PowerShell Kurulum Scripti
# Yönetici ayrıcalıkları ile çalıştırın

param(
    [switch]$Uninstall,
    [switch]$Portable,
    [string]$InstallPath = "$env:ProgramFiles\AzGelir"
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
        "$env:PUBLIC\Desktop\AzGelir.lnk",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\AzGelir.lnk"
    )
    
    foreach ($shortcut in $shortcuts) {
        if (Test-Path $shortcut) {
            Remove-Item $shortcut -Force
            Write-Success "Kısayol kaldırıldı: $(Split-Path $shortcut -Leaf)"
        }
    }
    
    # Registry temizle
    $regPaths = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir",
        "HKLM:\SOFTWARE\Classes\.azg",
        "HKLM:\SOFTWARE\Classes\AzGelir.Document"
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
    $shortcut = $WScriptShell.CreateShortcut("$env:PUBLIC\Desktop\AzGelir.lnk")
    $shortcut.TargetPath = "$InstallPath\AzGelir.exe"
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
    $shortcut.Save()
    Write-Success "Masaüstü kısayolu oluşturuldu"
    
    # Başlat menüsü kısayolu
    $startMenuShortcut = $WScriptShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\AzGelir.lnk")
    $startMenuShortcut.TargetPath = "$InstallPath\AzGelir.exe"
    $startMenuShortcut.WorkingDirectory = $InstallPath
    $startMenuShortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
    $startMenuShortcut.Save()
    Write-Success "Başlat menüsü kısayolu oluşturuldu"
    
    # Registry kayıtları
    New-Item "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Force | Out-Null
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Name "DisplayName" -Value "AzGelir"
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Name "DisplayVersion" -Value "1.0.0"
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Name "Publisher" -Value "Tamerefe"
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Name "InstallLocation" -Value $InstallPath
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AzGelir" -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File \"$InstallPath\uninstall.ps1\""
    Write-Success "Registry kayıtları oluşturuldu"
    
    # Kaldırma scripti oluştur
    $uninstallScript = @"
# AzGelir Kaldırma Scripti
Write-Host "AzGelir kaldırılıyor..." -ForegroundColor Yellow
& "$PSScriptRoot\install.ps1" -Uninstall
Write-Host "Kaldırma tamamlandı!" -ForegroundColor Green
pause
"@
    $uninstallScript | Out-File "$InstallPath\uninstall.ps1" -Encoding UTF8
    
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
    $batchContent | Out-File "$portableDir\AzGelir_Baslat.bat" -Encoding ASCII
    
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
    $readmeContent | Out-File "$portableDir\README.txt" -Encoding UTF8
    
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
        Write-Info "Veya portable sürüm için: .\install.ps1 -Portable"
        pause
        exit 1
    }
    Install-AzGelir
}

Write-Info "İşlem tamamlandı!"
pause
