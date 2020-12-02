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
from Config.Config import mainConfig
from Common import Source
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 

class SaveResource(): 
#主函数的实现
    def Run(self): 
        gameType = mainResource.getGameType()
        gameName = mainResource.getGameName()

        configDirUnity = mainResource.GetRootProjectUnity()+"/Assets/Resources/ConfigData/config"

        configAppType = mainConfig.GetConfigAppType(configDirUnity)
        configAppName = mainConfig.GetConfigAppName(configDirUnity)
        print ("unity:"+configAppType+" "+configAppName)

        if gameType!=configAppType or gameName!=configAppName:
            print ("check app type and name fail")
            sys.exit(0)


        dir1 = mainResource.GetRootProjectUnity()+"/Assets/Resources/App"
        dir2 = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/"+"Resources/App"
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # AppCommon
        dir1 = mainResource.GetRootProjectUnity()+"/Assets/Resources/AppCommon" 
        dir2 = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+"AppCommon/Resources"
        flag = os.path.exists(dir2)
        FileUtil.CopyDir(dir1,dir2)

    # ConfigData
        dir1 = mainResource.GetRootProjectUnity()+"/Assets/Resources/ConfigData" 
        dir2 = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/ConfigData"
        flag = os.path.exists(dir2)
        FileUtil.CopyDir(dir1,dir2)


        print ("save_resource sucess")    

mainSaveResource = SaveResource()  