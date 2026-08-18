#!/bin/bash

# Java
echo "Building Java"
mvn -f java/pom.xml compile

# C
echo "Building C"
make clean
make -C c

# C#
echo "Building C#"
dotnet build csharp/InsecureService.csproj