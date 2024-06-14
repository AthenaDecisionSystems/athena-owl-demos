#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=athena/ibu-insurance-data-mgr

if [[ $# -eq 1 ]]
then
  TAG=$1
else
  TAG=latest
fi

cd $scriptDir/../code/apis-datamgt-insurance-pc-claims
sh ./mvnw clean package -DskipTests
docker build -f src/main/docker/Dockerfile.jvm -t  ${IMAGE_NAME}:${TAG} .
docker tag  ${IMAGE_NAME}:${TAG}   ${IMAGE_NAME}:latest
