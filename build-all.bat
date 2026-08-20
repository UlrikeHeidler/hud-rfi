@echo off

echo BUILD SCRIPT STARTED > build.log
REM C#
dotnet build csharp\InsecureService.csproj

REM Java
javac java\src\main\java\com\example\InsecureApp.java

REM C
gcc c\insecure.c -o c\insecure.exe

echo BUILD SCRIPT FINISHED >> build.log