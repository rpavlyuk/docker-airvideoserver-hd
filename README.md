# docker-airvideoserver-hd
The other version of Air Video Server HD that is based on CentOS7 image

## Author and Credits
Roman Pavlyuk <roman.pavlyuk@gmail.com>
http://roman.pavlyuk.lviv.ua/

## Purpose
This image has been created to give the ability to run AirVideoServer HD for Linux (by InMethod.com http://www.inmethod.com/airvideohd/index.html) by the users who have VLC 3.x+ on their boxes. As you know, currently AirVideoServerHD 2.3.3 for Linux doesn't support VLC 3.x which is default one for Fedora Linux 24+ (see more here: http://forums.inmethod.com/topic/2291-air-video-server-hd-for-linux/ UPD: link broken :( ). That's why the best way to have AirVideoServerHD on Fedora 24+ is to run it in Docker container.

## How to use it?
There are several ways you can play with this project and make AirVideoServerHD running on your system.

### Method 1: Using pre-built container RPM (recommended for F24+ users)
**NOTE:** This will work on RedHat systems only
* Enable project repository on your box:
```
sudo wget http://repo.ukrspace.net/repo/airvideoserver-hd-master/fast/el7/airvideoserver-hd-master.repo -O /etc/yum.repos.d/airvideoserver-hd-master.repo
```
* Install the package:
```
sudo dnf install docker-airvideoserver-hd -y
```
if you are on CentOS 7.x then use ```yum```:
```
sudo yum install docker-airvideoserver-hd -y
```
* Open file ```/etc/docker-airvideoserver-hd/mounts.conf``` and specify which folders shall be exposed to the container. In other words, folders on your server where your media files are. Format is the following:``` -v [path_to_media_folder_on_the_server]:[path_to_media_folder_on_the_container]```. In fact, it is recommended to keep 'local' and 'container' paths the same, for example:
```
 -v /media:/media
```
Not a problem if you want to mount two folders or more. You can do it like this (example of ```/etc/docker-airvideoserver-hd/mounts.conf```):
```
 -v /media:/media -v /storage/movies:/storage/movies
```
* Edit file ```/etc/docker-airvideoserver-hd/Server.properties```, especially provide media folder paths. It is strongly recommended to leave parameters like ```logsPath```, ```applicationDataPath```, ```conversionFolderPath``` with their default values.
* Start ```systemctl start docker-airvideoserver-hd.service```:
```
sudo systemctl start docker-airvideoserver-hd.service
```
**NOTE:** It a while for the service to for the first time since it is pulling the container image from Docker Hub. You can monitor the progress by running:
```
systemctl status docker-airvideoserver-hd.service
```
* You can check of the container is running by issuing command ```docker ps```:
```
$ docker ps
CONTAINER ID        IMAGE                        COMMAND             CREATED             STATUS              PORTS                                                NAMES
d35a45270a8d        rpavlyuk/c7-airvideoserver-hd   "/usr/sbin/init"    3 minutes ago       Up 3 minutes        0.0.0.0:45601->45601/tcp, 0.0.0.0:45633->45633/tcp   airvideoserver-hd
```
That's it, now you have AirVideoServer HD up and running!

### Method 2: Using systemdock (one more recommended method for F24+ users)
```systemdock``` is the tool that run the container as ```systemd``` service and handles lots of pre- and post-configuration options of the container making its start/stop worry free for you once it is configured.

* First, install ```systemdock```. See instruction here: https://github.com/rpavlyuk/systemdock. It is strongly recommended that you install the ```systemdock``` using RPM package as there will be problem with dependencies below.
* We need to enable the pre-built RPM packages repository as well:
```
sudo wget http://repo.ukrspace.net/repo/airvideoserver-hd-master/fast/el7/airvideoserver-hd-master.repo -O /etc/yum.repos.d/airvideoserver-hd-master.repo
```
* Install ```systemdock``` profile:
```
sudo dnf install -y systemdock-airvideoserver-hd
```
* Open configuration file ```/etc/systemdock/containers.d/airvideoserver-hd/config.yaml``` and replace ```/media``` folder with your own configuration. You may add some more media locations if you have those, for examples:
```
...
        /media:
                bind: /media
                mode: ro
        /other-media/path:
                bind: /other-media/path
                mode: ro
...
```
Just make sure you preserve other mounts like ```/sys/fs/cgroup```, ```/var/lib/...``` etc. intact since they are needed for container to function properly.
* Edit ```/etc/airvideoserver-hd/Server.properties``` to by updating/adding path to your media that you've configured in the step above. Also, set access password to protect your server.
* Enable the service so the container will be started on system boot:
```
sudo systemctl enable systemdock-airvideoserver-hd.service
```
* Now, we are start the container as service:
```
sudo systemctl start systemdock-airvideoserver-hd.service
```
* As in the previous method, you can check the container is up-n-running by:
```
$ docker ps
CONTAINER ID        IMAGE                        COMMAND             CREATED             STATUS              PORTS                                                NAMES
d35a45270a8d        rpavlyuk/c7-airvideoserver-hd   "/usr/sbin/init"    3 minutes ago       Up 3 minutes        0.0.0.0:45601->45601/tcp, 0.0.0.0:45633->45633/tcp   airvideoserver-hd
```
* Some house-keeping -- let's make sure that non-systemdock service is disabled (should be, but just in case):
```
sudo systemctl disable airvideoserverhd.service
```

