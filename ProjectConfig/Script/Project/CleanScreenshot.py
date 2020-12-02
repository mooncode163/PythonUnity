#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime

sys.path.append('../../') 
sys.path.append('./') 
from Common import Source
from Project.Resource import mainResource

class CleanScreenshot():   
    def getGameResName(self):
        name = mainResource.getGameName()
        idx = name.rfind('_')
        s_len=len(name)
        game = name[idx+1:s_len]
        return game

    #主函数的实现
    def Run(self):
 
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        print(gameName)
        print(gameType)

        resDataName = mainResource.getGameName()#sys.argv[1]
        gameResName = self.getGameResName()

        gameResCommonRoot = mainResource.GetDirProductCommon()+"/GameResCommon"+"/"+gameResName
        gameResRoot = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/GameRes"
        flag = os.path.exists(gameResRoot)
        if not flag:
            #目录不存在的话到gamerescommon里copy
            gameResRoot = gameResCommonRoot;

        gameDataRoot = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/GameData"

        streamingAssetsUnity = mainResource.GetRootProjectUnity()+"/Assets/StreamingAssets"
        rootAndroidStudio = mainResource.GetRootDirAndroidStudio()
        rootiOSXcode =mainResource.GetRootDirXcode()

        
    # copy GameData 游戏配置等数据 
        dirname = "GameData/screenshot"
        # ios
        dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2) 

        dirname = "GameData/screenshot"
    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2) 


        print("clean_screenshot sucess")

mainCleanScreenshot = CleanScreenshot()
