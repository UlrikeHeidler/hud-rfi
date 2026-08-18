#!/bin/bash

# Java
echo "Building Java"
mvn clean -f java/src/main/java/com/example/pom.xml compile

# C
echo "Building C"
make clean
make -C c

# C#
echo "Building C#"
dotnet build csharp/InsecureService.csproj