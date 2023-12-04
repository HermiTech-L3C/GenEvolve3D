; GenEvolve3D Installer Script
!include "MUI2.nsh"

; Installer configuration
Name "GenEvolve3D"
OutFile "GenEvolve3D-Setup.exe"
InstallDir "$PROGRAMFILES\GenEvolve3D"
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
    File "GenEvolve3D.exe" ; Ensure this executable is in the same directory as the NSIS script
    CreateDirectory "$SMPROGRAMS\GenEvolve3D"
    CreateShortCut "$SMPROGRAMS\GenEvolve3D\GenEvolve3D.lnk" "$INSTDIR\GenEvolve3D.exe"
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\GenEvolve3D.exe"
    Delete "$SMPROGRAMS\GenEvolve3D\GenEvolve3D.lnk"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$SMPROGRAMS\GenEvolve3D"
    RMDir "$INSTDIR"
SectionEnd
