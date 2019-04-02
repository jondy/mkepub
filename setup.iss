[Setup]
AppId=yanhong-editor
AppVersion=0.1a2
AppName=—”∞≤∫Ï‘∆±‡º≠÷˙ ÷
AppVerName=—”∞≤∫Ï‘∆±‡º≠÷˙ ÷ 0.2a1
DefaultDirName={pf}\yanhong
DefaultGroupName=—”∞≤∫Ï‘∆∆ΩÃ®
AllowNoIcons=yes
SourceDir=D:\projects\mkepub\dist\mkepub
OutputDir=D:\projects\mkepub\dist
OutputBaseFilename=yanhong-editor

[Dirs]
Name: "{app}\output"; Permissions: authusers-modify;
Name: "{app}\logs"; Permissions: authusers-modify;

[Files]
Source: "D:\projects\mkepub\dist\mkepub\*"; DestDir: "{app}"; Flags: recursesubdirs;
Source: "D:\projects\mkepub\dist\images\logo-64.ico"; DestDir: "{app}"; DestName: "logo.ico";
Source: "D:\projects\mkepub\rulers.txt"; DestDir: "{app}"; Flags: recursesubdirs; Permissions: authusers-modify;

[Icons]
Name: "{group}\—”∞≤∫Ï‘∆±‡º≠÷˙ ÷"; Filename: "{app}\mkepub.exe"; IconFilename: "{app}\logo.ico";
Name: "{group}\–∂‘ÿ—”∞≤∫Ï‘∆±‡º≠÷˙ ÷"; Filename: "{uninstallexe}";
Name: "{group}\ π”√∞Ô÷˙"; Filename: "{app}\README.html"; WorkingDir: "{app}";
Name: "{userdesktop}\—”∞≤∫Ï‘∆±‡º≠÷˙ ÷"; Filename: "{app}\mkepub.exe"; WorkingDir: "{app}"; IconFilename: "{app}\logo.ico";

[Run]
Filename: "{app}\mkepub.exe"; Description: "‘À––—”∞≤∫Ï‘∆±‡º≠÷˙ ÷"; Flags: postinstall nowait

[UninstallDelete]
Type: dirifempty ; Name: "{app}"

