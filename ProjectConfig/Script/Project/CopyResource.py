#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime

#include common.py
sys.path.append('../../') 
sys.path.append('./')  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 

class CopyResource(): 
    def CopyPlugins(self):
        dirname = "Plugins"
        dir1 = mainResource.GetDirProductCommon()+"/"+dirname
        dir2 = mainResource.GetRootUnityAssets()+"/"+dirname
        flag = os.path.exists(dir2)
        if not flag:
            # shutil.rmtree(dir2)
            shutil.copytree(dir1,dir2)

    def CopyResConfigData(self):
        # ResConfigDataCommon 
        reousceDataRoot = mainResource.GetResourceDataRoot() 
        dirname = "ConfigDataCommon"
        dirUnity = mainResource.GetRootProjectUnity()+ "/Assets/Resources"
        dir1 = reousceDataRoot+"/"+dirname
        dir2 = dirUnity+"/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)
        
        # ConfigData
        dir1 = mainResource.GetConfigDataDir()
        dir2 = dirUnity+"/ConfigData"
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)


#主函数的实现
    def Run(self): 
        # resoucedata 
        gameType = mainResource.getGameType()
        gameName = mainResource.getGameName()
        dir1 = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/"+"Resources/App"
        dir2 = mainResource.GetRootProjectUnity()+"/Assets/Resources/App" 
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        print("copytree dir2 =",dir2)
        shutil.copytree(dir1,dir2)

        # AppCommon
        dir1 = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+"AppCommon/Resources"
        dir2 = mainResource.GetRootProjectUnity()+"/Assets/Resources/AppCommon" 
        FileUtil.CopyDir(dir1,dir2)

        self.CopyResConfigData()

        self.CopyPlugins()

        print ("copy_resource sucess")

mainCopyResource = CopyResource()
