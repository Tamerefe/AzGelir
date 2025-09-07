#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snap paket formatında Linux paketleme scripti
Ubuntu ve diğer Linux dağıtımları için
"""

import os
import subprocess
import sys
import shutil
import json
from pathlib import Path

def check_snapcraft():
    """Snapcraft kurulu mu kontrol et"""
    try:
        result = subprocess.run(["snapcraft", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Snapcraft bulundu")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Snapcraft bulunamadı")
    print("Kurulum için:")
    print("  Ubuntu/Debian: sudo apt install snapcraft")
    print("  veya Snap ile: sudo snap install snapcraft --classic")
    return False

def check_multipass():
    """Multipass kurulu mu kontrol et (clean build için)"""
    try:
        result = subprocess.run(["multipass", "version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Multipass bulundu (clean build kullanılabilir)")
            return True
    except FileNotFoundError:
        pass
    
    print("ℹ️ Multipass bulunamadı (clean build kullanılamaz)")
    return False

def validate_snapcraft_yaml():
    """snapcraft.yaml dosyasını doğrula"""
    if not os.path.exists("snapcraft.yaml"):
        print("❌ snapcraft.yaml dosyası bulunamadı!")
        return False
    
    try:
        import yaml
        with open("snapcraft.yaml", "r", encoding="utf-8") as f:
            snap_config = yaml.safe_load(f)
        
        required_fields = ["name", "version", "summary", "description", "parts"]
        for field in required_fields:
            if field not in snap_config:
                print(f"❌ snapcraft.yaml'da gerekli alan eksik: {field}")
                return False
        
        print("✓ snapcraft.yaml doğrulandı")
        return True
    except ImportError:
        print("⚠️ PyYAML bulunamadı, YAML doğrulaması atlanıyor")
        return True
    except Exception as e:
        print(f"❌ snapcraft.yaml doğrulama hatası: {e}")
        return False

def clean_build():
    """Önceki build dosyalarını temizle"""
    dirs_to_clean = ["parts", "stage", "prime", "snap"]
    files_to_clean = ["*.snap"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ {dir_name} temizlendi")
    
    # .snap dosyalarını temizle
    for snap_file in Path(".").glob("*.snap"):
        snap_file.unlink()
        print(f"✓ {snap_file} temizlendi")

def build_snap(use_multipass=False):
    """Snap paketini oluştur"""
    print("📦 Snap paketi oluşturuluyor...")
    
    if use_multipass:
        cmd = ["snapcraft", "--use-lxd"]
        print("🔨 Multipass ile clean build yapılıyor...")
    else:
        cmd = ["snapcraft"]
        print("🔨 Yerel build yapılıyor...")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Snap paketi başarıyla oluşturuldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Snap build hatası: {e}")
        return False

def install_snap_locally():
    """Oluşturulan snap'i yerel olarak kur"""
    snap_files = list(Path(".").glob("*.snap"))
    if not snap_files:
        print("❌ Snap dosyası bulunamadı!")
        return False
    
    snap_file = snap_files[0]
    print(f"📥 {snap_file} yerel olarak kuruluyor...")
    
    try:
        subprocess.check_call([
            "sudo", "snap", "install", str(snap_file), 
            "--dangerous", "--devmode"
        ])
        print("✅ Snap başarıyla kuruldu!")
        print("🚀 Kullanım: snap run azgelir")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Snap kurulum hatası: {e}")
        return False

def create_snap_readme():
    """Snap README dosyası oluştur"""
    readme_content = """# AzGelir - Snap Paketi

## Kurulum

### Snap Store'dan (Gelecekte):
```bash
sudo snap install azgelir
```

### Yerel Dosyadan:
```bash
sudo snap install azgelir_1.0.0_amd64.snap --dangerous --devmode
```

## Kullanım

```bash
# Uygulamayı çalıştır
snap run azgelir

# veya kısaca
azgelir
```

## İzinler

Snap paketinin güvenli çalışması için aşağıdaki izinler verilmiştir:

- **home**: Ev dizinindeki dosyalara erişim
- **desktop**: Masaüstü entegrasyonu
- **x11/wayland**: Grafik arayüzü
- **network**: İnternet bağlantısı (gelecek özellikler için)
- **removable-media**: USB/harici disk erişimi

## Veri Dosyaları

Snap uygulamasının verileri şurada saklanır:
```
~/snap/azgelir/current/
```

## Güncelleme

```bash
sudo snap refresh azgelir
```

## Kaldırma

```bash
sudo snap remove azgelir
```

## Snap Store'a Yayınlama

1. Snapcraft hesabı oluşturun: https://snapcraft.io/
2. Snap'inizi kaydedin:
   ```bash
   snapcraft register azgelir
   ```
3. Yayınlayın:
   ```bash
   snapcraft upload azgelir_1.0.0_amd64.snap
   snapcraft release azgelir <revision> stable
   ```

## Sorun Giderme

### İzin Sorunları
```bash
# Tüm izinleri kontrol et
snap connections azgelir

# Eksik bağlantıları el ile bağla
sudo snap connect azgelir:home
sudo snap connect azgelir:desktop
```

### Debug Modu
```bash
# Detaylı log için
snap run --shell azgelir
```

### Snap Logs
```bash
# Snap loglarını görüntüle
snap logs azgelir
```
"""
    
    with open("README_Snap.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ Snap README oluşturuldu")

def get_snap_info():
    """Oluşturulan snap hakkında bilgi göster"""
    snap_files = list(Path(".").glob("*.snap"))
    if snap_files:
        snap_file = snap_files[0]
        size = os.path.getsize(snap_file) / (1024 * 1024)
        print(f"\n📦 Snap dosyası: {snap_file}")
        print(f"📏 Dosya boyutu: {size:.1f} MB")
        
        # Snap info göster
        try:
            result = subprocess.run(
                ["snap", "info", str(snap_file)], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("\n📋 Snap bilgileri:")
                print(result.stdout)
        except:
            pass

def main():
    """Ana fonksiyon"""
    print("📦 Snap için AzGelir Paketleme Aracı")
    print("=" * 40)
    
    # Snapcraft kontrolü
    if not check_snapcraft():
        sys.exit(1)
    
    # Multipass kontrolü
    has_multipass = check_multipass()
    
    # snapcraft.yaml doğrulama
    if not validate_snapcraft_yaml():
        sys.exit(1)
    
    # Temizlik
    clean_build()
    
    # Build seçeneği
    use_multipass = False
    if has_multipass:
        response = input("\nMultipass ile clean build yapılsın mı? (y/N): ").lower()
        use_multipass = response in ['y', 'yes', 'evet']
    
    # Snap oluştur
    if not build_snap(use_multipass):
        sys.exit(1)
    
    # README oluştur
    create_snap_readme()
    
    # Bilgileri göster
    get_snap_info()
    
    print("\n🎉 Snap paketleme tamamlandı!")
    
    # Yerel kurulum seçeneği
    response = input("\nOluşturulan snap'i yerel olarak kurmak ister misiniz? (y/N): ").lower()
    if response in ['y', 'yes', 'evet']:
        install_snap_locally()

if __name__ == "__main__":
    main()
