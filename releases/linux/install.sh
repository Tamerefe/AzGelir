#!/bin/bash
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
