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
 

def download():

    
    # os.system("git config --global credential.helper store")
    # os.system("git config --global user.email \"chyfemail163@163.com\"")
    # os.system("git config --global user.name \"mooncode163\"")
    # os.system("git config --global user.password \"Qianlizhiwai1\"")
    
    # os.system("git pull origin master")
    # os.system("repo sync") 

    # git branch -al 查看本地和远程的所有分支。
    os.system("git branch -al") 

    # 直接采取暴力的方法，直接拉取并覆盖本地的所有代码 
    os.system("git fetch --all") 
    os.system("git reset --hard origin/master") 
    os.system("git pull") 
    

    # os.system("git reset --hard") 
    # os.system("git pull origin main")
    # os.system("git pull https://helenmooncom:helenmoon2020@github.com/helenmooncom/twolandlord_project_ios.git")

   
 
# 主函数的实现
if __name__ == "__main__":

    download() 

    print("git_download end")
