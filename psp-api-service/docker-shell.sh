#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
# Automatic export to the environment of subsequently executed commands
# source: the command 'help export' run in Terminal
# NOTE: Defining global VARs to use, mainly for paths to easily grab
export IMAGE_NAME="psp-api-service-v1"
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/

# GCP Connection
export GCP_PROJECT="ac215-nst"
export GCP_ZONE="us-central1-a"
export GOOGLE_APPLICATION_CREDENTIALS=/secrets/bucket-reader.json


# Build the image based on the Dockerfile
# FIX M1 MAC: Need amd64 arch because a lot of pip wheels not supported by default m1
# https://til.simonwillison.net/macos/running-docker-on-remote-m1
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container
# --mount: Attach a filesystem mount to the container
# -p: Publish a container's port(s) to the host (host_port: container_port) (source: https://dockerlabs.collabnix.com/intermediate/networking/ExposingContainerPort.html)
# NOTE: We mount all the local directories we want the actual container to have access to
# Create 2 containers -> DEV 1 or 0 is Dev or production
docker run --rm --name $IMAGE_NAME -ti \
--mount type=bind,source="$BASE_DIR",target=/app \
--mount type=bind,source="$PERSISTENT_DIR",target=/persistent \
--mount type=bind,source="$SECRETS_DIR",target=/secrets \
-p 9000:9000 \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e DEV=1 $IMAGE_NAME

