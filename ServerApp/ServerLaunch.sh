#!/bin/sh 
# 命令后面加 & 后台执行多个sh
sh /var/www/html/PythonUnity/ServerApp/AppleJWTToken.sh & 
sh /var/www/html/PythonUnity/ServerApp/AppVersion.sh & 
sh /var/www/html/PythonUnity/ServerApp/YoutubDownload.sh & 
  
# vnc
# vncserver -kill :1
vncserver :1
# vncconfig  