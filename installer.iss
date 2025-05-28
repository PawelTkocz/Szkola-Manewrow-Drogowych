[Setup]
AppName=Szkoła manewrów drogowych
AppVersion=1.0
DefaultDirName={autopf}\Szkola manewrow drogowych
DefaultGroupName=Szkoła manewrów drogowych
OutputDir=.
OutputBaseFilename=SzkolaManewrowDrogowych_1.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Szkoła manewrów drogowych"; Filename: "{app}\main.exe"
Name: "{group}\Odinstaluj Szkołę manewrów drogowych"; Filename: "{uninstallexe}"
