#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=athena/ibu-backend

if [[ $# -eq 1 ]]
then
  TAG=$1
else
  TAG=latest
fi

cd $scriptDir/..
docker build -f Dockerfile -t  ${IMAGE_NAME}:${TAG} src

docker tag  ${IMAGE_NAME}:${TAG}   ${IMAGE_NAME}:latest
