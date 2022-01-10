#!/bin/sh

echo $(date)

# launch TIgerVNC server
# ref: https://www.thegeekdiary.com/how-to-install-and-configure-vnc-tigervnc-server-in-centos-rhel-7/
# ref: https://itectec.com/ubuntu/ubuntu-how-to-start-and-stop-a-systemctl-service-inside-a-bash-script/

### ## may need to copy gpi file via
## ## >> sudo cp gpi /etc/sudoers.d/gpi
sudo systemctl enable vncserver_root@:2.service
systemctl daemon-reload
vncpasswd root
vncserver

# start IDL (TBD: development environment too)
idl

# get stuff from cpogpi computers
#wget -v [url]

# installation
