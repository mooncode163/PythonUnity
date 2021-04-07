#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime
 

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Common import Source  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 

class CopyGamedata(): 
    def getGameResName(self):
        name = mainResource.getGameName()
        idx = name.rfind('_')
        s_len=len(name)
        game = name[idx+1:s_len]
        return game

    def CopyConfigDataToAndroid(self): 
        dir1 = mainResource.GetConfigDataDir()+"/config"
        dir2 = mainResource.GetRootDirAndroidAsset()+ "/ConfigData/config"
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        # print "CopyConfigDataToAndroid:dir1=",dir1," dir2=",dir2
        shutil.copytree(dir1,dir2)

    def DoCopyAll(self):
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
            gameResRoot = gameResCommonRoot

        gameDataCommonRoot = mainResource.GetDirProductCommon()+"/GameDataCommon"
        gameDataRoot = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/GameData"

        streamingAssetsUnity = mainResource.GetRootProjectUnity()+"/Assets/StreamingAssets"
        rootAndroidStudio =mainResource.GetRootDirAndroidStudio()
        rootiOSXcode =mainResource.GetRootDirXcode()

        # copy GameRes 游戏图片等资源
        dirname = "GameRes"

        # unity editor 
        dir1 = gameResRoot
        # dir2 = streamingAssetsUnity+"/"+dirname
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

        # ios
        dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)


    # copy GameData 游戏配置等数据 
        dirname = "GameData"

        # unity editor 
        dir1 = gameDataRoot
        dir2 = streamingAssetsUnity+"/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # ios
        # dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        print("gamedata dir2=",dir2)
        shutil.copytree(dir1,dir2)


        dirname = "GameData/common"

        # unity editor 
        dir1 = gameDataCommonRoot
        dir2 = streamingAssetsUnity+"/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # ios
        # dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        self.CopyConfigDataToAndroid()

    def DoCopyGameData(self):
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
            gameResRoot = gameResCommonRoot

        gameDataCommonRoot = mainResource.GetDirProductCommon()+"/GameDataCommon"
        gameDataRoot = mainResource.GetResourceDataRoot()+"/"+gameType+"/"+gameName+"/GameData"

        streamingAssetsUnity = mainResource.GetRootProjectUnity()+"/Assets/StreamingAssets"
        rootAndroidStudio =mainResource.GetRootDirAndroidStudio()
        rootiOSXcode =mainResource.GetRootDirXcode()
 
    # copy GameData 游戏配置等数据 
        dirname = "GameData"

        # unity editor 
        dir1 = gameDataRoot
        dir2 = streamingAssetsUnity+"/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # ios
        # dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)


        dirname = "GameData/common"

        # unity editor 
        dir1 = gameDataCommonRoot
        dir2 = streamingAssetsUnity+"/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # ios
        # dir2 = rootiOSXcode+"/Data/Raw/"+dirname
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

    # android asset
        dir2 = rootAndroidStudio+"/src/main/assets/"+dirname
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # self.CopyConfigDataToAndroid()

#主函数的实现
    def Run(self):   
        self.DoCopyAll()

        print ("copy_gamedata sucess")

mainCopyGamedata = CopyGamedata()
