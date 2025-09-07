#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AppImage formatında Linux paketleme scripti
Taşınabilir Linux uygulaması oluşturur
"""

import os
import subprocess
import sys
import shutil
import urllib.request
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

def download_appimage_tool():
    """AppImage araçlarını indir"""
    appimage_tool_url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    
    if not os.path.exists("appimagetool-x86_64.AppImage"):
        print("📥 AppImage tool indiriliyor...")
        try:
            urllib.request.urlretrieve(appimage_tool_url, "appimagetool-x86_64.AppImage")
            os.chmod("appimagetool-x86_64.AppImage", 0o755)
            print("✓ AppImage tool indirildi")
        except Exception as e:
            print(f"❌ AppImage tool indirilemedi: {e}")
            return False
    else:
        print("✓ AppImage tool zaten mevcut")
    
    return True

def create_appdir_structure():
    """AppDir yapısını oluştur"""
    appdir = "AzGelir.AppDir"
    
    # Önceki AppDir'i temizle
    if os.path.exists(appdir):
        shutil.rmtree(appdir)
    
    # Dizin yapısını oluştur
    dirs = [
        f"{appdir}/usr/bin",
        f"{appdir}/usr/share/applications",
        f"{appdir}/usr/share/icons/hicolor/256x256/apps",
        f"{appdir}/usr/share/pixmaps"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✓ AppDir yapısı oluşturuldu")
    return appdir

def build_with_pyinstaller():
    """PyInstaller ile uygulamayı derle"""
    print("🔨 PyInstaller ile derleme...")
    
    cmd = [
        "pyinstaller",
        "--onedir",                     # Dizin halinde paketleme (AppImage için gerekli)
        "--windowed",                   # GUI uygulaması
        "--name=AzGelir",
        "--add-data=logo.png:.",
        "--add-data=records.db:." if os.path.exists("records.db") else "",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=sqlite3",
        "--hidden-import=csv",
        "--clean",
        "main.py"
    ]
    
    # Boş parametreleri filtrele
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.check_call(cmd)
        print("✓ PyInstaller derleme başarılı")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller derleme hatası: {e}")
        return False

def setup_appdir(appdir):
    """AppDir içeriğini hazırla"""
    print("📁 AppDir içeriği hazırlanıyor...")
    
    # Ana uygulamayı kopyala
    if os.path.exists("dist/AzGelir"):
        shutil.copytree("dist/AzGelir", f"{appdir}/usr/bin/AzGelir")
        print("✓ Uygulama dosyaları kopyalandı")
    else:
        print("❌ dist/AzGelir bulunamadı!")
        return False
    
    # AppRun dosyası oluştur
    apprun_content = """#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
cd "${HERE}/usr/bin/AzGelir"
exec "./AzGelir" "$@"
"""
    
    with open(f"{appdir}/AppRun", "w") as f:
        f.write(apprun_content)
    os.chmod(f"{appdir}/AppRun", 0o755)
    print("✓ AppRun oluşturuldu")
    
    # Desktop dosyası oluştur
    desktop_content = """[Desktop Entry]
Type=Application
Name=AzGelir
Comment=Gelir ve Gider Takip Uygulaması
Exec=AzGelir
Icon=azgelir
StartupWMClass=AzGelir
Categories=Office;Finance;
"""
    
    with open(f"{appdir}/AzGelir.desktop", "w") as f:
        f.write(desktop_content)
    
    with open(f"{appdir}/usr/share/applications/AzGelir.desktop", "w") as f:
        f.write(desktop_content)
    
    print("✓ Desktop dosyaları oluşturuldu")
    
    # İkon dosyasını kopyala
    if os.path.exists("logo.png"):
        shutil.copy2("logo.png", f"{appdir}/azgelir.png")
        shutil.copy2("logo.png", f"{appdir}/usr/share/pixmaps/azgelir.png")
        shutil.copy2("logo.png", f"{appdir}/usr/share/icons/hicolor/256x256/apps/azgelir.png")
        print("✓ İkon dosyaları kopyalandı")
    
    return True

def build_appimage(appdir):
    """AppImage oluştur"""
    print("📦 AppImage oluşturuluyor...")
    
    try:
        subprocess.check_call([
            "./appimagetool-x86_64.AppImage",
            appdir,
            "AzGelir-x86_64.AppImage"
        ])
        print("✅ AppImage başarıyla oluşturuldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ AppImage oluşturma hatası: {e}")
        return False

def create_appimage_readme():
    """AppImage README dosyası oluştur"""
    readme_content = """# AzGelir - AppImage Sürümü

## Kullanım

AppImage taşınabilir bir uygulama formatıdır. Kurulum gerektirmez.

### Çalıştırma:
```bash
chmod +x AzGelir-x86_64.AppImage
./AzGelir-x86_64.AppImage
```

### Sistem Entegrasyonu (İsteğe Bağlı):
AppImage'ı sistem menüsüne eklemek için:

```bash
# AppImage'ı uygun dizine taşı
mkdir -p ~/.local/bin
cp AzGelir-x86_64.AppImage ~/.local/bin/

# Çalıştırılabilir yap
chmod +x ~/.local/bin/AzGelir-x86_64.AppImage

# PATH'e ekle (bashrc'ye ekleyin)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Özellikler

- ✅ Taşınabilir - Kurulum gerektirmez
- ✅ Herhangi bir Linux dağıtımında çalışır
- ✅ Sandbox güvenliği
- ✅ Otomatik güncelleme desteği (gelecekte)

## Sistem Gereksinimleri

- Linux x86_64
- GLIBC 2.17+ (CentOS 7+, Ubuntu 14.04+)
- X11 veya Wayland

## Sorun Giderme

### FUSE Hatası
```bash
# Ubuntu/Debian
sudo apt install fuse

# CentOS/RHEL
sudo yum install fuse

# Fedora
sudo dnf install fuse
```

### İzin Sorunları
```bash
chmod +x AzGelir-x86_64.AppImage
```

### Grafik Sorunları
Wayland kullanıyorsanız:
```bash
QT_QPA_PLATFORM=xcb ./AzGelir-x86_64.AppImage
```
"""
    
    with open("README_AppImage.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ AppImage README oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("📦 AppImage için AzGelir Paketleme Aracı")
    print("=" * 45)
    
    # Gerekli araçları kontrol et ve indir
    check_dependencies()
    
    if not download_appimage_tool():
        print("❌ AppImage tool indirilemedi!")
        sys.exit(1)
    
    # PyInstaller ile derle
    if not build_with_pyinstaller():
        print("❌ Derleme başarısız!")
        sys.exit(1)
    
    # AppDir yapısını oluştur
    appdir = create_appdir_structure()
    
    # AppDir'i hazırla
    if not setup_appdir(appdir):
        print("❌ AppDir hazırlama başarısız!")
        sys.exit(1)
    
    # AppImage oluştur
    if not build_appimage(appdir):
        print("❌ AppImage oluşturma başarısız!")
        sys.exit(1)
    
    # README oluştur
    create_appimage_readme()
    
    print("\n🎉 AppImage paketleme tamamlandı!")
    print(f"📦 AppImage dosyası: {os.path.abspath('AzGelir-x86_64.AppImage')}")
    print("📄 Kullanım kılavuzu: README_AppImage.md")
    
    # Dosya boyutunu göster
    if os.path.exists("AzGelir-x86_64.AppImage"):
        size = os.path.getsize("AzGelir-x86_64.AppImage") / (1024 * 1024)
        print(f"📏 Dosya boyutu: {size:.1f} MB")

if __name__ == "__main__":
    main()
