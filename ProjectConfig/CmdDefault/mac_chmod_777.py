#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys
 
#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

# 设置为可执行文件
def UpdateMacFile(dir):
    for file in os.listdir(dir):
        filepath = os.path.join(dir,  file)
        if os.path.exists(filepath):
            # 分割文件名与后缀
            temp_list = os.path.splitext(file)
            # name without extension
            src_apk_name = temp_list[0]
            # 后缀名，包含.   例如: ".apk "
            src_apk_extension = temp_list[1]
            apk_ext='.bat'
            if apk_ext!=src_apk_extension: 
                os.system("chmod a+x "+filepath)
            
def ScanDir():  
    listDir= ["cmd_mac", "all_build"] 
    for dir in listDir:
        UpdateMacFile(dir)


# 主函数的实现
if __name__ == "__main__":

    ScanDir()

    print("ScanDir end")
