#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows MSI installer oluşturma scripti
WiX Toolset kullanır
"""

import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from uuid import uuid4

def check_wix():
    """WiX Toolset kurulu mu kontrol et"""
    try:
        result = subprocess.run(["candle", "-?"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ WiX Toolset bulundu")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ WiX Toolset bulunamadı")
    print("WiX Toolset indirmek için: https://wixtoolset.org/releases/")
    return False

def create_wix_config():
    """WiX installer config dosyası oluştur"""
    
    # Benzersiz GUID'ler oluştur
    product_guid = str(uuid4()).upper()
    upgrade_guid = str(uuid4()).upper()
    component_guid = str(uuid4()).upper()
    
    wix_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="{product_guid}" 
           Name="AzGelir" 
           Language="1055" 
           Version="1.0.0.0" 
           Manufacturer="Tamerefe" 
           UpgradeCode="{upgrade_guid}">
    
    <Package InstallerVersion="200" 
             Compressed="yes" 
             InstallScope="perMachine"
             Description="AzGelir - Gelir/Gider Takip Uygulaması"
             Comments="MIT License ile dağıtılır"
             Manufacturer="Tamerefe" />

    <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />
    <MediaTemplate EmbedCab="yes" />

    <!-- Özellikler -->
    <Feature Id="ProductFeature" Title="AzGelir" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
      <ComponentRef Id="ApplicationShortcut" />
      <ComponentRef Id="DesktopShortcut" />
    </Feature>

    <!-- Dizin yapısı -->
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="AzGelir" />
      </Directory>
      <Directory Id="ProgramMenuFolder">
        <Directory Id="ApplicationProgramsFolder" Name="AzGelir"/>
      </Directory>
      <Directory Id="DesktopFolder" Name="Desktop"/>
    </Directory>

    <!-- Bileşenler -->
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <Component Id="MainExecutable" Guid="{component_guid}">
        <File Id="AzGelirEXE" 
              Source="dist\\AzGelir.exe" 
              KeyPath="yes" 
              Checksum="yes">
          <Shortcut Id="StartMenuShortcut"
                    Directory="ApplicationProgramsFolder"
                    Name="AzGelir"
                    Description="Gelir ve Gider Takip Uygulaması"
                    WorkingDirectory="INSTALLFOLDER"
                    Icon="AzGelir.exe"
                    IconIndex="0"
                    Advertise="yes" />
        </File>
        
        <!-- Registry kayıtları -->
        <RegistryValue Root="HKLM" 
                       Key="Software\\AzGelir" 
                       Name="InstallDir" 
                       Type="string" 
                       Value="[INSTALLFOLDER]" 
                       KeyPath="no" />
        
        <!-- Dosya ilişkilendirme -->
        <RegistryValue Root="HKLM" 
                       Key="Software\\Classes\\.azg" 
                       Value="AzGelir.Document" 
                       Type="string" 
                       KeyPath="no" />
        
        <RegistryValue Root="HKLM" 
                       Key="Software\\Classes\\AzGelir.Document" 
                       Value="AzGelir Belgesi" 
                       Type="string" 
                       KeyPath="no" />
        
        <RegistryValue Root="HKLM" 
                       Key="Software\\Classes\\AzGelir.Document\\shell\\open\\command" 
                       Value='"[INSTALLFOLDER]AzGelir.exe" "%1"' 
                       Type="string" 
                       KeyPath="no" />
      </Component>
      
      <!-- Logo dosyası -->
      <Component Id="LogoFile" Guid="{str(uuid4()).upper()}">
        <File Id="LogoPNG" Source="logo.png" KeyPath="yes" />
      </Component>
    </ComponentGroup>

    <!-- Masaüstü kısayolu -->
    <Component Id="DesktopShortcut" Directory="DesktopFolder" Guid="{str(uuid4()).upper()}">
      <Shortcut Id="DesktopShortcut"
                Name="AzGelir"
                Description="Gelir ve Gider Takip Uygulaması"
                Target="[INSTALLFOLDER]AzGelir.exe"
                WorkingDirectory="INSTALLFOLDER" />
      <RemoveFolder Id="DesktopFolder" On="uninstall"/>
      <RegistryValue Root="HKCU" Key="Software\\AzGelir\\Desktop" Name="installed" Type="integer" Value="1" KeyPath="yes"/>
    </Component>

    <!-- Başlat menüsü kısayolu -->
    <Component Id="ApplicationShortcut" Directory="ApplicationProgramsFolder" Guid="{str(uuid4()).upper()}">
      <RemoveFolder Id="ApplicationProgramsFolder" On="uninstall"/>
      <RegistryValue Root="HKCU" Key="Software\\AzGelir\\StartMenu" Name="installed" Type="integer" Value="1" KeyPath="yes"/>
    </Component>

    <!-- İkonlar -->
    <Icon Id="AzGelir.exe" SourceFile="dist\\AzGelir.exe" />

    <!-- Program Ekle/Kaldır bilgileri -->
    <Property Id="ARPPRODUCTICON" Value="AzGelir.exe" />
    <Property Id="ARPHELPLINK" Value="https://github.com/Tamerefe/AzGelir" />
    <Property Id="ARPURLINFOABOUT" Value="https://github.com/Tamerefe/AzGelir" />
    <Property Id="ARPNOREPAIR" Value="1" />
    <Property Id="ARPNOMODIFY" Value="1" />

    <!-- Lisans -->
    <WixVariable Id="WixUILicenseRtf" Value="License.rtf" />

    <!-- UI -->
    <UIRef Id="WixUI_InstallDir" />
    <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />

  </Product>
</Wix>"""
    
    with open("AzGelir.wxs", "w", encoding="utf-8") as f:
        f.write(wix_content)
    
    print("✓ WiX konfigürasyon dosyası oluşturuldu")

def create_license_rtf():
    """RTF formatında lisans dosyası oluştur"""
    rtf_content = r"""{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}
\\f0\\fs24
\\par MIT License
\\par
\\par Copyright (c) 2025 Tamerefe
\\par
\\par Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
\\par
\\par The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
\\par
\\par THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
}"""
    
    with open("License.rtf", "w", encoding="utf-8") as f:
        f.write(rtf_content)
    
    print("✓ RTF lisans dosyası oluşturuldu")

def build_msi():
    """MSI installer oluştur"""
    print("🔨 MSI installer oluşturuluyor...")
    
    try:
        # WiX object dosyası oluştur
        subprocess.check_call([
            "candle", 
            "-arch", "x64",
            "-ext", "WixUIExtension",
            "AzGelir.wxs"
        ])
        print("✓ WiX object dosyası oluşturuldu")
        
        # MSI dosyası oluştur
        subprocess.check_call([
            "light",
            "-ext", "WixUIExtension",
            "-out", "AzGelir_Setup.msi",
            "AzGelir.wixobj"
        ])
        print("✅ MSI installer oluşturuldu!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ MSI oluşturma hatası: {e}")
        return False

def create_msi_readme():
    """MSI README dosyası oluştur"""
    readme_content = """# AzGelir - MSI Installer

## Kurulum

### MSI Dosyası ile:
```
AzGelir_Setup.msi dosyasını çalıştırın
```

### Komut Satırından (Sessiz Kurulum):
```cmd
msiexec /i AzGelir_Setup.msi /quiet
```

### Komut Satırından (Özelleştirme):
```cmd
msiexec /i AzGelir_Setup.msi INSTALLFOLDER="C:\\MyApps\\AzGelir"
```

## Kaldırma

### Programlar ve Özellikler'den:
1. Denetim Masası > Programlar ve Özellikler
2. "AzGelir" uygulamasını seçin
3. "Kaldır" butonuna tıklayın

### Komut Satırından:
```cmd
msiexec /x AzGelir_Setup.msi /quiet
```

## Özellikler

- ✅ Windows Installer teknolojisi
- ✅ Otomatik kaldırma
- ✅ Sistem entegrasyonu
- ✅ Registry yönetimi
- ✅ Dosya ilişkilendirme (.azg)
- ✅ Masaüstü ve Başlat menüsü kısayolları
- ✅ Güvenli kurulum/kaldırma

## Sistem Gereksinimleri

- Windows 7 SP1 veya üzeri
- Windows Installer 3.1 veya üzeri
- .NET Framework 4.6.1 veya üzeri
- 100 MB disk alanı

## Enterprise Dağıtım

### Group Policy ile:
1. MSI dosyasını paylaşılan ağ konumuna koyun
2. Group Policy Management Console açın
3. Computer Configuration > Software Installation
4. New > Package ekleyin

### SCCM ile:
1. MSI dosyasını SCCM'e import edin
2. Application olarak paketleyin
3. Deployment type oluşturun

### PowerShell DSC ile:
```powershell
Package AzGelir {
    Ensure = "Present"
    Path = "\\\\server\\share\\AzGelir_Setup.msi"
    Name = "AzGelir"
    ProductId = "{PRODUCT-GUID}"
}
```

## Sorun Giderme

### MSI Log Dosyası:
```cmd
msiexec /i AzGelir_Setup.msi /l*v install.log
```

### Repair Installation:
```cmd
msiexec /fa AzGelir_Setup.msi
```

### Force Uninstall:
```cmd
msiexec /x AzGelir_Setup.msi /f
```
"""
    
    with open("README_MSI.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ MSI README dosyası oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("📦 MSI Installer için AzGelir Paketleme")
    print("=" * 45)
    
    # WiX Toolset kontrolü
    if not check_wix():
        print("❌ WiX Toolset gerekli!")
        sys.exit(1)
    
    # Gerekli dosyaları kontrol et
    if not os.path.exists("dist/AzGelir.exe"):
        print("❌ dist/AzGelir.exe bulunamadı!")
        print("Önce build_windows.py çalıştırın")
        sys.exit(1)
    
    # Konfigürasyon dosyalarını oluştur
    create_wix_config()
    create_license_rtf()
    
    # MSI oluştur
    if build_msi():
        create_msi_readme()
        
        # Dosya boyutunu göster
        if os.path.exists("AzGelir_Setup.msi"):
            size = os.path.getsize("AzGelir_Setup.msi") / (1024 * 1024)
            print(f"\n📦 MSI dosyası: {os.path.abspath('AzGelir_Setup.msi')}")
            print(f"📏 Dosya boyutu: {size:.1f} MB")
        
        print("\n🎉 MSI installer oluşturuldu!")
        print("📋 Enterprise dağıtım için hazır!")
    else:
        print("❌ MSI oluşturma başarısız!")
        sys.exit(1)

if __name__ == "__main__":
    main()
