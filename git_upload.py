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
 
# remote: Permission to Jaykie/PythonUnity.git denied to helenmooncom.
def upload():

    
    # os.system("git config --global credential.helper store")
    # os.system("git config --global user.email \"chyfemail163@163.com\"")
    # os.system("git config --global user.name \"mooncode163\"")
    # os.system("git config --global user.password \"Qianlizhiwai1\"")
     
    os.system("git add .")
    os.system("git commit -m \"ui\"")
    # os.system("git commit")  
    
    # git branch -al 查看本地和远程的所有分支。
    os.system("git branch -al") 

    # os.system("git push -u origin master") 
    os.system("git push -f https://mooncode163:Qianlizhiwai1@github.com/mooncode163/PythonUnity.git")

   
 
# 主函数的实现
if __name__ == "__main__":

    upload() 

    print("git_upload end")
