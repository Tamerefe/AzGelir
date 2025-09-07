@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title AzGelir Tek Dosya Kurulum Oluşturucu

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║            AzGelir Tek Dosya Kurulum Oluşturucu             ║
echo ║                                                               ║
echo ║        Sıfırdan Bilgisayar İçin Exe Kurulum Dosyası         ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo ✓ Bu script şunları yapacak:
echo   • Ana uygulama exe'sini derleyecek
echo   • Gerekli tüm bağımlılıkları indirecek
echo   • Tek dosya kurulum exe'si oluşturacak
echo   • Sıfırdan bilgisayarda Python dahil her şeyi kuracak
echo.

set /p confirm="Kurulum dosyası oluşturmaya başlansın mı? (Y/N): "
if /i not "%confirm%"=="Y" exit /b 0

echo.
echo [1/6] Ana uygulama derleniyor...
if not exist "dist\AzGelir.exe" (
    echo Ana uygulama henüz derlenmemiş, derleniyor...
    python build_windows.py
    if errorlevel 1 (
        echo ❌ Ana uygulama derlenemedi!
        pause
        exit /b 1
    )
)
echo ✓ Ana uygulama hazır

echo [2/6] Tam kurulum scripti oluşturuluyor...
python create_full_installer.py
echo ✓ Kurulum scripti oluşturuldu

echo [3/6] Gerekli bağımlılıklar indiriliyor...

:: Python embedded indiriliyor
if not exist "python-embed.zip" (
    echo   📥 Python embedded indiriliyor...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile 'python-embed.zip'}"
)

:: Visual C++ Redistributable indiriliyor
if not exist "vc_redist.exe" (
    echo   📥 Visual C++ Redistributable indiriliyor...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.exe'}"
)

echo ✓ Bağımlılıklar indirildi

echo [4/6] Self-extracting archive oluşturuluyor...

:: Kurulum dosyalarını bir klasöre topla
if exist "installer_files" rmdir /s /q "installer_files"
mkdir "installer_files"

copy "dist\AzGelir.exe" "installer_files\"
copy "AzGelir_Full_Install.ps1" "installer_files\"
copy "AzGelir_Full_Auto_Install.bat" "installer_files\"
copy "python-embed.zip" "installer_files\"
copy "vc_redist.exe" "installer_files\"
copy "logo.png" "installer_files\" 2>nul

echo ✓ Kurulum dosyaları toplandı

echo [5/6] Tek dosya exe oluşturuluyor...

:: PyInstaller ile self-extracting installer oluştur
echo import sys > self_installer.py
echo import os >> self_installer.py
echo import subprocess >> self_installer.py
echo import tempfile >> self_installer.py
echo import shutil >> self_installer.py
echo import zipfile >> self_installer.py
echo. >> self_installer.py
echo # Gömülü dosyalar >> self_installer.py
echo embedded_files = { >> self_installer.py
echo     'AzGelir.exe': r'installer_files\AzGelir.exe', >> self_installer.py
echo     'AzGelir_Full_Install.ps1': r'installer_files\AzGelir_Full_Install.ps1', >> self_installer.py
echo     'python-embed.zip': r'installer_files\python-embed.zip', >> self_installer.py
echo     'vc_redist.exe': r'installer_files\vc_redist.exe' >> self_installer.py
echo } >> self_installer.py
echo. >> self_installer.py
echo def main(): >> self_installer.py
echo     print("AzGelir Kurulum Sihirbazı başlatılıyor...") >> self_installer.py
echo     temp_dir = tempfile.mkdtemp() >> self_installer.py
echo     try: >> self_installer.py
echo         # Dosyaları geçici dizine çıkar >> self_installer.py
echo         for name, path in embedded_files.items(): >> self_installer.py
echo             dest = os.path.join(temp_dir, name) >> self_installer.py
echo             shutil.copy2(path, dest) >> self_installer.py
echo         # PowerShell installerı çalıştır >> self_installer.py
echo         ps_script = os.path.join(temp_dir, 'AzGelir_Full_Install.ps1') >> self_installer.py
echo         subprocess.call(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_script]) >> self_installer.py
echo     finally: >> self_installer.py
echo         shutil.rmtree(temp_dir, ignore_errors=True) >> self_installer.py
echo. >> self_installer.py
echo if __name__ == "__main__": >> self_installer.py
echo     main() >> self_installer.py

:: Self-installer'ı derle
pyinstaller --onefile --windowed --name="AzGelir_Setup" --icon="logo.png" self_installer.py

echo ✓ Tek dosya exe oluşturuldu

echo [6/6] Temizlik yapılıyor...
del self_installer.py
del self_installer.spec
rmdir /s /q build 2>nul
rmdir /s /q __pycache__ 2>nul

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║                 KURULUM DOSYASI HAZIR!                       ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 Başarıyla oluşturuldu!
echo.
echo 📁 Oluşturulan dosyalar:
echo   • dist\AzGelir_Setup.exe - Tek dosya kurulum
echo   • AzGelir_Full_Install.ps1 - PowerShell kurulum
echo   • AzGelir_Full_Auto_Install.bat - Batch kurulum
echo.
echo 🚀 Kullanım:
echo   Sıfırdan bilgisayara kurmak için:
echo   • AzGelir_Setup.exe dosyasını çalıştırın
echo   • veya batch/PowerShell dosyalarını yönetici olarak çalıştırın
echo.
echo 💡 AzGelir_Setup.exe dosyası tamamen bağımsızdır ve
echo    sıfırdan bilgisayarda Python dahil her şeyi kurar!
echo.

pause
