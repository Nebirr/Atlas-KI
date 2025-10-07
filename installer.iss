; installer.iss — Atlas Installer (Inno Setup)
; Ziel: dist\Atlas\  ->  C:\Program Files\Atlas\
; Features: Startmenü + Desktop-Icon, optionaler Auto-Start, Launch-Checkbox

#define MyAppName        "Atlas"
#define MyAppExeName     "Atlas.exe"
#define MyAppPublisher   "Dein Name / Team"
#define MyAppURL         "https://example.com"
#define MyAppVersion     "1.0.0"

[Setup]
AppId={{6A0E0A18-8B2C-4B63-9D97-1B7DB6960B86}  ; GUID (beliebig, aber stabil lassen)
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableDirPage=no
DisableProgramGroupPage=no
AllowNoIcons=yes

; 64-bit Program Files verwenden, wenn OS 64-bit ist
ArchitecturesInstallIn64BitMode=x64

; Setup-Optik
SetupIconFile=assets\icons\atlas_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

; Signierung aus, falls nicht vorhanden
; SignTool= 

; Ausgabe
OutputBaseFilename=Atlas-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes

; Administratorrechte für Program Files
PrivilegesRequired=admin

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Optional: Desktop-Icon
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "Weitere Aufgaben:"; Flags: unchecked
; Optional: Autostart
Name: "autostart"; Description: "Atlas beim Anmelden automatisch starten"; GroupDescription: "Weitere Aufgaben:"; Flags: unchecked

[Files]
; *** GANZE onedir-Struktur aus dist\Atlas kopieren ***
; WICHTIG: Pfad anpassen, falls du das Script NICHT im Projekt-Root speicherst.
Source: "dist\Atlas\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Startmenü
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Optionales Desktop-Icon
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Autostart (pro Maschine) – setzt/entfernt Run-Schlüssel
; (Nutzt Tasks: autostart)
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
; Nach der Installation mit Checkbox starten
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Optional: Benutzer-Daten in AppData entfernen (NUR AUF WUNSCH!)
; WARNUNG: löscht alle Atlas-Nutzerdaten. Auskommentiert lassen, wenn du sicher sein willst.
; Type: filesandordirs; Name: "{userappdata}\Atlas"
; Type: filesandordirs; Name: "{localappdata}\Atlas"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  { Nichts nötig – Hook vorhanden, falls du später z.B. Prereqs prüfen willst }
end;