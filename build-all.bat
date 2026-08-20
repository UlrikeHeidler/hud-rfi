@echo off

cd "C:\Users\UlrikeHeidler\OneDrive - Black Duck Software\Work\Prospects\HUD - Housing and Urban Development\20260715 - HUD OIG RFI\HUD Follow Up Input\RE_ HUD RFI"
echo BUILD SCRIPT STARTED > build.log
REM C#
dotnet build csharp\InsecureService.csproj

REM Java
javac java\src\main\java\com\example\InsecureApp.java

REM C
gcc c\insecure.c -o c\insecure.exe

echo BUILD SCRIPT FINISHED >> build.log