#!/bin/bash
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
