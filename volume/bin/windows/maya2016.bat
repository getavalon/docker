@echo off

set __app__="Maya 2016"
set __exe__="C:\Program Files\Autodesk\Maya2016\bin\maya.exe"
if not exist %__exe__% goto :missing_app

start %__app__% %__exe__% %*

goto :eof

:missing_app
    echo ERROR: %__app__% not found in %__exe__%
    exit /B 1
