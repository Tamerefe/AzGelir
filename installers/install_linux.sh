#!/bin/bash
# AzGelir Linux Otomatik Kurulum Scripti
# Bu script, uygulamayı otomatik olarak kurar ve gerekli bağımlılıkları yükler

set -e  # Hata durumunda çık

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                   AzGelir Linux Kurulum                      ║"
echo "║                   Gelir/Gider Takip Uygulaması               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Fonksiyonlar
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Sistem tespiti
detect_system() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        print_error "İşletim sistemi tespit edilemedi!"
        exit 1
    fi
    
    print_info "Tespit edilen sistem: $OS $VER"
}

# Python kontrolü
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python3 bulundu: $PYTHON_VERSION"
        
        # Python 3.6+ kontrolü
        python3 -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_success "Python versiyonu uygun"
        else
            print_error "Python 3.6+ gerekli!"
            exit 1
        fi
    else
        print_error "Python3 bulunamadı!"
        install_python
    fi
}

# Python kurulumu
install_python() {
    print_info "Python3 kuruluyor..."
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y python3 python3-pip
            else
                sudo yum install -y python3 python3-pip
            fi
            ;;
        *"openSUSE"*)
            sudo zypper install -y python3 python3-pip
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm python python-pip
            ;;
        *)
            print_error "Desteklenmeyen dağıtım: $OS"
            print_info "Lütfen manuel olarak Python3 kurun"
            exit 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        print_success "Python3 kuruldu"
    else
        print_error "Python3 kurulumu başarısız!"
        exit 1
    fi
}

# PyQt5 kurulumu
install_pyqt5() {
    print_info "PyQt5 kuruluyor..."
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            sudo apt install -y python3-pyqt5 python3-pyqt5.qtwidgets python3-pyqt5.qtcore python3-pyqt5.qtgui
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y python3-qt5 python3-qt5-devel
            else
                sudo yum install -y python3-qt5 python3-qt5-devel
            fi
            ;;
        *"openSUSE"*)
            sudo zypper install -y python3-qt5
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm python-pyqt5
            ;;
        *)
            print_warning "Sistem paketi bulunamadı, pip ile kurulacak..."
            python3 -m pip install --user PyQt5
            ;;
    esac
    
    # PyQt5 test
    python3 -c "import PyQt5.QtWidgets" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "PyQt5 kuruldu"
    else
        print_warning "Sistem paketi başarısız, pip ile deneniyor..."
        python3 -m pip install --user PyQt5
        
        python3 -c "import PyQt5.QtWidgets" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_success "PyQt5 pip ile kuruldu"
        else
            print_error "PyQt5 kurulumu başarısız!"
            exit 1
        fi
    fi
}

# Font kurulumu
install_fonts() {
    print_info "Fontlar kuruluyor..."
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            sudo apt install -y fonts-liberation fonts-dejavu fonts-noto
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y liberation-fonts dejavu-fonts google-noto-fonts
            else
                sudo yum install -y liberation-fonts dejavu-fonts google-noto-sans-fonts
            fi
            ;;
        *"openSUSE"*)
            sudo zypper install -y liberation-fonts dejavu-fonts google-noto-fonts
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm ttf-liberation ttf-dejavu noto-fonts
            ;;
        *)
            print_warning "Font paketi bilinmiyor, atlanıyor..."
            ;;
    esac
    
    print_success "Fontlar kuruldu"
}

# AzGelir kurulumu
install_azgelir() {
    print_info "AzGelir kuruluyor..."
    
    # Kurulum dizinleri
    INSTALL_DIR="$HOME/.local/share/AzGelir"
    BIN_DIR="$HOME/.local/bin"
    DESKTOP_DIR="$HOME/.local/share/applications"
    
    # Dizinleri oluştur
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    mkdir -p "$DESKTOP_DIR"
    
    # Mevcut dosyaları kontrol et
    if [ -f "main.py" ]; then
        print_info "Kaynak dosyalardan kurulum yapılıyor..."
        
        # Dosyaları kopyala
        cp main.py "$INSTALL_DIR/"
        cp logo.png "$INSTALL_DIR/" 2>/dev/null || print_warning "Logo dosyası bulunamadı"
        cp records.db "$INSTALL_DIR/" 2>/dev/null || print_info "Veritabanı dosyası oluşturulacak"
        
        # Başlatıcı script oluştur
        cat > "$BIN_DIR/azgelir" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/AzGelir"
python3 main.py "$@"
EOF
        chmod +x "$BIN_DIR/azgelir"
        
    elif [ -f "AzGelir" ]; then
        print_info "Derlenmiş dosyadan kurulum yapılıyor..."
        
        # Derlenmiş dosyayı kopyala
        cp AzGelir "$INSTALL_DIR/"
        chmod +x "$INSTALL_DIR/AzGelir"
        cp logo.png "$INSTALL_DIR/" 2>/dev/null || print_warning "Logo dosyası bulunamadı"
        cp records.db "$INSTALL_DIR/" 2>/dev/null || print_info "Veritabanı dosyası oluşturulacak"
        
        # Sembolik link oluştur
        ln -sf "$INSTALL_DIR/AzGelir" "$BIN_DIR/azgelir"
        
    else
        print_error "AzGelir dosyaları bulunamadı!"
        print_info "Bu script'i AzGelir kaynak kodları ile aynı dizinde çalıştırın"
        exit 1
    fi
    
    # Desktop entry oluştur
    cat > "$DESKTOP_DIR/AzGelir.desktop" << EOF
[Desktop Entry]
Type=Application
Name=AzGelir
Name[tr]=AzGelir - Gelir/Gider Takip
Comment=Gelir ve Gider Takip Uygulaması
Comment[tr]=Muhasebe odaklı gelir ve gider takip sistemi
Exec=$BIN_DIR/azgelir
Icon=$INSTALL_DIR/logo.png
Terminal=false
StartupWMClass=AzGelir
Categories=Office;Finance;
Keywords=gelir;gider;muhasebe;finans;
EOF
    
    chmod +x "$DESKTOP_DIR/AzGelir.desktop"
    
    print_success "AzGelir kuruldu"
}

# PATH kontrolü
check_path() {
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        print_success "PATH zaten düzgün ayarlanmış"
    else
        print_warning "PATH'e ~/.local/bin ekleniyor..."
        
        # Shell'e göre uygun dosyayı bul
        if [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -f "$HOME/.profile" ]; then
            SHELL_RC="$HOME/.profile"
        else
            SHELL_RC="$HOME/.bashrc"
        fi
        
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        export PATH="$HOME/.local/bin:$PATH"
        
        print_success "PATH güncellendi ($SHELL_RC)"
        print_info "Değişikliklerin etkili olması için terminali yeniden başlatın"
    fi
}

# Kurulum sonrası test
test_installation() {
    print_info "Kurulum test ediliyor..."
    
    if [ -x "$HOME/.local/bin/azgelir" ]; then
        print_success "AzGelir çalıştırılabilir"
        
        # Python modüllerini test et
        python3 -c "
import sys
import sqlite3
import csv
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
print('✓ Tüm modüller yüklenebilir')
" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            print_success "Tüm bağımlılıklar hazır"
        else
            print_error "Bazı Python modülleri eksik!"
        fi
    else
        print_error "AzGelir çalıştırılabilir dosyası bulunamadı!"
    fi
}

# Kullanım bilgileri
show_usage() {
    echo
    print_success "Kurulum tamamlandı! 🎉"
    echo
    print_info "Kullanım:"
    echo "  Komut satırından: azgelir"
    echo "  Uygulama menüsünden: 'AzGelir' uygulamasını arayın"
    echo
    print_info "Dosya konumları:"
    echo "  Uygulama: $HOME/.local/share/AzGelir/"
    echo "  Başlatıcı: $HOME/.local/bin/azgelir"
    echo "  Desktop: $HOME/.local/share/applications/AzGelir.desktop"
    echo
    print_info "Kaldırmak için:"
    echo "  rm -rf $HOME/.local/share/AzGelir"
    echo "  rm -f $HOME/.local/bin/azgelir"
    echo "  rm -f $HOME/.local/share/applications/AzGelir.desktop"
    echo
}

# Ana kurulum süreci
main() {
    print_info "AzGelir Linux kurulumu başlıyor..."
    echo
    
    detect_system
    check_python
    install_pyqt5
    install_fonts
    install_azgelir
    check_path
    test_installation
    show_usage
    
    print_success "Kurulum başarıyla tamamlandı!"
}

# Script'i çalıştır
main "$@"
