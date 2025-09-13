
; AzGelir Windows Installer Script (NSIS)
; Modern UI kullanır

!include "MUI2.nsh"

; Program bilgileri
!define PRODUCT_NAME "AzGelir"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Tamerefe"
!define PRODUCT_WEB_SITE "https://github.com/Tamerefe/AzGelir"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\AzGelir.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

; Installer ayarları
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "AzGelir_Setup.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

; Modern UI ayarları
!define MUI_ABORTWARNING
!define MUI_ICON "logo.ico"
!define MUI_UNICON "logo.ico"

; Sayfalar
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Diller
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "English"

; Ana bölüm
Section "AzGelir (Gerekli)" SEC01
  SectionIn RO
  SetOutPath "$INSTDIR"
  File "dist\AzGelir.exe"
  File "logo.png"
  
  ; Registry kayıtları
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\AzGelir.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\AzGelir.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  
  ; Uninstaller oluştur
  WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

; Masaüstü kısayolu
Section "Masaüstü Kısayolu" SEC02
  CreateShortCut "$DESKTOP\AzGelir.lnk" "$INSTDIR\AzGelir.exe"
SectionEnd

; Başlat Menüsü
Section "Başlat Menüsü Kısayolu" SEC03
  CreateDirectory "$SMPROGRAMS\AzGelir"
  CreateShortCut "$SMPROGRAMS\AzGelir\AzGelir.lnk" "$INSTDIR\AzGelir.exe"
  CreateShortCut "$SMPROGRAMS\AzGelir\Kaldır.lnk" "$INSTDIR\uninst.exe"
SectionEnd

; Dosya uzantısı ilişkilendirme
Section "Dosya İlişkilendirme (.azg)" SEC04
  WriteRegStr HKCR ".azg" "" "AzGelir.Document"
  WriteRegStr HKCR "AzGelir.Document" "" "AzGelir Belgesi"
  WriteRegStr HKCR "AzGelir.Document\DefaultIcon" "" "$INSTDIR\AzGelir.exe,0"
  WriteRegStr HKCR "AzGelir.Document\shell\open\command" "" '"$INSTDIR\AzGelir.exe" "%1"'
SectionEnd

; Bölüm açıklamaları
LangString DESC_SEC01 ${LANG_TURKISH} "Ana uygulama dosyaları (gerekli)"
LangString DESC_SEC02 ${LANG_TURKISH} "Masaüstünde kısayol oluşturur"
LangString DESC_SEC03 ${LANG_TURKISH} "Başlat menüsünde kısayol oluşturur"
LangString DESC_SEC04 ${LANG_TURKISH} ".azg dosyalarını AzGelir ile ilişkilendirir"

LangString DESC_SEC01 ${LANG_ENGLISH} "Main application files (required)"
LangString DESC_SEC02 ${LANG_ENGLISH} "Create desktop shortcut"
LangString DESC_SEC03 ${LANG_ENGLISH} "Create start menu shortcuts"
LangString DESC_SEC04 ${LANG_ENGLISH} "Associate .azg files with AzGelir"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} $(DESC_SEC01)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} $(DESC_SEC02)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} $(DESC_SEC03)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} $(DESC_SEC04)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Kaldırıcı
Section Uninstall
  Delete "$INSTDIR\AzGelir.exe"
  Delete "$INSTDIR\logo.png"
  Delete "$INSTDIR\uninst.exe"
  Delete "$DESKTOP\AzGelir.lnk"
  Delete "$SMPROGRAMS\AzGelir\AzGelir.lnk"
  Delete "$SMPROGRAMS\AzGelir\Kaldır.lnk"
  RMDir "$SMPROGRAMS\AzGelir"
  RMDir "$INSTDIR"

  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey HKCR ".azg"
  DeleteRegKey HKCR "AzGelir.Document"
SectionEnd
