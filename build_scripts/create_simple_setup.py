#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Sıfırdan Kurulum Exe Oluşturucu
Tek dosyada Python dahil her şeyi kuran installer
"""

import os
import sys
import subprocess
import base64
import shutil
from pathlib import Path

def create_simple_installer():
    """Basit ama etkili installer oluştur"""
    
    print("🚀 AzGelir Sıfırdan Kurulum Exe'si Oluşturuluyor...")
    print("=" * 60)
    
    # 1. Ana uygulama kontrolü
    if not os.path.exists("dist/AzGelir.exe"):
        print("❌ Önce ana uygulamayı derleyin: python build_windows.py")
        return False
    
    # 2. Kurulum scripti oluştur
    print("\n📝 Kurulum scripti oluşturuluyor...")
    
    installer_code = '''import sys
import os
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
import base64
import tkinter as tk
from tkinter import ttk, messagebox
import threading
try:
    import winreg
except ImportError:
    import _winreg as winreg

class SimpleInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AzGelir Kurulum")
        self.root.geometry("500x400")
        self.install_dir = "C:\\\\Program Files\\\\AzGelir"
        self.create_ui()
        
    def create_ui(self):
        # Ana frame
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        tk.Label(frame, text="AzGelir Kurulum Sihirbazı", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(frame, text="Bu kurulum Python dahil tüm bileşenleri kuracaktır.\\n"
                           "İşlem 5-10 dakika sürebilir.", 
                font=("Arial", 10)).pack(pady=10)
        
        # Kurulum dizini
        tk.Label(frame, text="Kurulum Dizini:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.dir_var = tk.StringVar(value=self.install_dir)
        tk.Entry(frame, textvariable=self.dir_var, width=60).pack(fill='x', pady=5)
        
        # Seçenekler
        self.desktop_var = tk.BooleanVar(value=True)
        self.startmenu_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(frame, text="Masaüstü kısayolu", 
                      variable=self.desktop_var).pack(anchor='w', pady=2)
        tk.Checkbutton(frame, text="Başlat menüsü kısayolu", 
                      variable=self.startmenu_var).pack(anchor='w', pady=2)
        
        # Progress
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=20)
        
        self.status = tk.Label(frame, text="Kuruluma hazır")
        self.status.pack(pady=5)
        
        # Butonlar
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=20)
        
        self.install_btn = tk.Button(btn_frame, text="Kurulumu Başlat", 
                                   command=self.start_install,
                                   bg='green', fg='white', font=('Arial', 10, 'bold'))
        self.install_btn.pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Çıkış", command=self.root.quit,
                 bg='red', fg='white').pack(side='left', padx=5)
    
    def start_install(self):
        self.install_btn.config(state='disabled')
        self.progress.start()
        thread = threading.Thread(target=self.install)
        thread.daemon = True
        thread.start()
    
    def update_status(self, text):
        self.status.config(text=text)
        self.root.update()
    
    def install(self):
        try:
            # Kurulum dizini oluştur
            self.update_status("Kurulum dizini hazırlanıyor...")
            os.makedirs(self.dir_var.get(), exist_ok=True)
            
            # Python kontrol et
            self.update_status("Python kontrol ediliyor...")
            if not self.check_python():
                self.update_status("Python kuruluyor...")
                self.install_python()
            
            # AzGelir dosyalarını kopyala
            self.update_status("AzGelir dosyaları kopyalanıyor...")
            self.extract_azgelir()
            
            # Python paketleri kur
            self.update_status("Python paketleri kuruluyor...")
            self.install_packages()
            
            # Kısayollar oluştur
            self.update_status("Kısayollar oluşturuluyor...")
            self.create_shortcuts()
            
            # Registry
            self.update_status("Sistem kayıtları...")
            self.create_registry()
            
            self.progress.stop()
            self.update_status("✅ Kurulum tamamlandı!")
            
            messagebox.showinfo("Tamamlandı", "AzGelir başarıyla kuruldu!")
            
            if messagebox.askyesno("Çalıştır", "AzGelir'i şimdi açmak istiyor musunuz?"):
                subprocess.Popen([os.path.join(self.dir_var.get(), "AzGelir.exe")])
            
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Hata", f"Kurulum hatası: {str(e)}")
            self.install_btn.config(state='normal')
    
    def check_python(self):
        try:
            result = subprocess.run(['python', '--version'], capture_output=True, text=True)
            return result.returncode == 0 and "Python 3." in result.stdout
        except:
            return False
    
    def install_python(self):
        # Python embedded indir ve kur
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
        python_zip = os.path.join(tempfile.gettempdir(), "python.zip")
        python_dir = os.path.join(self.dir_var.get(), "Python")
        
        urllib.request.urlretrieve(python_url, python_zip)
        
        os.makedirs(python_dir, exist_ok=True)
        with zipfile.ZipFile(python_zip, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
        
        # pip kur
        pip_url = "https://bootstrap.pypa.io/get-pip.py"
        pip_file = os.path.join(python_dir, "get-pip.py")
        urllib.request.urlretrieve(pip_url, pip_file)
        
        # python._pth düzenle
        for pth_file in os.listdir(python_dir):
            if pth_file.endswith("._pth"):
                with open(os.path.join(python_dir, pth_file), 'a') as f:
                    f.write("\\nimport site\\n")
                break
        
        subprocess.run([os.path.join(python_dir, "python.exe"), pip_file])
    
    def extract_azgelir(self):
        # Gömülü AzGelir.exe'yi çıkar
        azgelir_data = base64.b64decode(AZGELIR_DATA)
        azgelir_path = os.path.join(self.dir_var.get(), "AzGelir.exe")
        with open(azgelir_path, 'wb') as f:
            f.write(azgelir_data)
    
    def install_packages(self):
        python_exe = shutil.which("python")
        if not python_exe:
            python_exe = os.path.join(self.dir_var.get(), "Python", "python.exe")
        
        packages = ["PyQt5==5.15.9", "pywin32"]
        for package in packages:
            subprocess.run([python_exe, "-m", "pip", "install", package], 
                          capture_output=True)
    
    def create_shortcuts(self):
        try:
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            
            if self.desktop_var.get():
                desktop = shell.SpecialFolders("Desktop")
                shortcut = shell.CreateShortCut(os.path.join(desktop, "AzGelir.lnk"))
                shortcut.Targetpath = os.path.join(self.dir_var.get(), "AzGelir.exe")
                shortcut.save()
            
            if self.startmenu_var.get():
                programs = shell.SpecialFolders("AllUsersPrograms")
                folder = os.path.join(programs, "AzGelir")
                os.makedirs(folder, exist_ok=True)
                shortcut = shell.CreateShortCut(os.path.join(folder, "AzGelir.lnk"))
                shortcut.Targetpath = os.path.join(self.dir_var.get(), "AzGelir.exe")
                shortcut.save()
        except:
            pass  # pywin32 yoksa kısayol olmadan devam et
    
    def create_registry(self):
        try:
            key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir"
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "AzGelir")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Tamerefe")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.dir_var.get())
            
            winreg.CloseKey(key)
        except:
            pass  # Registry yazma yetkisi yoksa sessizce devam et
    
    def run(self):
        self.root.mainloop()

# Gömülü AzGelir.exe verisi (Base64)
AZGELIR_DATA = """PLACEHOLDER_FOR_AZGELIR_DATA"""

if __name__ == "__main__":
    try:
        installer = SimpleInstaller()
        installer.run()
    except Exception as e:
        print(f"Installer hatası: {e}")
        input("Çıkmak için Enter'a basın...")
'''
    
    # 3. AzGelir.exe'yi base64'e çevir
    print("📦 AzGelir.exe gömülüyor...")
    with open("dist/AzGelir.exe", "rb") as f:
        azgelir_data = base64.b64encode(f.read()).decode()
    
    # Base64 veriyi script'e gömme
    installer_code = installer_code.replace('PLACEHOLDER_FOR_AZGELIR_DATA', azgelir_data)
    
    # 4. Installer script dosyasını yaz
    with open("simple_installer.py", "w", encoding="utf-8") as f:
        f.write(installer_code)
    
    print("✓ Installer scripti hazırlandı")
    
    # 5. PyInstaller ile exe oluştur
    print("\n🔨 Tek dosya exe oluşturuluyor...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=AzGelir_Setup",
        "--distpath=.",
        "simple_installer.py"
    ]
    
    if os.path.exists("logo.png"):
        cmd.insert(-1, "--icon=logo.png")
    
    try:
        subprocess.check_call(cmd)
        print("✅ AzGelir_Setup.exe oluşturuldu!")
    except subprocess.CalledProcessError:
        print("❌ Exe oluşturulamadı!")
        return False
    
    # 6. Temizlik
    print("\n🧹 Temizlik yapılıyor...")
    cleanup_items = [
        "simple_installer.py", 
        "simple_installer.spec",
        "build",
        "__pycache__"
    ]
    
    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    print("✓ Temizlik tamamlandı")
    
    # Sonuç
    file_size = os.path.getsize("AzGelir_Setup.exe") / 1024 / 1024
    
    print("\n" + "=" * 60)
    print("🎉 KURULUM DOSYASI BAŞARIYLA OLUŞTURULDU!")
    print("=" * 60)
    print(f"\n📁 Dosya: AzGelir_Setup.exe ({file_size:.1f} MB)")
    print("\n🚀 Özellikler:")
    print("   • Tek dosya - bağımsız çalışır")
    print("   • Python dahil her şeyi otomatik kurar")
    print("   • Sıfırdan bilgisayarda çalışır")
    print("   • Grafik arayüzlü kurulum sihirbazı")
    print("   • Masaüstü ve Başlat menüsü kısayolları")
    print("\n💡 Kullanım:")
    print("   • Herhangi bir Windows PC'ye kopyalayın")
    print("   • Yönetici olarak çalıştırın")
    print("   • Kurulum sihirbazını takip edin")
    
    return True

def main():
    """Ana fonksiyon"""
    print("🛠️ AzGelir Sıfırdan Kurulum Exe Oluşturucu")
    print("=" * 50)
    
    if create_simple_installer():
        print("\n✅ İşlem tamamlandı!")
    else:
        print("\n❌ İşlem başarısız!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
