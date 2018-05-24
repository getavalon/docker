@echo off

set __app__="NukeX"
set __exe__="C:\Program Files\The Foundry\NUKE\Nuke10.0v2\Nuke10.0"
if not exist %__exe__% goto :missing_app

start %__app__% %__exe__% --nukex %*

goto :eof

:missing_app
    echo ERROR: %__app__% not found in %__exe__%
    exit /B 1
