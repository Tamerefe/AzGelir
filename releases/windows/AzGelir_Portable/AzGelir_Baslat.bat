@echo off
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
