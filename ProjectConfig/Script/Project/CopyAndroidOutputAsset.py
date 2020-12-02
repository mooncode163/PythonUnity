#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime
import json
 

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Common import Source   
from Project.Resource import mainResource
from Common.Platform import Platform
from Project.CopyGamedata import mainCopyGamedata

class CopyAndroidOutputAsset(): 
    def CopyConfigDataToAndroid(self): 
        dir1 = mainResource.GetConfigDataDir()
        dir2 = mainResource.GetRootDirAndroidAsset()+ "/ConfigData"
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        # print(CopyConfigDataToAndroid:dir1=",dir1," dir2=",dir2
        shutil.copytree(dir1,dir2)

    def LoadJsonAndroidAssetConfigCommon(self):  
        jsonfile = mainResource.GetRootDirAndroidAsset()+"/ConfigData/config/config_common.json"
        with  open(jsonfile, 'rb') as json_file:
            data = json.load(json_file)
            return data


# 复制从unity打包输出的assets目录
#主函数的实现
    def Run(self): 
        gameType = mainResource.getGameType()
        gameName = mainResource.getGameName()

        rootAndroidStudio =mainResource.GetRootDirAndroidStudio()
 
    # android asset
        dir_asset = "/src/main/assets/bin"
        dir1 = mainResource.GetRootDirAndroidOutput()+dir_asset
        dir2 = rootAndroidStudio+dir_asset
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)
    
        dir_asset = "/src/main/assets/baidu_tts_data"
        dir1 = mainResource.GetRootDirAndroidOutput()+dir_asset
        dir2 = rootAndroidStudio+dir_asset
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)


        # android jniLibs
        dir_asset = "/src/main/jniLibs"
        dir1 = mainResource.GetRootDirAndroidOutput()+dir_asset
        dir2 = rootAndroidStudio+dir_asset
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)


        filename = "/libs/unity-classes.jar"
        shutil.copy2(mainResource.GetRootDirAndroidOutput()+filename, rootAndroidStudio+filename)

        dataJson = self.LoadJsonAndroidAssetConfigCommon()
        appNameAndroidAsset = dataJson["APP_NAME_KEYWORD"]
        appTypeAndroidAsset = dataJson["APP_TYPE"]
        print(appTypeAndroidAsset)
        print(appNameAndroidAsset)

        if appTypeAndroidAsset!=gameType or appNameAndroidAsset!=gameName:
            print("mainCopyGamedata DoCopyAll") 
            mainCopyGamedata.DoCopyAll()

        self.CopyConfigDataToAndroid()
        print("copy_android_output_asset sucess")   

mainCopyAndroidOutputAsset = CopyAndroidOutputAsset()