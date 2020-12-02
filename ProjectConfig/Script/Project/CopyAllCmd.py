#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys

# o_path = os.getcwd()  # 返回当前工作目录
# sys.path.append(o_path)  # 添加自己指定的搜索路径

sys.path.append('../../') 
sys.path.append('./')  
from Project.Resource import mainResource
from Common.Platform import Platform

class CopyAllCmd():  

# 设置为可执行文件
    def UpdateMacFile(self,dir):
        for file in os.listdir(dir):
            filepath = os.path.join(dir,  file)
            if os.path.exists(filepath):
                os.system("chmod a+x "+filepath)
                
    def ScanDir(self,sourceDir,dir2):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file) 
            if os.path.isdir(sourceFile): 
                if Platform.isWindowsSystem():
                    key = "/cmd_win" 
                else:
                    key = "/cmd_mac"

                dirsrc = mainResource.GetProjectConfigDefault()+key
                dir = sourceFile+key
                flag = os.path.exists(dir)
                if flag:
                    shutil.rmtree(dir)
                    shutil.copytree(dirsrc,dir)
                    if Platform.isMacSystem():
                        self.UpdateMacFile(dir)
 
    
    def Run(self):
        cmdPath = mainResource.cmdPath
        dir2 = cmdPath
        if Platform.IsVMWare():
            cmdPath="/Volumes/VMware Shared Folders/"+cmdPath
        print ("dir2="+dir2)
        self.ScanDir(cmdPath,dir2)


        

mainCopyAllCmd = CopyAllCmd()
      
