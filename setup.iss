[Setup]
AppId=yanhong-editor
AppVersion=0.1a2
AppName=�Ӱ����Ʊ༭����
AppVerName=�Ӱ����Ʊ༭���� 0.2a1
DefaultDirName={pf}\yanhong
DefaultGroupName=�Ӱ�����ƽ̨
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
Name: "{group}\�Ӱ����Ʊ༭����"; Filename: "{app}\mkepub.exe"; IconFilename: "{app}\logo.ico";
Name: "{group}\����ת��·��"; Filename: "{app}\tools\batch";
Name: "{group}\ж���Ӱ����Ʊ༭����"; Filename: "{uninstallexe}";
Name: "{group}\ʹ�ð���"; Filename: "{app}\README.html"; WorkingDir: "{app}";
Name: "{userdesktop}\�Ӱ����Ʊ༭����"; Filename: "{app}\mkepub.exe"; WorkingDir: "{app}"; IconFilename: "{app}\logo.ico";

[Run]
Filename: "{app}\mkepub.exe"; Description: "�����Ӱ����Ʊ༭����"; Flags: postinstall nowait

[UninstallDelete]
Type: dirifempty ; Name: "{app}"

