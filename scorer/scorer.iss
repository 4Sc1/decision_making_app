[Setup]
AppName=ExperimentScorer
AppVersion=1.6
DefaultDirName={localappdata}\Programs\4Sc1\ExperimentScorer
DefaultGroupName=ExperimentApp
OutputDir=userdocs:ExperimentScorer Installer
OutputBaseFilename=ExperimentScorer
PrivilegesRequired=lowest

[Files]
Source: ".\dist\*"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ExperimentScorer"; Filename: "{app}\Scorer.exe"

[Registry]
Root: HKCU; Subkey: "Software\4Sc1\ExperimentScorer"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: createvalueifdoesntexist
