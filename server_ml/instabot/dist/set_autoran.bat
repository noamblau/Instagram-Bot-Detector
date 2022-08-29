call run.bat
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Startup\instabotserver.lnk');$s.TargetPath='%~f0\..\run.bat';$s.Save()"