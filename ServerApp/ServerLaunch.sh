#!/bin/sh 


cd /var/www/html/PythonUnity/ServerApp/AppVersion
python3 AppVersion.py


# vnc
# vncserver -kill :1
vncserver :1
# vncconfig