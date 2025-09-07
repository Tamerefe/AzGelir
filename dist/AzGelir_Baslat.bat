@echo off
chcp 65001 >nul
title AzGelir - Gelir/Gider Takip Uygulaması

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        AzGelir                                ║
echo ║               Gelir/Gider Takip Uygulaması                    ║
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
