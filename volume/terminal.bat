@echo off

set AVALONCACHE=%HOMEDRIVE%%HOMEPATH%\.avalon
set PATH=%AVALONCACHE%\bin\python36;%PATH%

if not exist "%AVALONCACHE%" (
    echo Avalon was started for the first time, hold on..
    %~dp0bin\windows\python36\python.exe %~dp0avalon_cli.py --firsttime
    sleep 1
)

if not exist "%AVALONCACHE%" (
    echo This is a bug
    exit /b
)

set AVALON_MONGO=mongodb://192.168.99.100:27017

cls

if "%1" == "" (
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
)

call cmd /K %*
