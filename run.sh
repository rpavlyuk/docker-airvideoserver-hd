#!/bin/bash

# kill existing one
docker stop airvideoserver-hd
docker rm airvideoserver-hd

# run a new container
docker run -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 45633:45633 --name airvideoserver-hd local/c7-airvideoserver-hd
