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
python gelir_gider_modulu.py
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

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
