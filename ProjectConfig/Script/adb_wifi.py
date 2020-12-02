#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys

import socket

# include AppInfo.py
# sys.path.append('./common')
import AppInfo


sys.path.append('./common')
import common
class ConfigSDKAndroid(): 
def getIp():
    #获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    print myname
    print myaddr
    os.system("adb connect "+myaddr)

   
 
# 主函数的实现
if __name__ == "__main__":

    getIp() 

    print "adb_wifi end"
