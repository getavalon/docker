@echo off

set AVALON_MONGO=mongodb://192.168.99.100:27017
set AVALON_CORE=%~dp0git\avalon-core
set AVALON_LAUNCHER=%~dp0git\avalon-launcher
set PATH=%~dp0;%~dp0bin\windows\python36;%PATH%

:: Expose Python libraries
set PYTHONPATH=%AVALON_CORE%
set PYTHONPATH=%AVALON_LAUNCHER%;%PYTHONPATH%
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
