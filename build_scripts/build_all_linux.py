#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Linux Paketleme Merkezi
Tüm Linux paket formatları için tek script
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def print_banner():
    """Başlık banner'ını yazdır"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                   AzGelir Linux Paketleme                    ║
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
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Bağımlılıklar yüklendi")
    except subprocess.CalledProcessError as e:
        print(f"❌ Bağımlılık yükleme hatası: {e}")
        sys.exit(1)

def build_standard():
    """Standart Linux paketi (PyInstaller)"""
    print("\n🐧 Standart Linux paketi oluşturuluyor...")
    try:
        subprocess.check_call([sys.executable, "build_scripts/build_linux.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Standart paket oluşturma hatası: {e}")
        return False

def build_appimage():
    """AppImage paketi"""
    print("\n📦 AppImage paketi oluşturuluyor...")
    try:
        subprocess.check_call([sys.executable, "build_scripts/build_appimage.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ AppImage oluşturma hatası: {e}")
        return False

def build_snap():
    """Snap paketi"""
    print("\n🫰 Snap paketi oluşturuluyor...")
    try:
        subprocess.check_call([sys.executable, "build_scripts/build_snap.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Snap oluşturma hatası: {e}")
        return False

def build_flatpak():
    """Flatpak manifest oluştur"""
    print("\n📱 Flatpak manifest oluşturuluyor...")
    
    manifest_content = """{
    "app-id": "io.github.tamerefe.AzGelir",
    "runtime": "org.freedesktop.Platform",
    "runtime-version": "21.08",
    "sdk": "org.freedesktop.Sdk",
    "command": "azgelir",
    "finish-args": [
        "--socket=wayland",
        "--socket=x11",
        "--share=ipc",
        "--device=dri",
        "--filesystem=home",
        "--filesystem=xdg-documents"
    ],
    "modules": [
        {
            "name": "python3-pyqt5",
            "buildsystem": "simple",
            "build-commands": [
                "pip3 install --no-index --find-links=file://${PWD} --prefix=${FLATPAK_DEST} PyQt5"
            ],
            "sources": [
                {
                    "type": "file",
                    "url": "https://files.pythonhosted.org/packages/source/P/PyQt5/PyQt5-5.15.7.tar.gz",
                    "sha256": "755121a52b3a08cb07275c10ebb96576d36e320e572591db16cfdbc558101594"
                }
            ]
        },
        {
            "name": "azgelir",
            "buildsystem": "simple",
            "build-commands": [
                "install -Dm755 main.py ${FLATPAK_DEST}/bin/azgelir",
                "install -Dm644 logo.png ${FLATPAK_DEST}/share/icons/hicolor/256x256/apps/io.github.tamerefe.AzGelir.png",
                "install -Dm644 io.github.tamerefe.AzGelir.desktop ${FLATPAK_DEST}/share/applications/io.github.tamerefe.AzGelir.desktop",
                "install -Dm644 io.github.tamerefe.AzGelir.metainfo.xml ${FLATPAK_DEST}/share/metainfo/io.github.tamerefe.AzGelir.metainfo.xml"
            ],
            "sources": [
                {
                    "type": "dir",
                    "path": "."
                }
            ]
        }
    ]
}"""
    
    # Flatpak dosyalarını oluştur
    with open("io.github.tamerefe.AzGelir.json", "w", encoding="utf-8") as f:
        f.write(manifest_content)
    
    # Desktop dosyası
    desktop_content = """[Desktop Entry]
Type=Application
Name=AzGelir
Comment=Gelir ve Gider Takip Uygulaması
Exec=azgelir
Icon=io.github.tamerefe.AzGelir
StartupWMClass=AzGelir
Categories=Office;Finance;
"""
    
    with open("io.github.tamerefe.AzGelir.desktop", "w", encoding="utf-8") as f:
        f.write(desktop_content)
    
    # MetaInfo dosyası
    metainfo_content = """<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>io.github.tamerefe.AzGelir</id>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>MIT</project_license>
  <name>AzGelir</name>
  <summary>Gelir ve Gider Takip Uygulaması</summary>
  <description>
    <p>
      AzGelir, PyQt5 kullanılarak geliştirilmiş modern bir gelir/gider takip sistemidir.
      Muhasebe odaklı, erişilebilir ve kullanıcı dostu arayüzü ile finansal kayıtlarınızı
      kolayca takip edebilirsiniz.
    </p>
  </description>
  <categories>
    <category>Office</category>
    <category>Finance</category>
  </categories>
  <url type="homepage">https://github.com/Tamerefe/AzGelir</url>
  <developer_name>Tamerefe</developer_name>
  <releases>
    <release version="1.0.0" date="2025-09-06"/>
  </releases>
</component>"""
    
    with open("io.github.tamerefe.AzGelir.metainfo.xml", "w", encoding="utf-8") as f:
        f.write(metainfo_content)
    
    print("✅ Flatpak manifest dosyaları oluşturuldu")
    print("📋 Flatpak oluşturmak için:")
    print("   flatpak-builder build-dir io.github.tamerefe.AzGelir.json")
    return True

def create_distribution_readme():
    """Dağıtım README'si oluştur"""
    readme_content = """# AzGelir - Linux Dağıtım Paketleri

Bu dizin, AzGelir uygulamasının farklı Linux paket formatlarını içerir.

## 📦 Paket Formatları

### 1. Standart Linux Paketi (dist/)
- **Dosya**: `dist/AzGelir`
- **Kurulum**: `./install.sh`
- **Kullanım**: Geleneksel Linux uygulaması
- **Avantajlar**: Hızlı, küçük boyut
- **Uyumlu**: Tüm Linux dağıtımları

### 2. AppImage
- **Dosya**: `AzGelir-x86_64.AppImage`
- **Kurulum**: Kurulum gerektirmez
- **Kullanım**: `./AzGelir-x86_64.AppImage`
- **Avantajlar**: Taşınabilir, sandbox
- **Uyumlu**: Çoğu Linux dağıtımı

### 3. Snap Paketi
- **Dosya**: `azgelir_1.0.0_amd64.snap`
- **Kurulum**: `sudo snap install azgelir_1.0.0_amd64.snap --dangerous`
- **Kullanım**: `azgelir`
- **Avantajlar**: Otomatik güncelleme, güvenlik
- **Uyumlu**: Ubuntu, Fedora, vb.

### 4. Flatpak (Manifest)
- **Dosyalar**: `io.github.tamerefe.AzGelir.json`
- **Build**: `flatpak-builder build-dir io.github.tamerefe.AzGelir.json`
- **Avantajlar**: Sandbox, çapraz platform
- **Uyumlu**: Tüm modern Linux dağıtımları

## 🚀 Hızlı Başlangıç

### En Kolay: AppImage
```bash
chmod +x AzGelir-x86_64.AppImage
./AzGelir-x86_64.AppImage
```

### En Yaygın: Standart Paket
```bash
cd dist/
./install.sh
azgelir
```

### Ubuntu/Snap Kullanıcıları:
```bash
sudo snap install azgelir_1.0.0_amd64.snap --dangerous
azgelir
```

## 📋 Sistem Gereksinimleri

### Minimum:
- Linux x86_64
- Python 3.6+
- Qt5 libraries
- 512 MB RAM
- 100 MB disk alanı

### Önerilen:
- Ubuntu 20.04+ / Fedora 34+ / CentOS 8+
- Python 3.8+
- 1 GB RAM
- 200 MB disk alanı

## 🔧 Sorun Giderme

### PyQt5 Bulunamadı:
```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5

# Fedora
sudo dnf install python3-qt5

# CentOS/RHEL
sudo yum install python3-qt5
```

### Font Sorunları:
```bash
sudo apt install fonts-liberation fonts-dejavu
```

### Wayland Sorunları:
```bash
QT_QPA_PLATFORM=xcb ./AzGelir
```

## 📞 Destek

- **GitHub**: https://github.com/Tamerefe/AzGelir
- **Issues**: Sorunlar için GitHub'da issue açın
- **Wiki**: Detaylı dokümantasyon için wiki sayfasını inceleyin

## 📄 Lisans

MIT License - Detaylar için LICENSE dosyasını inceleyin.
"""
    
    with open("README_Distribution.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Dağıtım README'si oluşturuldu")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description="AzGelir Linux Paketleme Aracı")
    parser.add_argument("--format", choices=["standard", "appimage", "snap", "flatpak", "all"],
                       default="all", help="Paket formatı seçin")
    parser.add_argument("--no-deps", action="store_true", 
                       help="Bağımlılık kurulumunu atla")
    
    args = parser.parse_args()
    
    print_banner()
    check_python_version()
    
    if not args.no_deps:
        install_dependencies()
    
    success_count = 0
    total_count = 0
    
    if args.format in ["standard", "all"]:
        total_count += 1
        if build_standard():
            success_count += 1
    
    if args.format in ["appimage", "all"]:
        total_count += 1
        if build_appimage():
            success_count += 1
    
    if args.format in ["snap", "all"]:
        total_count += 1
        if build_snap():
            success_count += 1
    
    if args.format in ["flatpak", "all"]:
        total_count += 1
        if build_flatpak():
            success_count += 1
    
    # Dağıtım README'si oluştur
    create_distribution_readme()
    
    print(f"\n🎉 Paketleme tamamlandı!")
    print(f"✅ Başarılı: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🚀 Tüm paketler başarıyla oluşturuldu!")
    else:
        print("⚠️ Bazı paketlerde sorun oluştu. Detaylar için yukarıdaki logları inceleyin.")

if __name__ == "__main__":
    main()
