# Gelir/Gider Takip Uygulaması

Bu uygulama, PyQt5 kullanılarak geliştirilmiş bir gelir/gider takip sistemidir. Muhasebe odaklı, erişilebilir ve kullanıcı dostu bir arayüze sahiptir.

## Özellikler

- ✅ Gelir ve gider kayıtlarını tutma
- ✅ Gelişmiş tarih seçimi (takvim popup, hızlı butonlar)
- ✅ Tarih aralığı filtresi (son 30 gün varsayılan)
- ✅ İsteğe bağlı KDV hesaplama (KDV Yok, %1, %10, %18)
- ✅ Otomatik belge numarası oluşturma (G20250906001 formatında)
- ✅ Farklı hesap türleri (Kasa, Banka, vb.)
- ✅ Kategori bazlı gruplandırma
- ✅ Özet raporlama (Toplam gelir, gider, bakiye)
- ✅ CSV formatında dışa aktarma
- ✅ SQLite veritabanı entegrasyonu
- ✅ Modern ve responsive arayüz

## Kurulum

## Kurulum

### 🚀 Hızlı Kurulum

#### Linux:
```bash
git clone https://github.com/Tamerefe/AzGelir.git
cd AzGelir
chmod +x setup_linux.sh
./setup_linux.sh
```

#### Windows:
```cmd
git clone https://github.com/Tamerefe/AzGelir.git
cd AzGelir
setup_windows.bat
```

### 📖 Detaylı Kurulum Kılavuzu

Kapsamlı kurulum talimatları için: **[KURULUM_KILAVUZU.md](KURULUM_KILAVUZU.md)**

### 📋 Hızlı Başlangıç

#### Gereksinimler:
- Python 3.6+
- PyQt5
- SQLite3 (Python ile gelir)

#### Manuel Kurulum:
```bash
pip install -r requirements.txt
python main.py
```

### Gereksinimler
- Python 3.7 veya üzeri
- PyQt5

### Adımlar

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
python main.py
```

## Kullanım

1. **Yeni Kayıt Ekleme:**
   - Tarih seçin (takvim popup veya "Bugün"/"Dün" butonları)
   - Tür (Gelir/Gider), tutar bilgilerini girin
   - İsteğe bağlı KDV oranını seçin (KDV Yok, %1, %10, %18)
   - Hesap türü ve kategori seçin
   - Belge numarası otomatik oluşturulur (örn: G06.09.2025001)
   - Açıklama ekleyin ve "Kaydet" butonuna tıklayın

2. **Tarih Filtreleme:**
   - Kayıtlar tablosunda tarih aralığı seçin
   - "Filtrele" butonuna tıklayın
   - "Tümü" butonu ile filtreyi kaldırın

2. **Tarih Filtreleme:**
   - Kayıtlar tablosunda tarih aralığı seçin
   - "Filtrele" butonuna tıklayın
   - "Tümü" butonu ile filtreyi kaldırın

3. **Kayıt Silme:**
   - Tabloda silinecek kaydı seçin
   - "Sil" butonuna tıklayın

4. **Dışa Aktarma:**
   - "Dışa Aktar (CSV)" butonuna tıklayın
   - Kaydetmek istediğiniz konumu seçin

5. **Özet Bilgiler:**
   - Alt kısımda toplam gelir, gider ve bakiye bilgileri görüntülenir

## Veritabanı

Uygulama SQLite veritabanı kullanır. `records.db` dosyası otomatik olarak oluşturulur ve tüm kayıtlar burada saklanır.

## Hesap Türleri

- 100 - Kasa
- 101 - Alınan Çekler
- 102 - Banka
- 120 - Alıcılar
- 320 - Satıcılar

## Kategoriler

- Satış
- Hizmet
- Kira
- Fatura
- Ofis
- Maaş
- Diğer

## Ekran Görüntüleri

Uygulama modern ve kullanıcı dostu bir arayüze sahiptir:
- Temiz form alanları
- Tablo görünümü
- Özet bilgiler
- KDV hesaplama

## Linux Paketleme

AzGelir uygulaması farklı Linux paket formatlarında dağıtılabilir:

### 🚀 Hızlı Kurulum (Linux)
```bash
# Otomatik kurulum scripti
chmod +x install_linux.sh
./install_linux.sh
```

### 📦 Paket Formatları

#### 1. Standart Linux Paketi
```bash
python3 build_linux.py
# Çıktı: dist/AzGelir + kurulum scriptleri
```

#### 2. AppImage (Taşınabilir)
```bash
python3 build_appimage.py
# Çıktı: AzGelir-x86_64.AppImage
```

#### 3. Snap Paketi
```bash
python3 build_snap.py
# Çıktı: azgelir_1.0.0_amd64.snap
```

#### 4. Flatpak Manifest
```bash
python3 build_all_linux.py --format flatpak
# Çıktı: io.github.tamerefe.AzGelir.json
```

#### 5. Tüm Formatlar
```bash
python3 build_all_linux.py
# Tüm paket formatlarını oluşturur
```

### 🐧 Linux Sistem Gereksinimleri
- Python 3.6+
- PyQt5 kütüphaneleri
- SQLite3 desteği
- X11 veya Wayland display server

### 📋 Dağıtım Desteği
- ✅ Ubuntu 18.04+
- ✅ Fedora 30+
- ✅ CentOS 7+
- ✅ Debian 10+
- ✅ openSUSE Leap 15+
- ✅ Arch Linux
- ✅ Diğer modern Linux dağıtımları

## Windows Paketleme

AzGelir uygulaması farklı Windows paket formatlarında dağıtılabilir:

### 🚀 Hızlı Kurulum (Windows)
```powershell
# PowerShell'i yönetici olarak çalıştırın
.\build_all_windows.py
```

### 📦 Paket Formatları

#### 1. Windows Executable
```bash
python build_windows.py
# Çıktı: dist/AzGelir.exe + kurulum scriptleri
```

#### 2. MSI Installer (Enterprise)
```bash
python build_msi.py
# Çıktı: AzGelir_Setup.msi
```

#### 3. NSIS Installer
```bash
python build_all_windows.py --format nsis
# Çıktı: AzGelir_Setup.exe
```

#### 4. Portable Sürüm
```bash
python build_all_windows.py --format portable
# Çıktı: AzGelir_Portable.zip
```

#### 5. Chocolatey Paketi
```bash
python build_all_windows.py --format chocolatey
# Çıktı: chocolatey/azgelir.nuspec
```

#### 6. Tüm Formatlar
```bash
python build_all_windows.py
# Tüm paket formatlarını oluşturur
```

### 🪟 Windows Sistem Gereksinimleri
- Windows 7 SP1+ / Windows Server 2008 R2 SP1+
- .NET Framework 4.6.1+
- Visual C++ Redistributable (otomatik yüklenir)
- 512 MB RAM, 100 MB disk alanı

### 📋 Dağıtım Desteği
- ✅ Windows 7/8/8.1/10/11
- ✅ Windows Server 2008 R2+
- ✅ 32-bit ve 64-bit sistemler
- ✅ Domain ve Workgroup ortamları
- ✅ Debian 10+
- ✅ openSUSE Leap 15+
- ✅ Arch Linux
- ✅ Diğer modern Linux dağıtımları

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
