[Setup]
AppId=yanhong-editor
AppVersion=0.1a2
AppName=延安红云编辑助手
AppVerName=延安红云编辑助手 0.2a1
DefaultDirName={pf}\yanhong
DefaultGroupName=延安红云平台
AllowNoIcons=yes
SourceDir=D:\projects\mkepub\dist\mkepub
OutputDir=D:\projects\mkepub\dist
OutputBaseFilename=yanhong-editor

[Dirs]
Name: "{app}\output"; Permissions: authusers-modify;
Name: "{app}\logs"; Permissions: authusers-modify;
Name: "{app}\tools";
Name: "{app}\tools\batch"; Permissions: authusers-modify;

[Files]
Source: "D:\projects\mkepub\dist\mkepub\*"; DestDir: "{app}"; Flags: recursesubdirs;
Source: "D:\projects\mkepub\dist\images\logo-64.ico"; DestDir: "{app}"; DestName: "logo.ico";
Source: "D:\projects\mkepub\rulers.txt"; DestDir: "{app}"; Flags: recursesubdirs; Permissions: authusers-modify;

[Icons]
Name: "{group}\延安红云编辑助手"; Filename: "{app}\mkepub.exe"; IconFilename: "{app}\logo.ico";
Name: "{group}\批量转换路径"; Filename: "{app}\tools\batch";
Name: "{group}\卸载延安红云编辑助手"; Filename: "{uninstallexe}";
Name: "{group}\使用帮助"; Filename: "{app}\README.html"; WorkingDir: "{app}";
Name: "{userdesktop}\延安红云编辑助手"; Filename: "{app}\mkepub.exe"; WorkingDir: "{app}"; IconFilename: "{app}\logo.ico";

[Run]
Filename: "{app}\mkepub.exe"; Description: "运行延安红云编辑助手"; Flags: postinstall nowait

[UninstallDelete]
Type: dirifempty ; Name: "{app}"

