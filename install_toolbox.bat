SET "FILENAME=%~dp0DockerToolbox.exe"
SET "URL=https://download.docker.com/win/stable/DockerToolbox.exe"
powershell "Import-Module BitsTransfer; Start-BitsTransfer '%URL%' '%FILENAME%'"
%~dp0DockerToolbox.exe /SILENT
cd %~dp0
"C:\Program Files\Git\bin\bash.exe" --login -i "C:\Program Files\Docker Toolbox\start.sh" docker build . -t avalon/docker
"C:\Program Files\Git\bin\bash.exe" --login -i "C:\Program Files\Docker Toolbox\start.sh" docker run -d --name avalon -v avalon-db:/data/db --rm -p 27017:27017 -p 445:445 -p 139:139 avalon/docker
