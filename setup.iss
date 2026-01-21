[Setup]
AppName=ExperimentApp
AppVersion=1.7
DefaultDirName={localappdata}\Programs\4Sc1\ExperimentApp
DefaultGroupName=ExperimentApp
OutputDir=userdocs:ExperimentApp Installer
OutputBaseFilename=ExperimentApp
PrivilegesRequired=lowest

[Files]
Source: ".\dist\*"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\settings.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ExperimentApp"; Filename: "{app}\ExperimentApp.exe"
Name: "{group}\Settings File"; Filename: "{app}\settings.json"

[Registry]
Root: HKCU; Subkey: "Software\4Sc1\ExperimentApp"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: createvalueifdoesntexist
