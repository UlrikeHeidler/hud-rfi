#!/bin/bash

# Java
mvn -f java/pom.xml compile

# C
make clean
make -C c

# C#
dotnet build csharp/InsecureService.csproj