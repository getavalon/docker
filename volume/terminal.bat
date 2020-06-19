@echo off

set PATH=%~dp0;%PATH%

call avalon --environment > tmp.bat
call tmp.bat
del tmp.bat

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
