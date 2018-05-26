@echo off

set AVALON_MONGO=mongodb://192.168.99.100:27017
%~dp0bin\windows\python36\python.exe %~dp0avalon.py %*
