#!/bin/bash

# Java
echo "Building Java"
javac java/src/main/java/com/example/InsecureApp.java

# C
echo "Building C"
make clean
make -C c

# C#
echo "Building C#"
dotnet build csharp/InsecureService.csproj