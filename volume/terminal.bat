@echo off

set AVALON_MONGO=mongodb://192.168.99.100:27017
set PATH=%~dp0;%~dp0bin\windows\python36;%PATH%

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
