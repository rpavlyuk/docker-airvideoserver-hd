#!/bin/bash

VERSION="2.2.3"
AIRVIDEO_DIST="AirVideoServerHD-$VERSION.tar.bz2"

# Get airvideoserver-hd source
if [ ! -f "./airvideoserver-hd/src/$AIRVIDEO_DIST" ];
then
  wget https://s3.amazonaws.com/AirVideoHD/Download/$AIRVIDEO_DIST -O ./airvideoserver-hd/src/$AIRVIDEO_DIST
fi

# Run svarog to build the RPMs
svarog

# collect packages
rm -rf .rpms && mkdir -p .rpms
find ./repo -type f -name "*.rpm" -exec cp {} ./.rpms \;

# Build docker container
sudo docker build --rm -t local/c7-airvideoserver-hd .