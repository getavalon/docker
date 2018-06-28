@echo off

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

set AVALON_MONGO=mongodb://192.168.99.100:27017
set PATH=%~dp0;%~dp0bin\windows\python36;%PATH%
set PYTHONPATH=%~dp0git\avalon-core;%~dp0git\avalon-launcher;%~dp0git\mindbender-config;%~dp0git\pyblish-base;%~dp0git\pyblish-qml;%PYTHONPATH%

call cmd /K
