#!/bin/bash

docker run -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 45633:45633 --name airvideoserver-hd local/c7-airvideoserver-hd
