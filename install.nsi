; GENrevolve3D Installer Script
!include "MUI2.nsh"
; Installer configuration
Name "GENrevolve3D"
OutFile "GENrevolve3D-Setup.exe"
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
    ; Adding the executable. Adjust the path as needed if your build process puts the output somewhere else.
    File ".\dist\GENrevolve3D.exe"
    ; If you have additional data files or dependencies bundled with your application, include them here
    ; For example, if you have a data folder, you would include it like this:
    ; SetOutPath "$INSTDIR\data"
    ; File /r ".\dist\data\*.*"
    ; Create a shortcut in the Start Menu
    CreateDirectory "$SMPROGRAMS\GENrevolve3D"
    CreateShortCut "$SMPROGRAMS\GENrevolve3D\GENrevolve3D.lnk" "$INSTDIR\GENrevolve3D.exe"
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd
Section "Uninstall"
    ; Remove the executable and data files
    Delete "$INSTDIR\GENrevolve3D.exe"
    ; Include additional file or directory deletions here if necessary
    ; For example, to remove the data directory added above:
    ; RMDir /r "$INSTDIR\data"
    ; Remove the Start Menu shortcut and uninstaller
    Delete "$SMPROGRAMS\GENrevolve3D\GENrevolve3D.lnk"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$SMPROGRAMS\GENrevolve3D"
    RMDir "$INSTDIR"
SectionEnd












