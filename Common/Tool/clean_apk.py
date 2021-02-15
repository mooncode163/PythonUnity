#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
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
 
def scanApkFiles(sourceDir):
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
            #cover the files
        if os.path.isfile(sourceFile):
            # print sourceFile
            # 分割文件名与后缀
            temp_list = os.path.splitext(file)
            # name without extension
            src_apk_name = temp_list[0]
            # 后缀名，包含.   例如: ".apk "
            src_apk_extension = temp_list[1] 
            if '.apk'==src_apk_extension:
                print(sourceFile)
                os.remove(sourceFile)
                
        #目录嵌套
        if os.path.isdir(sourceFile):
            # print sourceFile
            scanApkFiles(sourceFile)
 
     


curDir = cur_file_dir()
scanApkFiles(curDir)   
       
