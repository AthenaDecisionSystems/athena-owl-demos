#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=jbcodeforce/ibu-insurance-data-mgr

if [[ $# -eq 2 ]]
then
  TAG=$1
  OS=$2
else
  TAG=latest
  OS=linux
fi

cd $scriptDir/../code/apis-datamgt-insurance-pc-claims
sh ./mvnw clean package -DskipTests -Dnet.bytebuddy.experimental

if  [[ $OS -eq "linux" ]]
then
  docker build -f Dockerfile --platform linux/amd64 -t  ${IMAGE_NAME}:${TAG} .
else
  docker build -f Dockerfile  -t  ${IMAGE_NAME}:${TAG} .
fi


docker build -f src/main/docker/Dockerfile.jvm -t  ${IMAGE_NAME}:${TAG} .
docker tag  ${IMAGE_NAME}:${TAG}   ${IMAGE_NAME}:latest
