#!/bin/sh

echo $(date)

# launch TIgerVNC server
# ref: https://www.thegeekdiary.com/how-to-install-and-configure-vnc-tigervnc-server-in-centos-rhel-7/
sudo systemctl enable vncserver_root@:2.service
systemctl daemon-reload
vncpasswd root
vncserver

# start IDL (TBD: development environment too)
idl

# get stuff from cpogpi computers
wget -v https://mwanakijiji.github.io/cv_20210926.pdf

# installation
