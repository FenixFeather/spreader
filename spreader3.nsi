;NSIS Modern User Interface
;Basic Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Spreader"
  OutFile "spreader-0.9.7-win32-installer.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Spreader"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Spreader" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin
  
;======================================================
; Defines
!define srcdir "./spreader-0.9.7-win32"
!define productname "Spreader"
!define regkey "Software\${productname}"
!define exec "spreader.exe"
!define uninstexec "Uninstall Spreader.exe"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname}"

;--------------------------------
;Variables

  Var StartMenuFolder
  
  
;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "${srcdir}\license.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  
  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "${regkey}" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Spreader Core" SecDummy

  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  !include "files.nsi"
  File /a "${srcdir}\${exec}"
  
  ;Store installation folder
  WriteRegStr HKCU "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname}" "DisplayName" "${productname} (remove only)"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname}" "UninstallString" '"$INSTDIR\${uninstexec}"'
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\${uninstexec}"
  
  
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\${productname}.lnk" "$INSTDIR\${exec}"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\${uninstexec}"
!insertmacro MUI_STARTMENU_WRITE_END


SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDummy ${LANG_ENGLISH} "Install main Spreader files"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END
  

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...
  !include unfiles.nsi
  Delete "$INSTDIR\${exec}"
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    
  Delete "$SMPROGRAMS\$StartMenuFolder\${productname}.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"

  Delete "$INSTDIR\${uninstexec}"

  RMDir "$INSTDIR"
  
  DeleteRegKey HKCU "${uninstkey}"
  DeleteRegKey HKCU "${regkey}"

SectionEnd