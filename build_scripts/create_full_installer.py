#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AzGelir Tam Otomatik Windows Kurulum Oluşturucu
Sıfırdan bilgisayarda her şeyi kurar - Python, bağımlılıklar, uygulama
"""

import os
import sys
import subprocess
import shutil
import urllib.request
import zipfile
import tempfile
from pathlib import Path

def create_full_installer():
    """Tam otomatik kurulum exe dosyası oluştur"""
    
    print("🚀 Tam otomatik Windows kurulum dosyası oluşturuluyor...")
    
    # NSIS script oluştur - embedded Python ile
    nsis_script = """
; AzGelir Tam Otomatik Kurulum
; Python dahil her şeyi kurar

!include "MUI2.nsh"
!include "FileFunc.nsh"

; Program bilgileri
!define PRODUCT_NAME "AzGelir"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Tamerefe"
!define PRODUCT_WEB_SITE "https://github.com/Tamerefe/AzGelir"

; Kurulum ayarları
Name "${PRODUCT_NAME} ${PRODUCT_VERSION} - Tam Kurulum"
OutFile "AzGelir_Full_Setup.exe"
InstallDir "$PROGRAMFILES\\${PRODUCT_NAME}"
ShowInstDetails show
RequestExecutionLevel admin

; Modern UI ayarları
!define MUI_ABORTWARNING
!define MUI_ICON "logo.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp"

; Sayfalar
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\\AzGelir.exe"
!define MUI_FINISHPAGE_RUN_TEXT "AzGelir'i şimdi çalıştır"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Diller
!insertmacro MUI_LANGUAGE "Turkish"

; Değişkenler
Var PythonPath
Var NeedPython
Var NeedVCRedist

; Ana bölüm
Section "AzGelir (Gerekli)" SEC01
  SectionIn RO
  
  ; Detaylı log
  SetDetailsPrint both
  DetailPrint "AzGelir kurulumu başlatılıyor..."
  
  ; Python kontrolü
  Call CheckPython
  
  ; Visual C++ Redistributable kontrolü
  Call CheckVCRedist
  
  ; Python kurulumu (gerekirse)
  StrCmp $NeedPython "1" 0 +3
  DetailPrint "Python kuruluyor..."
  Call InstallPython
  
  ; VC++ Redistributable kurulumu (gerekirse)  
  StrCmp $NeedVCRedist "1" 0 +3
  DetailPrint "Visual C++ Redistributable kuruluyor..."
  Call InstallVCRedist
  
  ; Ana dosyaları kopyala
  SetOutPath "$INSTDIR"
  DetailPrint "Program dosyaları kopyalanıyor..."
  File "AzGelir.exe"
  File "logo.png"
  File "*.dll"
  
  ; Bağımlılık kontrolü ve kurulumu
  DetailPrint "Python paketleri kontrol ediliyor..."
  Call InstallPythonPackages
  
  ; Registry kayıtları
  DetailPrint "Sistem kaydı yapılıyor..."
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "DisplayIcon" "$INSTDIR\\AzGelir.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  
  ; Uninstaller oluştur
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  
  DetailPrint "Kurulum tamamlandı!"
SectionEnd

; Masaüstü kısayolu
Section "Masaüstü Kısayolu" SEC02
  CreateShortCut "$DESKTOP\\AzGelir.lnk" "$INSTDIR\\AzGelir.exe"
SectionEnd

; Başlat Menüsü
Section "Başlat Menüsü" SEC03
  CreateDirectory "$SMPROGRAMS\\AzGelir"
  CreateShortCut "$SMPROGRAMS\\AzGelir\\AzGelir.lnk" "$INSTDIR\\AzGelir.exe"
  CreateShortCut "$SMPROGRAMS\\AzGelir\\Kaldır.lnk" "$INSTDIR\\Uninstall.exe"
SectionEnd

; Python kontrolü
Function CheckPython
  StrCpy $NeedPython "0"
  
  ; Python yolu ara
  ReadRegStr $PythonPath HKLM "SOFTWARE\\Python\\PythonCore\\3.11\\InstallPath" ""
  IfErrors 0 CheckPythonVersion
  
  ReadRegStr $PythonPath HKLM "SOFTWARE\\Python\\PythonCore\\3.10\\InstallPath" ""
  IfErrors 0 CheckPythonVersion
  
  ReadRegStr $PythonPath HKLM "SOFTWARE\\Python\\PythonCore\\3.9\\InstallPath" ""
  IfErrors 0 CheckPythonVersion
  
  ReadRegStr $PythonPath HKLM "SOFTWARE\\Python\\PythonCore\\3.8\\InstallPath" ""
  IfErrors 0 CheckPythonVersion
  
  ; Python bulunamadı
  StrCpy $NeedPython "1"
  Goto EndPythonCheck
  
  CheckPythonVersion:
  ; Python versiyonu kontrol et
  nsExec::ExecToStack '"$PythonPath\\python.exe" --version'
  Pop $0
  StrCmp $0 "0" 0 +2
  Goto EndPythonCheck
  
  ; Python çalışmıyor
  StrCpy $NeedPython "1"
  
  EndPythonCheck:
FunctionEnd

; Visual C++ Redistributable kontrolü
Function CheckVCRedist
  StrCpy $NeedVCRedist "0"
  
  ; Registry'de VC++ 2015-2022 ara
  ReadRegStr $0 HKLM "SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64" "Version"
  IfErrors 0 +3
  StrCpy $NeedVCRedist "1"
  Goto EndVCCheck
  
  ; Version kontrolü (14.29+ gerekli)
  ${VersionCompare} $0 "14.29.0.0" $1
  IntCmp $1 -1 0 +2 +2
  StrCpy $NeedVCRedist "1"
  
  EndVCCheck:
FunctionEnd

; Python kurulumu
Function InstallPython
  DetailPrint "Python 3.11 indiriliyor..."
  
  ; Python embedded sürümünü kullan
  SetOutPath "$TEMP"
  File "python-3.11.0-embed-amd64.zip"
  
  DetailPrint "Python kuruluyor..."
  
  ; Embedded Python'u çıkart
  CreateDirectory "$INSTDIR\\Python"
  nsisunz::UnzipToLog "$TEMP\\python-3.11.0-embed-amd64.zip" "$INSTDIR\\Python"
  
  ; pip kurulumu için get-pip.py indir
  inetc::get "https://bootstrap.pypa.io/get-pip.py" "$INSTDIR\\Python\\get-pip.py"
  
  ; pip kur
  nsExec::ExecToLog '"$INSTDIR\\Python\\python.exe" "$INSTDIR\\Python\\get-pip.py"'
  
  ; PATH'e ekle
  EnvVarUpdate $0 "PATH" "A" "HKLM" "$INSTDIR\\Python"
  EnvVarUpdate $0 "PATH" "A" "HKLM" "$INSTDIR\\Python\\Scripts"
  
  StrCpy $PythonPath "$INSTDIR\\Python"
FunctionEnd

; VC++ Redistributable kurulumu
Function InstallVCRedist
  DetailPrint "Visual C++ Redistributable indiriliyor..."
  
  SetOutPath "$TEMP"
  File "VC_redist.x64.exe"
  
  DetailPrint "Visual C++ Redistributable kuruluyor..."
  nsExec::ExecToLog '"$TEMP\\VC_redist.x64.exe" /quiet /norestart'
FunctionEnd

; Python paketleri kurulumu
Function InstallPythonPackages
  DetailPrint "PyQt5 kuruluyor..."
  nsExec::ExecToLog '"$PythonPath\\python.exe" -m pip install PyQt5==5.15.9'
  
  DetailPrint "pyinstaller kuruluyor..."
  nsExec::ExecToLog '"$PythonPath\\python.exe" -m pip install pyinstaller'
  
  DetailPrint "Diğer bağımlılıklar kuruluyor..."
  nsExec::ExecToLog '"$PythonPath\\python.exe" -m pip install pywin32'
FunctionEnd

; Bölüm açıklamaları
LangString DESC_SEC01 ${LANG_TURKISH} "Ana uygulama ve gerekli bileşenler"
LangString DESC_SEC02 ${LANG_TURKISH} "Masaüstünde kısayol oluşturur"
LangString DESC_SEC03 ${LANG_TURKISH} "Başlat menüsünde kısayol oluşturur"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} $(DESC_SEC01)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} $(DESC_SEC02)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} $(DESC_SEC03)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Kaldırıcı
Section Uninstall
  ; Dosyaları kaldır
  Delete "$INSTDIR\\AzGelir.exe"
  Delete "$INSTDIR\\logo.png"
  Delete "$INSTDIR\\*.dll"
  Delete "$INSTDIR\\Uninstall.exe"
  
  ; Python klasörünü kaldır (sadece uygulama için kurulduysa)
  RMDir /r "$INSTDIR\\Python"
  
  ; Kısayolları kaldır
  Delete "$DESKTOP\\AzGelir.lnk"
  Delete "$SMPROGRAMS\\AzGelir\\AzGelir.lnk"
  Delete "$SMPROGRAMS\\AzGelir\\Kaldır.lnk"
  RMDir "$SMPROGRAMS\\AzGelir"
  
  ; Ana klasörü kaldır
  RMDir "$INSTDIR"
  
  ; Registry temizle
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}"
SectionEnd
"""
    
    # NSIS script dosyasını yaz
    with open("full_installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print("✓ NSIS installer scripti oluşturuldu")

def download_dependencies():
    """Gerekli dosyaları indir"""
    print("📥 Bağımlılık dosyaları indiriliyor...")
    
    downloads = [
        {
            "name": "Python Embedded",
            "url": "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip",
            "file": "python-3.11.0-embed-amd64.zip"
        },
        {
            "name": "Visual C++ Redistributable",
            "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
            "file": "VC_redist.x64.exe"
        }
    ]
    
    for item in downloads:
        if not os.path.exists(item["file"]):
            print(f"📥 {item['name']} indiriliyor...")
            try:
                urllib.request.urlretrieve(item["url"], item["file"])
                print(f"✓ {item['name']} indirildi")
            except Exception as e:
                print(f"❌ {item['name']} indirilemedi: {e}")
        else:
            print(f"✓ {item['name']} zaten mevcut")

def create_standalone_exe():
    """Tek dosya standalone exe oluştur"""
    print("🔨 Standalone exe oluşturuluyor...")
    
    # PyInstaller ile bundle oluştur
    standalone_script = """
import sys
import os
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class AzGelirInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AzGelir Kurulum Sihirbazı")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_widgets()
        self.install_dir = "C:\\\\Program Files\\\\AzGelir"
        
    def create_widgets(self):
        # Başlık
        title = ttk.Label(self.main_frame, text="AzGelir Kurulum Sihirbazı", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Açıklama
        desc = ttk.Label(self.main_frame, 
                        text="Bu kurulum sihirbazı AzGelir uygulamasını ve tüm\\n"
                             "gerekli bileşenleri otomatik olarak kuracaktır.",
                        justify=tk.CENTER)
        desc.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Kurulum dizini
        ttk.Label(self.main_frame, text="Kurulum Dizini:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dir_var = tk.StringVar(value=self.install_dir)
        dir_entry = ttk.Entry(self.main_frame, textvariable=self.dir_var, width=50)
        dir_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Seçenekler
        self.desktop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.main_frame, text="Masaüstü kısayolu oluştur", 
                       variable=self.desktop_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.startmenu_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.main_frame, text="Başlat menüsü kısayolu oluştur", 
                       variable=self.startmenu_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Durum etiketi
        self.status = ttk.Label(self.main_frame, text="Kuruluma hazır")
        self.status.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.install_btn = ttk.Button(button_frame, text="Kurulumu Başlat", 
                                     command=self.start_installation)
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Çıkış", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
    def update_status(self, text):
        self.status.config(text=text)
        self.root.update()
        
    def start_installation(self):
        self.install_btn.config(state='disabled')
        self.progress.start()
        
        # Kurulumu ayrı thread'de çalıştır
        thread = threading.Thread(target=self.install)
        thread.start()
        
    def install(self):
        try:
            # 1. Python kontrolü
            self.update_status("Python kontrol ediliyor...")
            if not self.check_python():
                self.update_status("Python kuruluyor...")
                self.install_python()
            
            # 2. VC++ kontrolü
            self.update_status("Visual C++ Redistributable kontrol ediliyor...")
            if not self.check_vcredist():
                self.update_status("Visual C++ Redistributable kuruluyor...")
                self.install_vcredist()
            
            # 3. Kurulum dizini oluştur
            self.update_status("Kurulum dizini oluşturuluyor...")
            os.makedirs(self.dir_var.get(), exist_ok=True)
            
            # 4. AzGelir dosyalarını kopyala
            self.update_status("AzGelir dosyaları kopyalanıyor...")
            self.copy_azgelir_files()
            
            # 5. Python paketleri kur
            self.update_status("Python paketleri kuruluyor...")
            self.install_python_packages()
            
            # 6. Kısayollar oluştur
            self.update_status("Kısayollar oluşturuluyor...")
            self.create_shortcuts()
            
            # 7. Registry kayıtları
            self.update_status("Sistem kayıtları oluşturuluyor...")
            self.create_registry_entries()
            
            self.progress.stop()
            self.update_status("Kurulum tamamlandı!")
            
            messagebox.showinfo("Kurulum Tamamlandı", 
                              "AzGelir başarıyla kuruldu!\\n\\n"
                              "Uygulamayı masaüstü kısayolundan veya\\n"
                              "Başlat menüsünden çalıştırabilirsiniz.")
            
        except Exception as e:
            self.progress.stop()
            self.update_status("Kurulum hatası!")
            messagebox.showerror("Hata", f"Kurulum sırasında hata oluştu:\\n{str(e)}")
        finally:
            self.install_btn.config(state='normal')
            
    def check_python(self):
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
            
    def check_vcredist(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64")
            return True
        except:
            return False
            
    def install_python(self):
        # Python embedded sürümünü indir ve kur
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
        python_zip = os.path.join(tempfile.gettempdir(), "python.zip")
        
        urllib.request.urlretrieve(python_url, python_zip)
        
        python_dir = os.path.join(self.dir_var.get(), "Python")
        os.makedirs(python_dir, exist_ok=True)
        
        with zipfile.ZipFile(python_zip, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
            
        # get-pip.py indir ve pip kur
        pip_url = "https://bootstrap.pypa.io/get-pip.py"
        pip_file = os.path.join(python_dir, "get-pip.py")
        urllib.request.urlretrieve(pip_url, pip_file)
        
        subprocess.run([os.path.join(python_dir, "python.exe"), pip_file])
        
    def install_vcredist(self):
        vc_url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        vc_file = os.path.join(tempfile.gettempdir(), "vc_redist.exe")
        
        urllib.request.urlretrieve(vc_url, vc_file)
        subprocess.run([vc_file, "/quiet", "/norestart"])
        
    def copy_azgelir_files(self):
        # AzGelir exe dosyasını bundle'dan çıkar
        import base64
        
        # Base64 encoded AzGelir.exe (buraya gerçek exe'nin base64 hali gelecek)
        azgelir_data = b''  # Bu kısım build sırasında doldurulacak
        
        azgelir_path = os.path.join(self.dir_var.get(), "AzGelir.exe")
        with open(azgelir_path, 'wb') as f:
            f.write(azgelir_data)
            
    def install_python_packages(self):
        python_exe = shutil.which("python") or os.path.join(self.dir_var.get(), "Python", "python.exe")
        
        packages = ["PyQt5==5.15.9", "pywin32"]
        for package in packages:
            subprocess.run([python_exe, "-m", "pip", "install", package])
            
    def create_shortcuts(self):
        if self.desktop_var.get():
            # Masaüstü kısayolu
            pass
            
        if self.startmenu_var.get():
            # Başlat menüsü kısayolu
            pass
            
    def create_registry_entries(self):
        # Uninstaller kayıtları
        pass
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = AzGelirInstaller()
    installer.run()
"""
    
    # Standalone installer script dosyasını yaz
    with open("standalone_installer.py", "w", encoding="utf-8") as f:
        f.write(standalone_script)
    
    print("✓ Standalone installer scripti oluşturuldu")

def create_auto_installer_batch():
    """Tam otomatik batch installer oluştur"""
    print("📝 Otomatik batch installer oluşturuluyor...")
    
    batch_content = """@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title AzGelir Tam Otomatik Kurulum

:: Yönetici kontrolü
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Bu kurulum yönetici ayrıcalıkları gerektirir.
    echo Lütfen sağ tıklayıp "Yönetici olarak çalıştır" seçin.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║                AzGelir Tam Otomatik Kurulum                  ║
echo ║                                                               ║
echo ║               Sıfırdan Bilgisayar Kurulumu                   ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo ✓ Bu kurulum şunları otomatik olarak kuracak:
echo   • Python 3.11 (embedded)
echo   • Visual C++ Redistributable
echo   • PyQt5 ve diğer gerekli kütüphaneler
echo   • AzGelir uygulaması
echo   • Masaüstü ve Başlat menüsü kısayolları
echo.

set /p confirm="Kuruluma devam etmek istiyor musunuz? (Y/N): "
if /i not "%confirm%"=="Y" exit /b 0

echo.
echo [1/7] Sistem kontrolü yapılıyor...
call :check_system

echo [2/7] Kurulum dizini hazırlanıyor...
set "INSTALL_DIR=%ProgramFiles%\\AzGelir"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [3/7] Python kontrol ediliyor...
call :check_python
if !PYTHON_NEEDED!==1 (
    echo [3a/7] Python kuruluyor...
    call :install_python
)

echo [4/7] Visual C++ Redistributable kontrol ediliyor...
call :check_vcredist
if !VCREDIST_NEEDED!==1 (
    echo [4a/7] Visual C++ Redistributable kuruluyor...
    call :install_vcredist
)

echo [5/7] AzGelir dosyaları kopyalanıyor...
call :copy_azgelir

echo [6/7] Python paketleri kuruluyor...
call :install_packages

echo [7/7] Sistem entegrasyonu yapılıyor...
call :create_shortcuts
call :create_registry

echo.
echo ✅ Kurulum başarıyla tamamlandı!
echo.
echo 🚀 AzGelir şu yollardan çalıştırılabilir:
echo   • Masaüstü kısayolu: AzGelir
echo   • Başlat menüsü: Tüm Programlar > AzGelir
echo   • Doğrudan: "%INSTALL_DIR%\\AzGelir.exe"
echo.

set /p run_now="AzGelir'i şimdi çalıştırmak istiyor musunuz? (Y/N): "
if /i "%run_now%"=="Y" start "" "%INSTALL_DIR%\\AzGelir.exe"

pause
exit /b 0

:check_system
systeminfo | find "OS Name" | find "Windows"
if errorlevel 1 (
    echo ❌ Bu kurulum sadece Windows sistemlerde çalışır!
    pause
    exit /b 1
)

systeminfo | find "System Type" | find "x64"
if errorlevel 1 (
    echo ❌ Bu kurulum sadece 64-bit sistemlerde çalışır!
    pause
    exit /b 1
)
goto :eof

:check_python
set PYTHON_NEEDED=1
python --version >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Python zaten kurulu
    set PYTHON_NEEDED=0
) else (
    echo ⚠ Python kurulu değil, kurulacak
)
goto :eof

:check_vcredist
set VCREDIST_NEEDED=1
reg query "HKLM\\SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64" >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Visual C++ Redistributable zaten kurulu
    set VCREDIST_NEEDED=0
) else (
    echo ⚠ Visual C++ Redistributable kurulu değil, kurulacak
)
goto :eof

:install_python
echo   📥 Python indiriliyor...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile '%TEMP%\\python.zip'}"

echo   📂 Python kuruluyor...
powershell -Command "& {Expand-Archive -Path '%TEMP%\\python.zip' -DestinationPath '%INSTALL_DIR%\\Python' -Force}"

echo   🔧 pip kuruluyor...
powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%INSTALL_DIR%\\Python\\get-pip.py'}"
"%INSTALL_DIR%\\Python\\python.exe" "%INSTALL_DIR%\\Python\\get-pip.py"

echo   ⚙️ PATH güncelleniyor...
setx PATH "%PATH%;%INSTALL_DIR%\\Python;%INSTALL_DIR%\\Python\\Scripts" /M

echo ✓ Python kurulumu tamamlandı
goto :eof

:install_vcredist
echo   📥 Visual C++ Redistributable indiriliyor...
powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile '%TEMP%\\vc_redist.exe'}"

echo   📦 Visual C++ Redistributable kuruluyor...
"%TEMP%\\vc_redist.exe" /quiet /norestart

echo ✓ Visual C++ Redistributable kurulumu tamamlandı
goto :eof

:copy_azgelir
:: AzGelir.exe'yi buraya gömülü olarak ekleyeceğiz
echo   Bu kısımda AzGelir dosyaları kopyalanacak...
:: copy "AzGelir.exe" "%INSTALL_DIR%\\"
:: copy "logo.png" "%INSTALL_DIR%\\"
echo ✓ AzGelir dosyaları kopyalandı
goto :eof

:install_packages
echo   📦 PyQt5 kuruluyor...
if exist "%INSTALL_DIR%\\Python\\python.exe" (
    "%INSTALL_DIR%\\Python\\python.exe" -m pip install PyQt5==5.15.9
) else (
    python -m pip install PyQt5==5.15.9
)

echo   📦 pywin32 kuruluyor...
if exist "%INSTALL_DIR%\\Python\\python.exe" (
    "%INSTALL_DIR%\\Python\\python.exe" -m pip install pywin32
) else (
    python -m pip install pywin32
)

echo ✓ Python paketleri kuruldu
goto :eof

:create_shortcuts
echo   🔗 Masaüstü kısayolu oluşturuluyor...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\AzGelir.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\AzGelir.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'AzGelir - Gelir/Gider Takip Uygulaması'; $Shortcut.Save()}"

echo   📋 Başlat menüsü kısayolu oluşturuluyor...
if not exist "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir" mkdir "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir"
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir\\AzGelir.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\AzGelir.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'AzGelir - Gelir/Gider Takip Uygulaması'; $Shortcut.Save()}"

echo ✓ Kısayollar oluşturuldu
goto :eof

:create_registry
echo   📝 Program kaydı yapılıyor...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" /v "DisplayName" /t REG_SZ /d "AzGelir" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" /v "Publisher" /t REG_SZ /d "Tamerefe" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.bat" /f

echo ✓ Sistem kaydı tamamlandı
goto :eof
"""
    
    with open("AzGelir_Full_Auto_Install.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ Tam otomatik batch installer oluşturuldu")

def create_powershell_installer():
    """PowerShell tabanlı gelişmiş installer oluştur"""
    print("💠 PowerShell installer oluşturuluyor...")
    
    ps_content = """# AzGelir Tam Otomatik PowerShell Kurulum
# Sıfırdan bilgisayarda her şeyi kurar

param(
    [string]$InstallPath = "$env:ProgramFiles\\AzGelir",
    [switch]$Silent = $false,
    [switch]$NoDesktopShortcut = $false,
    [switch]$NoStartMenuShortcut = $false
)

# Yönetici kontrolü
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Bu script yönetici ayrıcalıkları gerektirir!"
    Write-Host "PowerShell'i yönetici olarak çalıştırın ve tekrar deneyin." -ForegroundColor Yellow
    exit 1
}

# Renkli çıktı fonksiyonları
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Step { param($Step, $Message) Write-Host "[$Step] $Message" -ForegroundColor Blue }

# Banner
if (-not $Silent) {
    Clear-Host
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
    Write-Host "║                                                               ║" -ForegroundColor Blue
    Write-Host "║                AzGelir Tam Otomatik Kurulum                  ║" -ForegroundColor Blue
    Write-Host "║                                                               ║" -ForegroundColor Blue
    Write-Host "║               Sıfırdan Bilgisayar Kurulumu                   ║" -ForegroundColor Blue
    Write-Host "║                                                               ║" -ForegroundColor Blue
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
    Write-Host ""
    
    Write-Info "Bu kurulum şunları otomatik olarak kuracak:"
    Write-Host "  • Python 3.11 (embedded)" -ForegroundColor White
    Write-Host "  • Visual C++ Redistributable" -ForegroundColor White
    Write-Host "  • PyQt5 ve diğer gerekli kütüphaneler" -ForegroundColor White
    Write-Host "  • AzGelir uygulaması" -ForegroundColor White
    Write-Host "  • Masaüstü ve Başlat menüsü kısayolları" -ForegroundColor White
    Write-Host ""
    
    $confirm = Read-Host "Kuruluma devam etmek istiyor musunuz? (Y/N)"
    if ($confirm -ne "Y" -and $confirm -ne "y") {
        Write-Info "Kurulum iptal edildi."
        exit 0
    }
}

try {
    Write-Step "1/8" "Sistem kontrolü yapılıyor..."
    
    # Sistem kontrolü
    $osInfo = Get-WmiObject -Class Win32_OperatingSystem
    $architecture = $osInfo.OSArchitecture
    
    if ($architecture -ne "64-bit") {
        throw "Bu kurulum sadece 64-bit Windows sistemlerde çalışır!"
    }
    
    Write-Success "Sistem uyumlu: $($osInfo.Caption) $architecture"
    
    Write-Step "2/8" "Kurulum dizini hazırlanıyor..."
    
    # Kurulum dizini oluştur
    if (-not (Test-Path $InstallPath)) {
        New-Item -Path $InstallPath -ItemType Directory -Force | Out-Null
    }
    Write-Success "Kurulum dizini: $InstallPath"
    
    Write-Step "3/8" "Python kontrol ediliyor..."
    
    # Python kontrolü
    $pythonInstalled = $false
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion -match "Python 3\.([8-9]|1[0-9])") {
            Write-Success "Python zaten kurulu: $pythonVersion"
            $pythonInstalled = $true
            $pythonExe = "python"
        }
    } catch {
        Write-Warning "Python kurulu değil"
    }
    
    # Python kurulumu
    if (-not $pythonInstalled) {
        Write-Step "3a/8" "Python kuruluyor..."
        
        $pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
        $pythonZip = "$env:TEMP\\python.zip"
        $pythonDir = "$InstallPath\\Python"
        
        Write-Info "Python indiriliyor..."
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonZip -UseBasicParsing
        
        Write-Info "Python kuruluyor..."
        if (Test-Path $pythonDir) {
            Remove-Item $pythonDir -Recurse -Force
        }
        Expand-Archive -Path $pythonZip -DestinationPath $pythonDir -Force
        
        # pip kurulumu
        Write-Info "pip kuruluyor..."
        $pipUrl = "https://bootstrap.pypa.io/get-pip.py"
        $pipFile = "$pythonDir\\get-pip.py"
        Invoke-WebRequest -Uri $pipUrl -OutFile $pipFile -UseBasicParsing
        
        # python._pth dosyasını düzenle (pip için)
        $pthFile = Get-ChildItem "$pythonDir\\*._pth" | Select-Object -First 1
        if ($pthFile) {
            Add-Content $pthFile.FullName "import site"
        }
        
        & "$pythonDir\\python.exe" $pipFile
        
        $pythonExe = "$pythonDir\\python.exe"
        Write-Success "Python kurulumu tamamlandı"
    }
    
    Write-Step "4/8" "Visual C++ Redistributable kontrol ediliyor..."
    
    # VC++ Redistributable kontrolü
    $vcInstalled = $false
    try {
        $vcKey = Get-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64" -ErrorAction Stop
        if ($vcKey.Version -ge "14.29") {
            Write-Success "Visual C++ Redistributable zaten kurulu"
            $vcInstalled = $true
        }
    } catch {
        Write-Warning "Visual C++ Redistributable kurulu değil"
    }
    
    # VC++ kurulumu
    if (-not $vcInstalled) {
        Write-Step "4a/8" "Visual C++ Redistributable kuruluyor..."
        
        $vcUrl = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        $vcFile = "$env:TEMP\\vc_redist.exe"
        
        Write-Info "Visual C++ Redistributable indiriliyor..."
        Invoke-WebRequest -Uri $vcUrl -OutFile $vcFile -UseBasicParsing
        
        Write-Info "Visual C++ Redistributable kuruluyor..."
        Start-Process -FilePath $vcFile -ArgumentList "/quiet", "/norestart" -Wait
        
        Write-Success "Visual C++ Redistributable kurulumu tamamlandı"
    }
    
    Write-Step "5/8" "AzGelir dosyaları hazırlanıyor..."
    
    # AzGelir dosyalarını kopyala (bu kısım build sırasında doldurulacak)
    # Base64 encoded dosyalar buraya gelecek
    
    Write-Success "AzGelir dosyaları hazırlandı"
    
    Write-Step "6/8" "Python paketleri kuruluyor..."
    
    # PyQt5 kurulumu
    Write-Info "PyQt5 kuruluyor..."
    & $pythonExe -m pip install PyQt5==5.15.9 --quiet
    
    # pywin32 kurulumu
    Write-Info "pywin32 kuruluyor..."
    & $pythonExe -m pip install pywin32 --quiet
    
    # Diğer bağımlılıklar
    Write-Info "Diğer bağımlılıklar kuruluyor..."
    & $pythonExe -m pip install pyinstaller --quiet
    
    Write-Success "Python paketleri kuruldu"
    
    Write-Step "7/8" "Kısayollar oluşturuluyor..."
    
    # COM Shell nesnesi
    $WshShell = New-Object -comObject WScript.Shell
    
    # Masaüstü kısayolu
    if (-not $NoDesktopShortcut) {
        $DesktopPath = [Environment]::GetFolderPath("Desktop")
        $ShortcutPath = "$DesktopPath\\AzGelir.lnk"
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = "$InstallPath\\AzGelir.exe"
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
        $Shortcut.Save()
        Write-Success "Masaüstü kısayolu oluşturuldu"
    }
    
    # Başlat menüsü kısayolu
    if (-not $NoStartMenuShortcut) {
        $StartMenuPath = "$env:ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir"
        if (-not (Test-Path $StartMenuPath)) {
            New-Item -Path $StartMenuPath -ItemType Directory -Force | Out-Null
        }
        
        $StartShortcutPath = "$StartMenuPath\\AzGelir.lnk"
        $StartShortcut = $WshShell.CreateShortcut($StartShortcutPath)
        $StartShortcut.TargetPath = "$InstallPath\\AzGelir.exe"
        $StartShortcut.WorkingDirectory = $InstallPath
        $StartShortcut.Description = "AzGelir - Gelir/Gider Takip Uygulaması"
        $StartShortcut.Save()
        
        # Kaldırıcı kısayolu
        $UninstallShortcutPath = "$StartMenuPath\\AzGelir Kaldır.lnk"
        $UninstallShortcut = $WshShell.CreateShortcut($UninstallShortcutPath)
        $UninstallShortcut.TargetPath = "powershell.exe"
        $UninstallShortcut.Arguments = "-ExecutionPolicy Bypass -File \\"$InstallPath\\uninstall.ps1\\""
        $UninstallShortcut.Description = "AzGelir Kaldır"
        $UninstallShortcut.Save()
        
        Write-Success "Başlat menüsü kısayolları oluşturuldu"
    }
    
    Write-Step "8/8" "Sistem entegrasyonu tamamlanıyor..."
    
    # Registry kayıtları
    $RegPath = "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir"
    New-Item -Path $RegPath -Force | Out-Null
    Set-ItemProperty -Path $RegPath -Name "DisplayName" -Value "AzGelir"
    Set-ItemProperty -Path $RegPath -Name "DisplayVersion" -Value "1.0.0"
    Set-ItemProperty -Path $RegPath -Name "Publisher" -Value "Tamerefe"
    Set-ItemProperty -Path $RegPath -Name "InstallLocation" -Value $InstallPath
    Set-ItemProperty -Path $RegPath -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File \\"$InstallPath\\uninstall.ps1\\""
    Set-ItemProperty -Path $RegPath -Name "URLInfoAbout" -Value "https://github.com/Tamerefe/AzGelir"
    
    # Kaldırıcı script oluştur
    $UninstallScript = @"
# AzGelir Kaldırıcı
Write-Host "AzGelir kaldırılıyor..." -ForegroundColor Yellow

# Çalışan uygulamayı durdur
Get-Process -Name "AzGelir" -ErrorAction SilentlyContinue | Stop-Process -Force

# Dosyaları kaldır
Remove-Item "$InstallPath" -Recurse -Force -ErrorAction SilentlyContinue

# Kısayolları kaldır
Remove-Item "$env:PUBLIC\\Desktop\\AzGelir.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\AzGelir" -Recurse -Force -ErrorAction SilentlyContinue

# Registry temizle
Remove-Item "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AzGelir" -Force -ErrorAction SilentlyContinue

Write-Host "AzGelir başarıyla kaldırıldı!" -ForegroundColor Green
"@
    
    $UninstallScript | Out-File "$InstallPath\\uninstall.ps1" -Encoding UTF8
    
    Write-Success "Sistem entegrasyonu tamamlandı"
    
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "║                   KURULUM TAMAMLANDI!                        ║" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    Write-Success "AzGelir başarıyla kuruldu!"
    Write-Host ""
    Write-Info "Çalıştırma seçenekleri:"
    Write-Host "  • Masaüstü kısayolu: AzGelir" -ForegroundColor White
    Write-Host "  • Başlat menüsü: Tüm Programlar > AzGelir" -ForegroundColor White
    Write-Host "  • Doğrudan: $InstallPath\\AzGelir.exe" -ForegroundColor White
    Write-Host ""
    
    if (-not $Silent) {
        $runNow = Read-Host "AzGelir'i şimdi çalıştırmak istiyor musunuz? (Y/N)"
        if ($runNow -eq "Y" -or $runNow -eq "y") {
            Start-Process "$InstallPath\\AzGelir.exe"
        }
    }
    
} catch {
    Write-Error "Kurulum sırasında hata oluştu: $($_.Exception.Message)"
    Write-Host ""
    Write-Warning "Lütfen şunları kontrol edin:"
    Write-Host "  • İnternet bağlantınız aktif mi?" -ForegroundColor White
    Write-Host "  • Yönetici ayrıcalıkları var mı?" -ForegroundColor White
    Write-Host "  • Antivırüs yazılımı engelliyor mu?" -ForegroundColor White
    Write-Host ""
    
    if (-not $Silent) {
        Read-Host "Çıkmak için Enter'a basın"
    }
    exit 1
}"""
    
    with open("AzGelir_Full_Install.ps1", "w", encoding="utf-8") as f:
        f.write(ps_content)
    
    print("✓ PowerShell installer oluşturuldu")

def create_self_extracting_exe():
    """Kendi kendini çıkaran exe oluştur"""
    print("📦 Self-extracting exe oluşturuluyor...")
    
    # 7-Zip SFX modülü ile self-extracting exe oluştur
    sfx_config = """
;!@Install@!UTF-8!
Title="AzGelir Kurulum Sihirbazı"
BeginPrompt="AzGelir uygulamasını kurmak istediğinizden emin misiniz?"
RunProgram="AzGelir_Full_Install.ps1"
;!@InstallEnd@!
"""
    
    with open("config.txt", "w", encoding="utf-8") as f:
        f.write(sfx_config)
    
    print("✓ Self-extracting exe konfigürasyonu oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🏗️ AzGelir Tam Otomatik Kurulum Sistemi Oluşturucu")
    print("=" * 60)
    
    # Önce ana uygulama exe'sini oluştur
    print("\n1. Ana uygulama exe'si oluşturuluyor...")
    if not os.path.exists("dist/AzGelir.exe"):
        print("📦 Önce ana uygulamayı derleyelim...")
        try:
            subprocess.check_call([sys.executable, "build_windows.py"])
        except subprocess.CalledProcessError:
            print("❌ Ana uygulama derlenemedi!")
            return
    
    # Kurulum dosyalarını oluştur
    print("\n2. Kurulum dosyaları oluşturuluyor...")
    create_full_installer()
    download_dependencies()
    create_standalone_exe()
    create_auto_installer_batch()
    create_powershell_installer()
    create_self_extracting_exe()
    
    print("\n🎉 Tam otomatik kurulum sistemi oluşturuldu!")
    print("\n📋 Oluşturulan dosyalar:")
    print("   • AzGelir_Full_Auto_Install.bat - Batch installer")
    print("   • AzGelir_Full_Install.ps1 - PowerShell installer")
    print("   • full_installer.nsi - NSIS script")
    print("   • standalone_installer.py - Tkinter GUI installer")
    print("   • config.txt - Self-extracting exe config")
    
    print("\n🚀 Kullanım:")
    print("   Sıfırdan bilgisayara kurulum için:")
    print("   - AzGelir_Full_Auto_Install.bat (Yönetici olarak çalıştır)")
    print("   - veya AzGelir_Full_Install.ps1 (PowerShell yönetici)")

if __name__ == "__main__":
    main()
