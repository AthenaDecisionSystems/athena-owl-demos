#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=athenadecisionsystems/ibu-insurance-data-mgr


if [[ $# -eq 2 ]]
then
  TAG=$1
  OS=$2
else
  TAG=1.0.2
  OS=linux
fi

cd $scriptDir/..
mvn package -DskipTests
if  [[ $OS -eq "linux" ]]
then
  docker build -f src/main/docker/Dockerfile.jvm --platform linux/amd64 -t  ${IMAGE_NAME}:${TAG} .
else
  docker build -f src/main/docker/Dockerfile.jvm   -t  ${IMAGE_NAME}:${TAG} .
fi

docker tag  ${IMAGE_NAME}:${TAG}   ${IMAGE_NAME}:latest

