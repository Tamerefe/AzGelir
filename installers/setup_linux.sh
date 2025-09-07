#!/bin/bash
# AzGelir Kurulum Sihirbazı
# Bu script, AzGelir uygulamasını otomatik olarak kurar ve paketler

set -e

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Unicode karakterler
CHECK="✓"
CROSS="✗"
ARROW="→"
STAR="★"
INFO="ℹ"
WARNING="⚠"

# Banner fonksiyonu
show_banner() {
    clear
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                     AzGelir Kurulum Sihirbazı                ║
║                                                               ║
║                 Gelir/Gider Takip Uygulaması                 ║
║                                                               ║
║                      Linux Kurulum Aracı                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo -e "${CYAN}                         Versiyon 1.0.0${NC}"
    echo -e "${CYAN}                      GitHub: Tamerefe/AzGelir${NC}"
    echo
}

# Fonksiyonlar
print_success() { echo -e "${GREEN}${CHECK} $1${NC}"; }
print_error() { echo -e "${RED}${CROSS} $1${NC}"; }
print_warning() { echo -e "${YELLOW}${WARNING} $1${NC}"; }
print_info() { echo -e "${CYAN}${INFO} $1${NC}"; }
print_step() { echo -e "${PURPLE}${ARROW} $1${NC}"; }

# İlerleme çubuğu
show_progress() {
    local current=$1
    local total=$2
    local text=$3
    local percent=$((current * 100 / total))
    local filled=$((percent / 2))
    local empty=$((50 - filled))
    
    printf "\r${BLUE}["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "] ${percent}%% ${text}${NC}"
    
    if [ $current -eq $total ]; then
        echo
    fi
}

# Menü sistemi
show_menu() {
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                        KURULUM SEÇENEKLERI${NC}"
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${GREEN}1)${NC} ${CYAN}Hızlı Kurulum${NC}          - Otomatik kurulum (Önerilen)"
    echo -e "${GREEN}2)${NC} ${CYAN}Standart Paket${NC}         - Geleneksel Linux paketi"
    echo -e "${GREEN}3)${NC} ${CYAN}AppImage${NC}               - Taşınabilir uygulama"
    echo -e "${GREEN}4)${NC} ${CYAN}Snap Paketi${NC}           - Ubuntu/Snap Store paketi"
    echo -e "${GREEN}5)${NC} ${CYAN}Flatpak Manifest${NC}      - Evrensel Linux paketi"
    echo -e "${GREEN}6)${NC} ${CYAN}Tüm Paketler${NC}          - Tüm formatları oluştur"
    echo -e "${GREEN}7)${NC} ${CYAN}Sistem Bilgisi${NC}        - Sistem uyumluluğunu kontrol et"
    echo -e "${GREEN}8)${NC} ${CYAN}Kaldır${NC}                - AzGelir'i kaldır"
    echo -e "${GREEN}9)${NC} ${CYAN}Yardım${NC}                - Detaylı yardım"
    echo -e "${RED}0)${NC} ${RED}Çıkış${NC}"
    echo
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo
}

# Sistem tespiti
detect_system() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        DISTRO=$ID
    else
        print_error "İşletim sistemi tespit edilemedi!"
        exit 1
    fi
    
    # Mimari tespiti
    ARCH=$(uname -m)
    
    print_info "Tespit edilen sistem: $OS $VER ($ARCH)"
    
    # Uyumluluk kontrolü
    case "$DISTRO" in
        ubuntu|debian)
            PACKAGE_MANAGER="apt"
            SUPPORTED=true
            ;;
        fedora|centos|rhel)
            PACKAGE_MANAGER="dnf"
            SUPPORTED=true
            ;;
        opensuse*|sles)
            PACKAGE_MANAGER="zypper"
            SUPPORTED=true
            ;;
        arch|manjaro)
            PACKAGE_MANAGER="pacman"
            SUPPORTED=true
            ;;
        *)
            PACKAGE_MANAGER="unknown"
            SUPPORTED=false
            print_warning "Desteklenmeyen dağıtım: $DISTRO"
            ;;
    esac
}

# Bağımlılık kontrolü
check_dependencies() {
    print_step "Sistem bağımlılıkları kontrol ediliyor..."
    
    local deps_ok=true
    local step=0
    local total_steps=5
    
    # Python kontrolü
    ((step++))
    show_progress $step $total_steps "Python3 kontrol ediliyor..."
    sleep 0.5
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python3 bulundu: $PYTHON_VERSION"
    else
        print_error "Python3 bulunamadı!"
        deps_ok=false
    fi
    
    # Pip kontrolü
    ((step++))
    show_progress $step $total_steps "Pip kontrol ediliyor..."
    sleep 0.5
    if command -v pip3 &> /dev/null || python3 -m pip --version &> /dev/null; then
        print_success "pip3 bulundu"
    else
        print_error "pip3 bulunamadı!"
        deps_ok=false
    fi
    
    # Git kontrolü
    ((step++))
    show_progress $step $total_steps "Git kontrol ediliyor..."
    sleep 0.5
    if command -v git &> /dev/null; then
        print_success "Git bulundu"
    else
        print_warning "Git bulunamadı (isteğe bağlı)"
    fi
    
    # PyQt5 kontrolü
    ((step++))
    show_progress $step $total_steps "PyQt5 kontrol ediliyor..."
    sleep 0.5
    if python3 -c "import PyQt5.QtWidgets" 2>/dev/null; then
        print_success "PyQt5 bulundu"
    else
        print_warning "PyQt5 bulunamadı (kurulacak)"
    fi
    
    # Disk alanı kontrolü
    ((step++))
    show_progress $step $total_steps "Disk alanı kontrol ediliyor..."
    sleep 0.5
    available_space=$(df . | awk 'NR==2 {print $4}')
    required_space=204800  # 200MB in KB
    
    if [ "$available_space" -gt "$required_space" ]; then
        print_success "Yeterli disk alanı mevcut"
    else
        print_warning "Disk alanı az olabilir"
    fi
    
    echo
    return $deps_ok
}

# Eksik bağımlılıkları yükle
install_dependencies() {
    print_step "Eksik bağımlılıklar yükleniyor..."
    
    case "$PACKAGE_MANAGER" in
        apt)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv python3-pyqt5 \
                               python3-pyqt5.qtwidgets python3-pyqt5.qtcore \
                               python3-pyqt5.qtgui fonts-liberation fonts-dejavu
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip python3-qt5 python3-qt5-devel \
                               liberation-fonts dejavu-fonts
            ;;
        zypper)
            sudo zypper install -y python3 python3-pip python3-qt5 \
                                   liberation-fonts dejavu-fonts
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-pip python-pyqt5 \
                                       ttf-liberation ttf-dejavu
            ;;
        *)
            print_warning "Bilinmeyen paket yöneticisi, pip ile kurulacak..."
            python3 -m pip install --user PyQt5 pyinstaller
            ;;
    esac
    
    print_success "Bağımlılıklar yüklendi"
}

# Hızlı kurulum
quick_install() {
    echo
    print_step "Hızlı kurulum başlatılıyor..."
    echo
    
    # İlerleme takibi
    local total_steps=8
    local current_step=0
    
    # Bağımlılıkları kontrol et ve yükle
    ((current_step++))
    show_progress $current_step $total_steps "Bağımlılıklar kontrol ediliyor..."
    sleep 1
    if ! check_dependencies; then
        install_dependencies
    fi
    
    # Python paketlerini yükle
    ((current_step++))
    show_progress $current_step $total_steps "Python paketleri yükleniyor..."
    sleep 1
    python3 -m pip install --user -r requirements.txt || {
        print_warning "requirements.txt bulunamadı, temel paketler yükleniyor..."
        python3 -m pip install --user PyQt5 pyinstaller
    }
    
    # Standart Linux paketi oluştur
    ((current_step++))
    show_progress $current_step $total_steps "Linux paketi oluşturuluyor..."
    sleep 1
    python3 build_linux.py
    
    # Kurulum dizinlerini oluştur
    ((current_step++))
    show_progress $current_step $total_steps "Kurulum dizinleri oluşturuluyor..."
    sleep 1
    INSTALL_DIR="$HOME/.local/share/AzGelir"
    BIN_DIR="$HOME/.local/bin"
    DESKTOP_DIR="$HOME/.local/share/applications"
    
    mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR"
    
    # Dosyaları kopyala
    ((current_step++))
    show_progress $current_step $total_steps "Dosyalar kopyalanıyor..."
    sleep 1
    if [ -d "dist" ]; then
        cp -r dist/* "$INSTALL_DIR/"
    else
        cp main.py "$INSTALL_DIR/"
        cp logo.png "$INSTALL_DIR/" 2>/dev/null || true
        cp records.db "$INSTALL_DIR/" 2>/dev/null || true
    fi
    
    # Başlatıcı script oluştur
    ((current_step++))
    show_progress $current_step $total_steps "Başlatıcı oluşturuluyor..."
    sleep 1
    cat > "$BIN_DIR/azgelir" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/AzGelir"
if [ -f "AzGelir" ]; then
    ./AzGelir "$@"
else
    python3 main.py "$@"
fi
EOF
    chmod +x "$BIN_DIR/azgelir"
    
    # Desktop entry oluştur
    ((current_step++))
    show_progress $current_step $total_steps "Sistem entegrasyonu..."
    sleep 1
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
    
    # PATH kontrolü
    ((current_step++))
    show_progress $current_step $total_steps "Kurulum tamamlanıyor..."
    sleep 1
    
    # Shell'e PATH ekle
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    echo
    print_success "Hızlı kurulum tamamlandı!"
    show_completion_info
}

# Tüm paketleri oluştur
build_all_packages() {
    print_step "Tüm paket formatları oluşturuluyor..."
    echo
    
    local total_packages=4
    local current_package=0
    
    # Standart paket
    ((current_package++))
    echo -e "${CYAN}[$current_package/$total_packages] Standart Linux paketi...${NC}"
    python3 build_linux.py && print_success "Standart paket oluşturuldu" || print_error "Standart paket başarısız"
    echo
    
    # AppImage
    ((current_package++))
    echo -e "${CYAN}[$current_package/$total_packages] AppImage paketi...${NC}"
    python3 build_appimage.py && print_success "AppImage oluşturuldu" || print_error "AppImage başarısız"
    echo
    
    # Snap
    ((current_package++))
    echo -e "${CYAN}[$current_package/$total_packages] Snap paketi...${NC}"
    python3 build_snap.py && print_success "Snap paketi oluşturuldu" || print_error "Snap başarısız"
    echo
    
    # Flatpak
    ((current_package++))
    echo -e "${CYAN}[$current_package/$total_packages] Flatpak manifest...${NC}"
    python3 build_all_linux.py --format flatpak && print_success "Flatpak manifest oluşturuldu" || print_error "Flatpak başarısız"
    echo
    
    print_success "Tüm paketler oluşturuldu!"
}

# Sistem bilgilerini göster
show_system_info() {
    echo
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                           SİSTEM BİLGİSİ${NC}"
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    
    detect_system
    
    echo -e "${CYAN}İşletim Sistemi:${NC} $OS $VER"
    echo -e "${CYAN}Dağıtım:${NC} $DISTRO"
    echo -e "${CYAN}Mimari:${NC} $ARCH"
    echo -e "${CYAN}Paket Yöneticisi:${NC} $PACKAGE_MANAGER"
    echo -e "${CYAN}Destekleniyor:${NC} $([ "$SUPPORTED" = true ] && echo -e "${GREEN}Evet${NC}" || echo -e "${RED}Hayır${NC}")"
    echo
    
    # Bellek bilgisi
    if [ -f /proc/meminfo ]; then
        local total_mem=$(grep MemTotal /proc/meminfo | awk '{print int($2/1024)}')
        local free_mem=$(grep MemAvailable /proc/meminfo | awk '{print int($2/1024)}')
        echo -e "${CYAN}Toplam Bellek:${NC} ${total_mem} MB"
        echo -e "${CYAN}Kullanılabilir Bellek:${NC} ${free_mem} MB"
    fi
    
    # Disk alanı
    local disk_info=$(df -h . | awk 'NR==2 {print $2, $3, $4}')
    echo -e "${CYAN}Disk Alanı:${NC} $disk_info (Toplam Kullanılan Boş)"
    echo
    
    check_dependencies
}

# Kaldırma işlemi
uninstall_azgelir() {
    echo
    print_warning "AzGelir kaldırılıyor..."
    echo
    
    read -p "Emin misiniz? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Kaldırma iptal edildi"
        return
    fi
    
    # Çalışan uygulamayı durdur
    pkill -f "AzGelir" 2>/dev/null || true
    pkill -f "main.py.*AzGelir" 2>/dev/null || true
    
    # Dosyaları kaldır
    rm -rf "$HOME/.local/share/AzGelir"
    rm -f "$HOME/.local/bin/azgelir"
    rm -f "$HOME/.local/share/applications/AzGelir.desktop"
    
    # Build dosyalarını temizle
    rm -rf build dist *.spec __pycache__ parts stage prime snap *.snap *.AppImage
    
    print_success "AzGelir başarıyla kaldırıldı!"
}

# Tamamlama bilgilerini göster
show_completion_info() {
    echo
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                       KURULUM TAMAMLANDI!${NC}"
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${GREEN}${STAR} AzGelir başarıyla kuruldu!${NC}"
    echo
    echo -e "${CYAN}Kullanım seçenekleri:${NC}"
    echo -e "  ${GREEN}•${NC} Komut satırından: ${YELLOW}azgelir${NC}"
    echo -e "  ${GREEN}•${NC} Uygulama menüsünden: ${YELLOW}AzGelir${NC} uygulamasını arayın"
    echo
    echo -e "${CYAN}Dosya konumları:${NC}"
    echo -e "  ${GREEN}•${NC} Uygulama: ${YELLOW}$HOME/.local/share/AzGelir/${NC}"
    echo -e "  ${GREEN}•${NC} Başlatıcı: ${YELLOW}$HOME/.local/bin/azgelir${NC}"
    echo -e "  ${GREEN}•${NC} Desktop: ${YELLOW}$HOME/.local/share/applications/AzGelir.desktop${NC}"
    echo
    echo -e "${CYAN}İlk kullanım için:${NC}"
    echo -e "  ${GREEN}•${NC} Terminali yeniden başlatın veya: ${YELLOW}source ~/.bashrc${NC}"
    echo -e "  ${GREEN}•${NC} Ardından: ${YELLOW}azgelir${NC} komutunu çalıştırın"
    echo
    echo -e "${CYAN}Destek:${NC}"
    echo -e "  ${GREEN}•${NC} GitHub: ${YELLOW}https://github.com/Tamerefe/AzGelir${NC}"
    echo -e "  ${GREEN}•${NC} Issues: Sorunlar için GitHub'da issue açın"
    echo
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
}

# Yardım menüsü
show_help() {
    echo
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                             YARDIM${NC}"
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${CYAN}Kurulum Seçenekleri:${NC}"
    echo
    echo -e "${GREEN}Hızlı Kurulum:${NC}"
    echo "  En basit kurulum yöntemi. Tüm bağımlılıkları otomatik yükler"
    echo "  ve uygulamayı sistem menüsüne entegre eder."
    echo
    echo -e "${GREEN}Standart Paket:${NC}"
    echo "  Geleneksel Linux paketi oluşturur. PyInstaller kullanır."
    echo "  Tek executable dosya oluşturur."
    echo
    echo -e "${GREEN}AppImage:${NC}"
    echo "  Taşınabilir uygulama formatı. Kurulum gerektirmez."
    echo "  USB bellekte taşıyabilirsiniz."
    echo
    echo -e "${GREEN}Snap Paketi:${NC}"
    echo "  Ubuntu Store uyumlu paket. Snap desteği gerekir."
    echo "  Otomatik güncelleme ve sandbox güvenlik."
    echo
    echo -e "${GREEN}Flatpak:${NC}"
    echo "  Evrensel Linux paket formatı. Flathub uyumlu."
    echo "  Çapraz platform sandbox uygulaması."
    echo
    echo -e "${CYAN}Sistem Gereksinimleri:${NC}"
    echo "  • Python 3.6+"
    echo "  • PyQt5 kütüphaneleri"
    echo "  • 512 MB RAM"
    echo "  • 200 MB disk alanı"
    echo
    echo -e "${CYAN}Desteklenen Dağıtımlar:${NC}"
    echo "  • Ubuntu 18.04+"
    echo "  • Debian 10+"
    echo "  • Fedora 30+"
    echo "  • CentOS 7+"
    echo "  • openSUSE Leap 15+"
    echo "  • Arch Linux"
    echo
}

# Ana menü döngüsü
main_menu() {
    while true; do
        show_banner
        detect_system
        show_menu
        
        read -p "Seçiminizi yapın [1-9, 0=Çıkış]: " choice
        case $choice in
            1)
                quick_install
                read -p "Devam etmek için Enter'a basın..." 
                ;;
            2)
                print_step "Standart paket oluşturuluyor..."
                python3 build_linux.py && print_success "Standart paket oluşturuldu!"
                read -p "Devam etmek için Enter'a basın..."
                ;;
            3)
                print_step "AppImage oluşturuluyor..."
                python3 build_appimage.py && print_success "AppImage oluşturuldu!"
                read -p "Devam etmek için Enter'a basın..."
                ;;
            4)
                print_step "Snap paketi oluşturuluyor..."
                python3 build_snap.py && print_success "Snap paketi oluşturuldu!"
                read -p "Devam etmek için Enter'a basın..."
                ;;
            5)
                print_step "Flatpak manifest oluşturuluyor..."
                python3 build_all_linux.py --format flatpak && print_success "Flatpak manifest oluşturuldu!"
                read -p "Devam etmek için Enter'a basın..."
                ;;
            6)
                build_all_packages
                read -p "Devam etmek için Enter'a basın..."
                ;;
            7)
                show_system_info
                read -p "Devam etmek için Enter'a basın..."
                ;;
            8)
                uninstall_azgelir
                read -p "Devam etmek için Enter'a basın..."
                ;;
            9)
                show_help
                read -p "Devam etmek için Enter'a basın..."
                ;;
            0)
                echo
                print_info "AzGelir Kurulum Sihirbazından çıkılıyor..."
                echo -e "${CYAN}Teşekkürler! AzGelir kullandığınız için${NC}"
                exit 0
                ;;
            *)
                print_error "Geçersiz seçim! Lütfen 0-9 arasında bir değer girin."
                sleep 2
                ;;
        esac
    done
}

# Script başlangıcı
if [ "$#" -eq 0 ]; then
    # İnteraktif mod
    main_menu
else
    # Komut satırı modu
    case "$1" in
        --quick)
            show_banner
            detect_system
            quick_install
            ;;
        --help)
            show_banner
            show_help
            ;;
        --system-info)
            show_banner
            detect_system
            show_system_info
            ;;
        --uninstall)
            show_banner
            uninstall_azgelir
            ;;
        *)
            echo "Kullanım: $0 [--quick|--help|--system-info|--uninstall]"
            echo "Veya parametresiz çalıştırarak interaktif menüyü kullanın"
            exit 1
            ;;
    esac
fi
