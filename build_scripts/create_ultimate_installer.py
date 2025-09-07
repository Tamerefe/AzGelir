#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Embedded Installer Creator
Tek dosya, sıfırdan bilgisayar kurulum exe dosyası oluşturucu
"""

import os
import sys
import subprocess
import base64
import zipfile
import tempfile
import shutil
from pathlib import Path

def create_embedded_installer():
    """Gömülü dosyalı tek exe installer oluştur"""
    
    print("🔨 Embedded installer oluşturuluyor...")
    
    # Dosyaları base64'e çevir
    def file_to_base64(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        return ""
    
    # Ana executable varsa base64'e çevir
    azgelir_exe_b64 = ""
    if os.path.exists("dist/AzGelir.exe"):
        print("📦 AzGelir.exe gömülüyor...")
        azgelir_exe_b64 = file_to_base64("dist/AzGelir.exe")
    
    # Logo varsa base64'e çevir
    logo_b64 = ""
    if os.path.exists("logo.png"):
        print("🖼️ Logo gömülüyor...")
        logo_b64 = file_to_base64("logo.png")
    
    # Embedded installer script oluştur
    installer_script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Sıfırdan Bilgisayar Kurulum Programı
Python dahil her şeyi otomatik kurar
"""

import sys
import os
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import winreg
from pathlib import Path

# Gömülü dosyalar (Base64)
AZGELIR_EXE_B64 = """{azgelir_exe_b64[:1000]}"""  # Kısaltılmış gösterim
LOGO_PNG_B64 = """{logo_b64}"""

class AzGelirFullInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AzGelir Sıfırdan Kurulum Sihirbazı")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Tema ayarları
        self.root.configure(bg='#f0f0f0')
        
        self.install_dir = "C:\\\\Program Files\\\\AzGelir"
        self.temp_dir = tempfile.mkdtemp()
        
        self.create_widgets()
        self.extract_embedded_files()
        
    def create_widgets(self):
        # Ana frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık frame
        title_frame = tk.Frame(main_frame, bg='#2c3e50', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="AzGelir Sıfırdan Kurulum Sihirbazı",
                              font=("Arial", 18, "bold"),
                              fg='white', bg='#2c3e50',
                              pady=15)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Python dahil tüm bileşenleri otomatik kurar",
                                 font=("Arial", 10),
                                 fg='#ecf0f1', bg='#2c3e50',
                                 pady=(0, 15))
        subtitle_label.pack()
        
        # Bilgi frame
        info_frame = tk.LabelFrame(main_frame, text="Kurulum Bilgileri", 
                                  font=("Arial", 10, "bold"),
                                  bg='#f0f0f0', fg='#2c3e50')
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, 
                           bg='#ffffff', fg='#2c3e50',
                           font=("Arial", 9), bd=1, relief=tk.SUNKEN)
        info_text.pack(fill=tk.X, padx=10, pady=10)
        
        info_content = """Bu kurulum sihirbazı şunları otomatik olarak kuracaktır:

• Python 3.11 (Embedded sürüm)
• Visual C++ Redistributable (gerekirse)
• PyQt5 ve diğer gerekli Python kütüphaneleri
• AzGelir ana uygulaması
• Masaüstü ve Başlat menüsü kısayolları
• Sistem kayıtları ve kaldırıcı

Bu işlem yaklaşık 5-10 dakika sürecektir."""
        
        info_text.insert(tk.END, info_content)
        info_text.configure(state=tk.DISABLED)
        
        # Ayarlar frame
        settings_frame = tk.LabelFrame(main_frame, text="Kurulum Ayarları",
                                     font=("Arial", 10, "bold"),
                                     bg='#f0f0f0', fg='#2c3e50')
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Kurulum dizini
        dir_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        dir_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(dir_frame, text="Kurulum Dizini:", 
                font=("Arial", 9, "bold"),
                bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W)
        
        dir_entry_frame = tk.Frame(dir_frame, bg='#f0f0f0')
        dir_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.dir_var = tk.StringVar(value=self.install_dir)
        self.dir_entry = tk.Entry(dir_entry_frame, textvariable=self.dir_var,
                                 font=("Arial", 9), bd=1, relief=tk.SUNKEN)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(dir_entry_frame, text="Gözat...",
                              command=self.browse_directory,
                              font=("Arial", 8),
                              bg='#3498db', fg='white',
                              bd=1, relief=tk.RAISED)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Seçenekler
        options_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.desktop_var = tk.BooleanVar(value=True)
        self.startmenu_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(options_frame, text="Masaüstü kısayolu oluştur",
                      variable=self.desktop_var,
                      font=("Arial", 9),
                      bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W)
        
        tk.Checkbutton(options_frame, text="Başlat menüsü kısayolu oluştur",
                      variable=self.startmenu_var,
                      font=("Arial", 9),
                      bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W)
        
        # İlerleme frame
        progress_frame = tk.LabelFrame(main_frame, text="Kurulum İlerlemesi",
                                     font=("Arial", 10, "bold"),
                                     bg='#f0f0f0', fg='#2c3e50')
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate',
                                       length=400)
        self.progress.pack(padx=10, pady=10)
        
        self.status_label = tk.Label(progress_frame, text="Kuruluma hazır",
                                   font=("Arial", 9),
                                   bg='#f0f0f0', fg='#2c3e50')
        self.status_label.pack(pady=(0, 10))
        
        # Butonlar
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.install_btn = tk.Button(button_frame, text="Kurulumu Başlat",
                                   command=self.start_installation,
                                   font=("Arial", 11, "bold"),
                                   bg='#27ae60', fg='white',
                                   padx=20, pady=10,
                                   bd=0, relief=tk.FLAT)
        self.install_btn.pack(side=tk.LEFT)
        
        tk.Button(button_frame, text="Çıkış",
                 command=self.root.quit,
                 font=("Arial", 11),
                 bg='#e74c3c', fg='white',
                 padx=20, pady=10,
                 bd=0, relief=tk.FLAT).pack(side=tk.RIGHT)
        
    def extract_embedded_files(self):
        """Gömülü dosyaları çıkar"""
        try:
            # AzGelir.exe'yi çıkar
            if AZGELIR_EXE_B64:
                azgelir_data = base64.b64decode(AZGELIR_EXE_B64)
                with open(os.path.join(self.temp_dir, "AzGelir.exe"), 'wb') as f:
                    f.write(azgelir_data)
                    
            # Logo'yu çıkar
            if LOGO_PNG_B64:
                logo_data = base64.b64decode(LOGO_PNG_B64)
                with open(os.path.join(self.temp_dir, "logo.png"), 'wb') as f:
                    f.write(logo_data)
                    
        except Exception as e:
            print(f"Dosya çıkarma hatası: {{e}}")
    
    def browse_directory(self):
        """Kurulum dizini seç"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)
    
    def update_status(self, text):
        """Durum metnini güncelle"""
        self.status_label.config(text=text)
        self.root.update()
    
    def start_installation(self):
        """Kurulumu başlat"""
        self.install_btn.config(state='disabled', text="Kuruluyor...")
        self.progress.start()
        
        # Kurulumu ayrı thread'de çalıştır
        thread = threading.Thread(target=self.install)
        thread.daemon = True
        thread.start()
    
    def install(self):
        """Ana kurulum işlemi"""
        try:
            # 1. Sistem kontrolü
            self.update_status("1/8 - Sistem uyumluluğu kontrol ediliyor...")
            self.check_system()
            
            # 2. Kurulum dizini
            self.update_status("2/8 - Kurulum dizini hazırlanıyor...")
            os.makedirs(self.dir_var.get(), exist_ok=True)
            
            # 3. Python kontrolü
            self.update_status("3/8 - Python kontrol ediliyor...")
            if not self.check_python():
                self.update_status("3a/8 - Python kuruluyor...")
                self.install_python()
            
            # 4. VC++ kontrolü
            self.update_status("4/8 - Visual C++ Redistributable kontrol ediliyor...")
            if not self.check_vcredist():
                self.update_status("4a/8 - Visual C++ Redistributable kuruluyor...")
                self.install_vcredist()
            
            # 5. AzGelir dosyaları
            self.update_status("5/8 - AzGelir dosyaları kopyalanıyor...")
            self.copy_azgelir_files()
            
            # 6. Python paketleri
            self.update_status("6/8 - Python paketleri kuruluyor...")
            self.install_python_packages()
            
            # 7. Kısayollar
            self.update_status("7/8 - Kısayollar oluşturuluyor...")
            self.create_shortcuts()
            
            # 8. Sistem kayıtları
            self.update_status("8/8 - Sistem kayıtları oluşturuluyor...")
            self.create_registry_entries()
            
            self.progress.stop()
            self.update_status("✅ Kurulum başarıyla tamamlandı!")
            
            messagebox.showinfo("Kurulum Tamamlandı",
                              "AzGelir başarıyla kuruldu!\\n\\n"
                              "Uygulamayı masaüstü kısayolundan veya\\n"
                              "Başlat menüsünden çalıştırabilirsiniz.")
            
            # Uygulamayı çalıştırma seçeneği
            if messagebox.askyesno("Uygulama Çalıştır", 
                                  "AzGelir'i şimdi çalıştırmak istiyor musunuz?"):
                subprocess.Popen([os.path.join(self.dir_var.get(), "AzGelir.exe")])
                
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            self.update_status("❌ Kurulum hatası!")
            messagebox.showerror("Kurulum Hatası", 
                               f"Kurulum sırasında hata oluştu:\\n\\n{{str(e)}}")
            self.install_btn.config(state='normal', text="Kurulumu Başlat")
    
    def check_system(self):
        """Sistem uyumluluğu kontrol et"""
        import platform
        
        if platform.system() != "Windows":
            raise Exception("Bu kurulum sadece Windows sistemlerde çalışır!")
        
        if platform.machine() != "AMD64":
            raise Exception("Bu kurulum sadece 64-bit sistemlerde çalışır!")
    
    def check_python(self):
        """Python kurulu mu kontrol et"""
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and "Python 3." in result.stdout:
                version = result.stdout.strip().split()[1]
                major, minor = map(int, version.split('.')[:2])
                return major == 3 and minor >= 8
            return False
        except:
            return False
    
    def check_vcredist(self):
        """Visual C++ Redistributable kurulu mu kontrol et"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64")
            version, _ = winreg.QueryValueEx(key, "Version")
            winreg.CloseKey(key)
            
            # Version 14.29+ gerekli
            ver_parts = [int(x) for x in version.split('.')]
            return ver_parts[0] >= 14 and ver_parts[1] >= 29
        except:
            return False
    
    def install_python(self):
        """Python embedded kurulumu"""
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
        python_zip = os.path.join(tempfile.gettempdir(), "python.zip")
        python_dir = os.path.join(self.dir_var.get(), "Python")
        
        # Python'u indir
        urllib.request.urlretrieve(python_url, python_zip)
        
        # Çıkar
        os.makedirs(python_dir, exist_ok=True)
        with zipfile.ZipFile(python_zip, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
        
        # pip kur
        pip_url = "https://bootstrap.pypa.io/get-pip.py"
        pip_file = os.path.join(python_dir, "get-pip.py")
        urllib.request.urlretrieve(pip_url, pip_file)
        
        # python._pth dosyasını düzenle
        pth_files = list(Path(python_dir).glob("*._pth"))
        if pth_files:
            with open(pth_files[0], 'a') as f:
                f.write("\\nimport site\\n")
        
        # pip'i çalıştır
        subprocess.run([os.path.join(python_dir, "python.exe"), pip_file],
                      check=True)
    
    def install_vcredist(self):
        """Visual C++ Redistributable kurulumu"""
        vc_url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        vc_file = os.path.join(tempfile.gettempdir(), "vc_redist.exe")
        
        urllib.request.urlretrieve(vc_url, vc_file)
        subprocess.run([vc_file, "/quiet", "/norestart"], check=True)
    
    def copy_azgelir_files(self):
        """AzGelir dosyalarını kopyala"""
        # Ana exe dosyası
        src_exe = os.path.join(self.temp_dir, "AzGelir.exe")
        dest_exe = os.path.join(self.dir_var.get(), "AzGelir.exe")
        
        if os.path.exists(src_exe):
            shutil.copy2(src_exe, dest_exe)
        
        # Logo dosyası
        src_logo = os.path.join(self.temp_dir, "logo.png")
        dest_logo = os.path.join(self.dir_var.get(), "logo.png")
        
        if os.path.exists(src_logo):
            shutil.copy2(src_logo, dest_logo)
    
    def install_python_packages(self):
        """Gerekli Python paketlerini kur"""
        python_exe = shutil.which("python")
        if not python_exe:
            python_exe = os.path.join(self.dir_var.get(), "Python", "python.exe")
        
        packages = [
            "PyQt5==5.15.9",
            "pywin32"
        ]
        
        for package in packages:
            subprocess.run([python_exe, "-m", "pip", "install", package],
                          check=True)
    
    def create_shortcuts(self):
        """Kısayollar oluştur"""
        from win32com.client import Dispatch
        
        shell = Dispatch('WScript.Shell')
        
        # Masaüstü kısayolu
        if self.desktop_var.get():
            desktop = shell.SpecialFolders("Desktop")
            shortcut = shell.CreateShortCut(os.path.join(desktop, "AzGelir.lnk"))
            shortcut.Targetpath = os.path.join(self.dir_var.get(), "AzGelir.exe")
            shortcut.WorkingDirectory = self.dir_var.get()
            shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
            shortcut.save()
        
        # Başlat menüsü kısayolu
        if self.startmenu_var.get():
            programs = shell.SpecialFolders("AllUsersPrograms")
            azgelir_folder = os.path.join(programs, "AzGelir")
            os.makedirs(azgelir_folder, exist_ok=True)
            
            shortcut = shell.CreateShortCut(os.path.join(azgelir_folder, "AzGelir.lnk"))
            shortcut.Targetpath = os.path.join(self.dir_var.get(), "AzGelir.exe")
            shortcut.WorkingDirectory = self.dir_var.get()
            shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
            shortcut.save()
    
    def create_registry_entries(self):
        """Sistem kayıtları oluştur"""
        try:
            key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir"
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            
            install_path = self.dir_var.get()
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "AzGelir")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Tamerefe")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_path)
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, 
                            f'"{install_path}\\uninstall.exe"')
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry kaydı hatası: {e}")
    
    def run(self):
        """Uygulamayı çalıştır"""
        try:
            self.root.mainloop()
        finally:
            # Geçici dosyaları temizle
            shutil.rmtree(self.temp_dir, ignore_errors=True)

def main():
    """Ana fonksiyon"""
    try:
        installer = AzGelirFullInstaller()
        installer.run()
    except Exception as e:
        print(f"Installer hatası: {{e}}")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
'''
    
    # Installer script dosyasını yaz
    with open("embedded_installer.py", "w", encoding="utf-8") as f:
        f.write(installer_script)
    
    print("✓ Embedded installer scripti oluşturuldu")

def create_build_script():
    """Build script oluştur"""
    print("📋 Build script oluşturuluyor...")
    
    build_script = """#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import base64
import urllib.request

def download_if_not_exists(url, filename):
    if not os.path.exists(filename):
        print(f"📥 {filename} indiriliyor...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ {filename} indirildi")
    else:
        print(f"✓ {filename} zaten mevcut")

def build_full_installer():
    print("🏗️ AzGelir Tam Kurulum Sistemi Oluşturuluyor")
    print("=" * 60)
    
    # 1. Ana uygulamayı derle
    print("\\n1. Ana uygulama derleniyor...")
    if not os.path.exists("dist/AzGelir.exe"):
        try:
            subprocess.check_call([sys.executable, "build_windows.py"])
            print("✓ Ana uygulama derlendi")
        except subprocess.CalledProcessError:
            print("❌ Ana uygulama derlenemedi!")
            return False
    else:
        print("✓ Ana uygulama zaten derlenmiş")
    
    # 2. Gerekli dosyaları indir
    print("\\n2. Gerekli dosyalar indiriliyor...")
    downloads = [
        {
            "url": "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip",
            "file": "python-embed.zip"
        },
        {
            "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe", 
            "file": "vc_redist.exe"
        }
    ]
    
    for item in downloads:
        download_if_not_exists(item["url"], item["file"])
    
    # 3. Embedded installer oluştur
    print("\\n3. Embedded installer oluşturuluyor...")
    
    # Ana exe'yi base64'e çevir
    with open("dist/AzGelir.exe", "rb") as f:
        azgelir_b64 = base64.b64encode(f.read()).decode()
    
    # Logo varsa base64'e çevir
    logo_b64 = ""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
    
    # Embedded installer template'ini güncelle
    with open("embedded_installer.py", "r", encoding="utf-8") as f:
        template = f.read()
    
    # Base64 verilerini template'e gömme
    template = template.replace('AZGELIR_EXE_B64 = ""', f'AZGELIR_EXE_B64 = "{azgelir_b64}"')
    template = template.replace('LOGO_PNG_B64 = ""', f'LOGO_PNG_B64 = "{logo_b64}"')
    
    # Güncellenmiş template'i yaz
    with open("final_installer.py", "w", encoding="utf-8") as f:
        f.write(template)
    
    print("✓ Embedded installer scripti hazırlandı")
    
    # 4. Tek dosya exe oluştur
    print("\\n4. Tek dosya exe derleniyor...")
    
    icon_param = "--icon=logo.png" if os.path.exists("logo.png") else ""
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name=AzGelir_FullSetup",
        icon_param,
        "--distpath=.",
        "final_installer.py"
    ]
    
    cmd = [x for x in cmd if x]  # Boş parametreleri kaldır
    
    try:
        subprocess.check_call(cmd)
        print("✓ Tek dosya exe oluşturuldu: AzGelir_FullSetup.exe")
    except subprocess.CalledProcessError:
        print("❌ Exe oluşturulamadı!")
        return False
    
    # 5. Temizlik
    print("\\n5. Temizlik yapılıyor...")
    cleanup_files = [
        "final_installer.py",
        "final_installer.spec", 
        "build",
        "__pycache__"
    ]
    
    for item in cleanup_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    print("✓ Temizlik tamamlandı")
    
    print("\\n" + "=" * 60)
    print("🎉 KURULUM DOSYASI BAŞARIYLA OLUŞTURULDU!")
    print("=" * 60)
    print("\\n📁 Oluşturulan dosya:")
    print("   • AzGelir_FullSetup.exe - Sıfırdan kurulum (tek dosya)")
    print("\\n🚀 Kullanım:")
    print("   • Bu dosyayı herhangi bir Windows bilgisayarına kopyalayın")
    print("   • Yönetici olarak çalıştırın")  
    print("   • Python dahil her şey otomatik kurulacak")
    print("\\n💡 Dosya boyutu: ~50-100MB (tüm bağımlılıklar dahil)")
    
    return True

if __name__ == "__main__":
    success = build_full_installer()
    if not success:
        input("\\nHata oluştu. Çıkmak için Enter'a basın...")
        sys.exit(1)
    else:
        input("\\nTamamlandı! Çıkmak için Enter'a basın...")
"""
    
    with open("build_full_setup.py", "w", encoding="utf-8") as f:
        f.write(build_script)
    
    print("✓ Build script oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🚀 AzGelir Sıfırdan Kurulum Sistemi Oluşturucu")
    print("=" * 60)
    print("\nBu araç sıfırdan bilgisayarda çalışacak tek dosya kurulum exe'si oluşturur.")
    print("Python dahil her şeyi otomatik kurar!")
    print()
    
    # Tüm gerekli dosyaları oluştur
    create_embedded_installer()
    create_build_script()
    
    print("\n" + "=" * 60)
    print("✅ TÜM KURULUM DOSYALARI OLUŞTURULDU!")
    print("=" * 60)
    
    print("\n📋 Oluşturulan dosyalar:")
    print("   • create_full_installer.py - Ana kurulum sistemi")
    print("   • embedded_installer.py - Gömülü dosyalı installer")
    print("   • build_full_setup.py - Tek dosya exe oluşturucu")
    print("   • create_single_exe_installer.bat - Batch build script")
    
    print("\n🚀 Kullanım adımları:")
    print("   1. Ana uygulamayı derleyin: python build_windows.py")
    print("   2. Kurulum exe'si oluşturun: python build_full_setup.py")
    print("   3. Veya batch ile: create_single_exe_installer.bat")
    
    print("\n💡 Sonuç:")
    print("   • AzGelir_FullSetup.exe - Sıfırdan kurulum dosyası")
    print("   • Bu dosya herhangi bir Windows PC'de çalışır")
    print("   • Python, VC++, PyQt5 dahil her şeyi kurar")
    print("   • Yaklaşık 50-100MB boyutunda")

if __name__ == "__main__":
    main()
