#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux için PyInstaller build scripti
AzGelir uygulamasını tek dosya halinde paketler
"""

import os
import subprocess
import sys
import shutil
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

def build_application():
    """Uygulamayı paketle"""
    print("🚀 Linux için uygulama paketleniyor...")
    
    # PyInstaller komut parametreleri
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tek dosya halinde paketleme
        "--windowed",                   # GUI uygulaması (console gizle)
        "--name=AzGelir",              # Uygulama adı
        "--icon=logo.png",             # Uygulama ikonu (varsa)
        "--add-data=logo.png:.",       # Logo dosyasını dahil et
        "--add-data=records.db:.",     # Veritabanı dosyasını dahil et (varsa)
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=sqlite3",
        "--hidden-import=csv",
        "--clean",                     # Önceki build'i temizle
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Paketleme başarılı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paketleme hatası: {e}")
        return False

def create_desktop_file():
    """Linux desktop entry dosyası oluştur"""
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=AzGelir
Name[tr]=AzGelir - Gelir/Gider Takip
Comment=Gelir ve Gider Takip Uygulaması
Comment[tr]=Muhasebe odaklı gelir ve gider takip sistemi
Exec=./AzGelir
Icon=azgelir
Terminal=false
StartupWMClass=AzGelir
Categories=Office;Finance;
Keywords=gelir;gider;muhasebe;finans;
"""
    
    with open("dist/AzGelir.desktop", "w", encoding="utf-8") as f:
        f.write(desktop_content)
    
    print("✓ Desktop entry dosyası oluşturuldu")

def create_install_script():
    """Kurulum scripti oluştur"""
    install_script = """#!/bin/bash
# AzGelir Linux Kurulum Scripti

echo "🚀 AzGelir kurulum başlıyor..."

# Kurulum dizinini oluştur
INSTALL_DIR="$HOME/.local/share/AzGelir"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"

# Dosyaları kopyala
echo "📁 Dosyalar kopyalanıyor..."
cp AzGelir "$INSTALL_DIR/"
cp logo.png "$INSTALL_DIR/" 2>/dev/null || echo "Logo dosyası bulunamadı, atlanıyor..."
cp records.db "$INSTALL_DIR/" 2>/dev/null || echo "Veritabanı dosyası bulunamadı, atlanıyor..."

# Çalıştırılabilir yapma
chmod +x "$INSTALL_DIR/AzGelir"

# Sembolik link oluştur
ln -sf "$INSTALL_DIR/AzGelir" "$BIN_DIR/azgelir"

# Desktop entry'yi kopyala ve düzenle
sed "s|Exec=./AzGelir|Exec=$INSTALL_DIR/AzGelir|g" AzGelir.desktop > "$DESKTOP_DIR/AzGelir.desktop"
chmod +x "$DESKTOP_DIR/AzGelir.desktop"

echo "✅ Kurulum tamamlandı!"
echo "🎯 Uygulamayı başlatmak için 'azgelir' komutunu kullanın"
echo "📱 Veya uygulama menüsünden 'AzGelir' uygulamasını arayın"
"""
    
    with open("dist/install.sh", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    os.chmod("dist/install.sh", 0o755)
    print("✓ Kurulum scripti oluşturuldu")

def create_uninstall_script():
    """Kaldırma scripti oluştur"""
    uninstall_script = """#!/bin/bash
# AzGelir Linux Kaldırma Scripti

echo "🗑️ AzGelir kaldırılıyor..."

# Kurulum dizinleri
INSTALL_DIR="$HOME/.local/share/AzGelir"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Dosyaları kaldır
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/azgelir"
rm -f "$DESKTOP_DIR/AzGelir.desktop"

echo "✅ AzGelir başarıyla kaldırıldı!"
"""
    
    with open("dist/uninstall.sh", "w", encoding="utf-8") as f:
        f.write(uninstall_script)
    
    os.chmod("dist/uninstall.sh", 0o755)
    print("✓ Kaldırma scripti oluşturuldu")

def create_readme():
    """Linux README dosyası oluştur"""
    readme_content = """# AzGelir - Linux Sürümü

## Kurulum

### Otomatik Kurulum (Önerilen)
```bash
chmod +x install.sh
./install.sh
```

### Manuel Kurulum
1. AzGelir dosyasını istediğiniz dizine kopyalayın
2. Çalıştırma izni verin: `chmod +x AzGelir`
3. Çalıştırın: `./AzGelir`

## Çalıştırma

### Komut satırından:
```bash
azgelir
```

### Uygulama menüsünden:
"AzGelir" uygulamasını arayın ve çalıştırın.

## Sistem Gereksinimleri

- Linux (Ubuntu 18.04+, CentOS 7+, Fedora 30+ veya eşdeğeri)
- X11 veya Wayland display server
- PyQt5 kütüphaneleri (genellikle sistem paketleri ile gelir)

## Kaldırma

```bash
./uninstall.sh
```

## Sorun Giderme

### PyQt5 Hatası
Eğer PyQt5 ile ilgili hata alırsanız:

**Ubuntu/Debian:**
```bash
sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install python3-qt5 python3-qt5-devel
```

### Font Sorunları
Türkçe karakterler düzgün görünmüyorsa:
```bash
sudo apt install fonts-liberation fonts-dejavu
```

### İzin Sorunları
Uygulama çalışmıyorsa:
```bash
chmod +x AzGelir
```

## Destek

Sorunlar için GitHub deposunda issue açabilirsiniz.
"""
    
    with open("dist/README_Linux.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ Linux README dosyası oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🐧 Linux için AzGelir Paketleme Aracı")
    print("=" * 40)
    
    # Gerekli bağımlılıkları kontrol et
    check_dependencies()
    
    # Önceki build'leri temizle
    clean_build()
    
    # Uygulamayı paketleme
    if not build_application():
        print("❌ Paketleme başarısız!")
        sys.exit(1)
    
    # Ek dosyalar oluştur
    create_desktop_file()
    create_install_script()
    create_uninstall_script()
    create_readme()
    
    print("\n🎉 Linux paketleme tamamlandı!")
    print(f"📦 Paket dosyaları: {os.path.abspath('dist')}")
    print("\n📋 Dağıtım için hazır dosyalar:")
    print("   • AzGelir (ana uygulama)")
    print("   • install.sh (kurulum scripti)")
    print("   • uninstall.sh (kaldırma scripti)")
    print("   • AzGelir.desktop (desktop entry)")
    print("   • README_Linux.md (kullanım kılavuzu)")

if __name__ == "__main__":
    main()
