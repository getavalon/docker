@echo off

set AVALON_MONGO=mongodb://192.168.99.100:27017
set PATH=%~dp0;%~dp0bin\windows\python36;%PATH%

:: Expose Python libraries
set PYTHONPATH=%~dp0git\avalon-core
set PYTHONPATH=%~dp0git\avalon-launcher;%PYTHONPATH%
set PYTHONPATH=%~dp0git\mindbender-config;%PYTHONPATH%
set PYTHONPATH=%~dp0git\pyblish-base;%PYTHONPATH%
set PYTHONPATH=%~dp0git\pyblish-qml;%PYTHONPATH%
set PYTHONPATH=%~dp0git\cgwire-gazu;%PYTHONPATH%

:: Expose cross-platform libraries
set PYTHONPATH=%~dp0bin\pythonpath;%PYTHONPATH%

cls

echo.
echo  Avalon Terminal
echo  ---------------
echo.
echo  :: Launch avalon
echo  $ avalon
echo.
echo  :: Get help
echo  $ avalon --help
echo.
echo.

call cmd /K
