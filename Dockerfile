FROM centos:7
MAINTAINER "Roman Pavlyuk" <roman.pavlyuk@gmail.com>

ENV container docker

RUN yum install -y epel-release
RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm

RUN yum update -y
RUN yum install -y vlc

RUN yum install -y less file 

### Let's enable systemd on the container
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
# VOLUME [ "/sys/fs/cgroup" ]

# VOLUME ["/var/lib/airvideoserver-hd/converted", "/var/lib/airvideoserver-hd/data", "/var/lib/airvideoserver-hd/logs"]

COPY .rpms /rpms

RUN ls -al /rpms

RUN yum localinstall -y /rpms/airvideoserver-hd-* /rpms/miniupnpc-*

RUN systemctl enable airvideoserverhd.service

### Kick it off
CMD ["/usr/sbin/init"]
