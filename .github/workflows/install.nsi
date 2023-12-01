; GENrevolve3D Installer Script
!include "MUI2.nsh"

; Installer configuration
Name "GENrevolve3D"
OutFile "GENrevolve3D-Setup.exe"  ; This is the name of the installer
InstallDir "$PROGRAMFILES\GENrevolve3D"
ShowInstDetails show
ShowUnInstDetails show

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File ".\dist\Main.exe"  ; Make sure this path matches the location of the built executable
    CreateDirectory "$SMPROGRAMS\GENrevolve3D"
    CreateShortCut "$SMPROGRAMS\GENrevolve3D\GENrevolve3D.lnk" "$INSTDIR\Main.exe"
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\Main.exe"
    Delete "$SMPROGRAMS\GENrevolve3D\GENrevolve3D.lnk"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$SMPROGRAMS\GENrevolve3D"
    RMDir "$INSTDIR"
SectionEnd
