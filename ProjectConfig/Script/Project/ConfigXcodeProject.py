#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
# from Common import Source 
# from Common import common
#include common.py
# sys.path.append('./common')
from Common import common
from Common import Source
from Common import adconfig
import AppInfo
import config_adsdk_android

class ConfigXcodeProject(): 
    def ConfigXcodeProjectFile(self,fileProject):  
        strFile = common.GetFileString(fileProject)  

        
    #  		OTHER_LDFLAGS = (
    # 					"$(inherited)",
    # 					"-weak_framework",
    # 					CoreMotion,
    # 					"-weak-lSystem",
    # 				);
                    # 
        strold = "\"-weak-lSystem\","
        strnew = "\"-weak-lSystem\",\n\"-ObjC\","   
        idx = strFile.find(strnew)
        if idx >= 0:
            return 

        strFile = strFile.replace(strold,strnew)

        # DEVELOPMENT_TEAM
        strold = "DEVELOPMENT_TEAM = \"\""
        strnew = "DEVELOPMENT_TEAM = \"Y9ZUK2WTEE\""   
        strFile = strFile.replace(strold,strnew)

        
        common.saveString2File(strFile,fileProject)

#主函数的实现
if  __name__ =="__main__":
    
      # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    
    #入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = common.cur_file_dir() 
    count = len(sys.argv)
    for i in range(1,count):
        print("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i] 

    common.SetCmdPath(cmdPath)
    gameName = common.getGameName()
    gameType = common.getGameType()
    print(gameName)
    print(gameType) 

    rootiOSXcode = common.GetRootDirXcode()
    xcodeProject = rootiOSXcode+"/Unity-iPhone.xcodeproj/project.pbxproj"
    
 
    # ConfigXcodeProjectFile(xcodeProject)
 
    print("config_xcode_project sucess") 
