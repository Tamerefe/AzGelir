@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: AzGelir Windows Kurulum Sihirbazı
:: Bu script, AzGelir uygulamasını otomatik olarak kurar ve paketler

title AzGelir Kurulum Sihirbazı

:: Renkli çıktı için ANSI kodları
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "PURPLE=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

:: Unicode karakterler
set "CHECK=✓"
set "CROSS=✗"
set "ARROW=→"
set "STAR=★"
set "INFO=ℹ"
set "WARNING=⚠"

:: Banner göster
call :show_banner

:: Ana menü
:main_menu
cls
call :show_banner
call :detect_system
call :show_menu

set /p choice="Seçiminizi yapın [1-9, 0=Çıkış]: "

if "%choice%"=="1" call :quick_install
if "%choice%"=="2" call :build_executable
if "%choice%"=="3" call :build_msi
if "%choice%"=="4" call :build_nsis
if "%choice%"=="5" call :build_portable
if "%choice%"=="6" call :build_chocolatey
if "%choice%"=="7" call :build_all_packages
if "%choice%"=="8" call :show_system_info
if "%choice%"=="9" call :uninstall_azgelir
if "%choice%"=="0" goto :exit_program

echo.
echo %RED%%CROSS% Geçersiz seçim! Lütfen 0-9 arasında bir değer girin.%NC%
timeout /t 2 /nobreak >nul
goto :main_menu

:: Banner fonksiyonu
:show_banner
echo.
echo %BLUE%╔═══════════════════════════════════════════════════════════════╗%NC%
echo %BLUE%║                                                               ║%NC%
echo %BLUE%║                    AzGelir Kurulum Sihirbazı                  ║%NC%
echo %BLUE%║                                                               ║%NC%
echo %BLUE%║                Gelir/Gider Takip Uygulaması                   ║%NC%
echo %BLUE%║                                                               ║%NC%
echo %BLUE%║                     Windows Kurulum Aracı                     ║%NC%
echo %BLUE%║                                                               ║%NC%
echo %BLUE%╚═══════════════════════════════════════════════════════════════╝%NC%
echo.
echo %CYAN%                         Versiyon 1.0.0%NC%
echo %CYAN%                      GitHub: Tamerefe/AzGelir%NC%
echo.
goto :eof

:: Menü göster
:show_menu
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo %WHITE%                        KURULUM SEÇENEKLERI%NC%
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo.
echo %GREEN%1^)%NC% %CYAN%Hızlı Kurulum%NC%          - Otomatik kurulum (Önerilen)
echo %GREEN%2^)%NC% %CYAN%Windows Executable%NC%     - Tek .exe dosyası oluştur
echo %GREEN%3^)%NC% %CYAN%MSI Installer%NC%          - Enterprise kurulum paketi
echo %GREEN%4^)%NC% %CYAN%NSIS Installer%NC%         - Geleneksel Windows installer
echo %GREEN%5^)%NC% %CYAN%Portable Sürüm%NC%         - Taşınabilir ZIP paketi
echo %GREEN%6^)%NC% %CYAN%Chocolatey Paketi%NC%      - Package manager paketi
echo %GREEN%7^)%NC% %CYAN%Tüm Paketler%NC%           - Tüm formatları oluştur
echo %GREEN%8^)%NC% %CYAN%Sistem Bilgisi%NC%         - Sistem uyumluluğunu kontrol et
echo %GREEN%9^)%NC% %CYAN%Kaldır%NC%                 - AzGelir'i kaldır
echo %RED%0^)%NC% %RED%Çıkış%NC%
echo.
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo.
goto :eof

:: Sistem tespiti
:detect_system
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
set ARCH=%PROCESSOR_ARCHITECTURE%
if "%ARCH%"=="AMD64" set ARCH=x64
if "%ARCH%"=="x86" set ARCH=x86

echo %INFO% Windows %VERSION% %ARCH% tespit edildi
goto :eof

:: Python kontrolü
:check_python
echo %ARROW% Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo %CROSS% Python bulunamadı! Lütfen Python 3.6+ yükleyin.
        echo %INFO% İndirme: https://www.python.org/downloads/
        set PYTHON_OK=false
        goto :eof
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

for /f "tokens=2" %%i in ('%PYTHON_CMD% --version') do set PYTHON_VERSION=%%i
echo %CHECK% Python %PYTHON_VERSION% bulundu
set PYTHON_OK=true
goto :eof

:: Pip kontrolü
:check_pip
echo %ARROW% Pip kontrol ediliyor...
%PYTHON_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %CROSS% Pip bulunamadı!
    set PIP_OK=false
) else (
    echo %CHECK% Pip bulundu
    set PIP_OK=true
)
goto :eof

:: Bağımlılıkları yükle
:install_dependencies
echo %ARROW% Python paketleri yükleniyor...

if exist requirements.txt (
    %PYTHON_CMD% -m pip install -r requirements.txt
) else (
    echo %WARNING% requirements.txt bulunamadı, temel paketler yükleniyor...
    %PYTHON_CMD% -m pip install PyQt5 pyinstaller pywin32
)

if errorlevel 1 (
    echo %CROSS% Paket yüklemesi başarısız!
    pause
    goto :main_menu
) else (
    echo %CHECK% Python paketleri yüklendi
)
goto :eof

:: Hızlı kurulum
:quick_install
cls
call :show_banner
echo %ARROW% Hızlı kurulum başlatılıyor...
echo.

call :check_python
if "%PYTHON_OK%"=="false" (
    echo %CROSS% Python gereksinimi karşılanmadı!
    pause
    goto :main_menu
)

call :check_pip
if "%PIP_OK%"=="false" (
    echo %CROSS% Pip gereksinimi karşılanmadı!
    pause
    goto :main_menu
)

call :install_dependencies

echo.
echo %ARROW% Windows executable oluşturuluyor...
%PYTHON_CMD% build_windows.py

if errorlevel 1 (
    echo %CROSS% Build başarısız!
    pause
    goto :main_menu
)

echo.
echo %ARROW% Kurulum tamamlanıyor...

:: PowerShell kurulum scriptini çalıştır
if exist "dist\install.ps1" (
    echo %INFO% PowerShell kurulum scripti çalıştırılıyor...
    powershell -ExecutionPolicy Bypass -File "dist\install.ps1"
) else (
    echo %WARNING% Kurulum scripti bulunamadı, manuel kurulum gerekli
)

call :show_completion_info
pause
goto :main_menu

:: Windows executable oluştur
:build_executable
cls
echo %ARROW% Windows executable oluşturuluyor...
call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_windows.py
if errorlevel 1 (
    echo %CROSS% Build başarısız!
) else (
    echo %CHECK% Windows executable oluşturuldu!
)
pause
goto :main_menu

:: MSI installer oluştur
:build_msi
cls
echo %ARROW% MSI installer oluşturuluyor...
call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_msi.py
if errorlevel 1 (
    echo %CROSS% MSI build başarısız!
    echo %INFO% WiX Toolset gerekli: https://wixtoolset.org/
) else (
    echo %CHECK% MSI installer oluşturuldu!
)
pause
goto :main_menu

:: NSIS installer oluştur
:build_nsis
cls
echo %ARROW% NSIS installer oluşturuluyor...

:: NSIS kontrol
where makensis >nul 2>&1
if errorlevel 1 (
    echo %WARNING% NSIS bulunamadı. NSI script oluşturulacak ancak derlenemeyecek.
    echo %INFO% NSIS indirmek için: https://nsis.sourceforge.io/
)

call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_all_windows.py --format nsis
if errorlevel 1 (
    echo %CROSS% NSIS build başarısız!
) else (
    echo %CHECK% NSIS installer oluşturuldu!
)
pause
goto :main_menu

:: Portable sürüm oluştur
:build_portable
cls
echo %ARROW% Portable sürüm oluşturuluyor...
call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_all_windows.py --format portable
if errorlevel 1 (
    echo %CROSS% Portable build başarısız!
) else (
    echo %CHECK% Portable sürüm oluşturuldu!
)
pause
goto :main_menu

:: Chocolatey paketi oluştur
:build_chocolatey
cls
echo %ARROW% Chocolatey paketi oluşturuluyor...
call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_all_windows.py --format chocolatey
if errorlevel 1 (
    echo %CROSS% Chocolatey build başarısız!
) else (
    echo %CHECK% Chocolatey paketi oluşturuldu!
)
pause
goto :main_menu

:: Tüm paketleri oluştur
:build_all_packages
cls
echo %ARROW% Tüm paket formatları oluşturuluyor...
call :check_python
if "%PYTHON_OK%"=="false" goto :main_menu

%PYTHON_CMD% build_all_windows.py
if errorlevel 1 (
    echo %CROSS% Bazı paketler başarısız oldu!
) else (
    echo %CHECK% Tüm paketler oluşturuldu!
)
pause
goto :main_menu

:: Sistem bilgilerini göster
:show_system_info
cls
call :show_banner
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo %WHITE%                           SİSTEM BİLGİSİ%NC%
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo.

call :detect_system
echo %CYAN%İşletim Sistemi:%NC% Windows %VERSION%
echo %CYAN%Mimari:%NC% %ARCH%
echo %CYAN%Kullanıcı:%NC% %USERNAME%
echo %CYAN%Bilgisayar:%NC% %COMPUTERNAME%

:: Bellek bilgisi
for /f "skip=1" %%p in ('wmic computersystem get TotalPhysicalMemory ^| findstr [0-9]') do set TOTAL_MEMORY=%%p
set /a TOTAL_MEMORY_MB=%TOTAL_MEMORY:~0,-6%
echo %CYAN%Toplam Bellek:%NC% %TOTAL_MEMORY_MB% MB

:: Python kontrolü
call :check_python
call :check_pip

:: PyQt5 kontrolü
echo %ARROW% PyQt5 kontrol ediliyor...
%PYTHON_CMD% -c "import PyQt5.QtWidgets" >nul 2>&1
if errorlevel 1 (
    echo %CROSS% PyQt5 bulunamadı
) else (
    echo %CHECK% PyQt5 bulundu
)

:: Disk alanı kontrolü
echo %ARROW% Disk alanı kontrol ediliyor...
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set FREE_SPACE=%%a
set FREE_SPACE=%FREE_SPACE:,=%
set /a FREE_SPACE_MB=%FREE_SPACE:~0,-6%
echo %CYAN%Kullanılabilir Disk Alanı:%NC% %FREE_SPACE_MB% MB

echo.
pause
goto :main_menu

:: Kaldırma işlemi
:uninstall_azgelir
cls
echo.
echo %WARNING% AzGelir kaldırılıyor...
echo.
set /p confirm="Emin misiniz? (y/N): "
if /i not "%confirm%"=="y" (
    echo %INFO% Kaldırma iptal edildi
    pause
    goto :main_menu
)

:: PowerShell kaldırma scriptini çalıştır
if exist "dist\install.ps1" (
    echo %INFO% PowerShell kaldırma scripti çalıştırılıyor...
    powershell -ExecutionPolicy Bypass -File "dist\install.ps1" -Uninstall
) else (
    echo %WARNING% Kaldırma scripti bulunamadı
)

:: Build dosyalarını temizle
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
del /q "*.spec" 2>nul
del /q "*.msi" 2>nul
del /q "*Setup.exe" 2>nul
del /q "*.zip" 2>nul

echo %CHECK% AzGelir kaldırıldı!
pause
goto :main_menu

:: Tamamlama bilgilerini göster
:show_completion_info
echo.
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo %WHITE%                       KURULUM TAMAMLANDI!%NC%
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
echo.
echo %GREEN%%STAR% AzGelir başarıyla kuruldu!%NC%
echo.
echo %CYAN%Kullanım seçenekleri:%NC%
echo   %GREEN%•%NC% Masaüstü kısayolundan çalıştırın
echo   %GREEN%•%NC% Başlat menüsünde "AzGelir" arayın
echo   %GREEN%•%NC% Doğrudan AzGelir.exe dosyasını çalıştırın
echo.
echo %CYAN%Kurulum konumu:%NC%
echo   %GREEN%•%NC% %YELLOW%^%PROGRAMFILES^%\AzGelir\%NC%
echo.
echo %CYAN%Destek:%NC%
echo   %GREEN%•%NC% GitHub: %YELLOW%https://github.com/Tamerefe/AzGelir%NC%
echo   %GREEN%•%NC% Issues: Sorunlar için GitHub'da issue açın
echo.
echo %WHITE%═══════════════════════════════════════════════════════════════%NC%
goto :eof

:: Çıkış
:exit_program
cls
echo.
echo %INFO% AzGelir Kurulum Sihirbazından çıkılıyor...
echo %CYAN%Teşekkürler! AzGelir kullandığınız için%NC%
echo.
timeout /t 2 /nobreak >nul
exit /b 0
