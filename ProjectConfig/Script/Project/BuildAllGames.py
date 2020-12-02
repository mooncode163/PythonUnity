#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys

# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
 
from Common import Source
from Project.Resource import mainResource
from Common.Platform import Platform

class BuildAllGames():  

    def ScanDirs(self,sourceDir,channel,dir2):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file) 
            if os.path.isdir(sourceFile):
                # python 里无法直接执行cd目录，想要用chdir改变当前的工作目录
                if Platform.isWindowsSystem():
                    os.chdir(sourceFile+"/cmd_win")
                    os.system("echo.| copy_cmd.bat")
                else:
                    dirapp = dir2+"/"+file+"/cmd_mac" 
                    if Platform.IsVMWare():
                        dirapp = "/Volumes/VMware\\ Shared\\ Folders/"+dir2+"/"+file+"/cmd_mac"
                        # os.system("cd /Volumes/VMware\\ Shared\\ Folders")
                        
                        # cmdPath="/Volumes/VMware Shared Folders/"+cmdPath
                    
                        os.system("cd "+dirapp)
                    else:
                        os.chdir(dirapp)
                    
                    os.system("sh "+"./copy_cmd")
                    # os.system("sh "+dirapp+"/build_all_ios")

                print(file)
                # update_appname build_huawei
                
                if channel=="huawei":
                    os.system("echo.| call build_huawei.bat")
                if channel=="gp":
                    os.system("echo.| call build_gp.bat")
                if channel=="android":
                    os.system("echo.| call build_all_android.bat")
                if channel=="ios":
                    if Platform.isWindowsSystem():
                        os.system("echo.| build_all_ios.bat")
                    # else:
                        # os.system("build_all_ios")
                        # os.system("cd "+dirapp)
                        os.system("sh "+"./build_all_ios")
                
                if channel=="ios_copy_cmd":
                    print("ios_copy_cmd")

                

    
# 主函数的实现
if __name__ == "__main__":

     # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    print ("脚本名：", sys.argv[0])
    cmdPath = cur_file_dir()
    count = len(sys.argv)
    channel = ""

    for i in range(1, count):
        print ("参数", i, sys.argv[i])
        if i == 1:
            cmdPath = sys.argv[i]

        if i == 2:
            channel = sys.argv[i] 

    dir2 = cmdPath
    if Platform.IsVMWare():
        cmdPath="/Volumes/VMware Shared Folders/"+cmdPath

    print ("dir2="+dir2)


    ScanDir(cmdPath,channel,dir2)

    print  ("build_huawei sucess")
