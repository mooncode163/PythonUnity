#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys

# include AppInfo.py
# sys.path.append('./common')
import AppInfo 

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script 
sys.path.append('../../') 
sys.path.append('./')  
from Config.Config import mainConfig
from Common import Source
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil  
from AppInfo.AppChannel import mainAppChannel
from Common.Platform import Platform

class ApkBuild(): 
    builder:None
    listChannel = [] 
    def BuildClean(self): 
        targetDir = mainResource.GetRootDirAndroidStudio()
        # build
        dir2 = targetDir + "/build"
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)

        print("apk_build_clean sucess")


    def BuildApk(self):
        if Platform.isWindowsSystem():
            # dir1 = "C:\Program Files\Android\Android Studio\gradle"
            dir2 = "C:/moon/gradle/gradle-4.10.1"
            flag = os.path.exists(dir2)
            if not flag:
                # shutil.copytree(dir1,dir2)
                dir2 = "E:/Program Files/Android/Android Studio/gradle/gradle-4.10.1"
                flag = os.path.exists(dir2)
                if not flag:
                    # aliyun
                    dir2 = "C:/Program Files/Unity/Hub/Editor/"+source.UNITY_VERSION_WIN+"/Editor/Data/PlaybackEngines/AndroidPlayer/Tools/gradle"

    
            os.system(dir2+"/bin/gradle assembleRelease")
        else:
            dir2 = "/Users/moon/sourcecode/gradle/gradle-4.10.1/bin"
            flag = os.path.exists(dir2) 
            if flag:
                # os.system("chmod 777 "+dir2+"/gradle")
                os.system(dir2+"/gradle assembleRelease")
            else:
                os.system("gradle assembleRelease")
        


    def CopyApk(self,channel):
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
    # copy2 同时复制文件权限
        dirapk = mainResource.GetProjectOutPutApp() + "/apk"
        if mainResource.AppForPad(False):
            dirapk+="/heng"
            gameName += "_hd"
        else:
            dirapk+="/shu"

        if not os.path.exists(dirapk):
            os.makedirs(dirapk)

        shutil.copy2(mainResource.getAndroidProjectApk(), dirapk + "/" +
                    gameType + "_" + gameName + "_" + channel + ".apk")
    def Init(self,channel): 
        self.listChannel.clear()
        if channel==Source.HUAWEI:
            self.listChannel.append(Source.HUAWEI)
        if channel==Source.TAPTAP:
            self.listChannel.append(Source.TAPTAP)
        if channel==Source.GP:
            self.listChannel.append(Source.GP)
        if channel=="all":
            self.listChannel.append(Source.HUAWEI)
            self.listChannel.append(Source.TAPTAP)
            self.listChannel.append(Source.GP)
 
        
# 主函数的实现
    def Run(self,channel,isHD):  
        self.Init(channel)
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        print("ApkBuild isHD="+str(isHD))
        print("gameName="+gameName)
        print ("gameType="+gameType) 
        print(mainResource.getAndroidProjectApk())
        # python 里无法直接执行cd目录，想要用chdir改变当前的工作目录
        android_studio_dir = mainResource.GetRootDirAndroidStudio()
        # python 里无法直接执行cd目录，要用chdir改变当前的工作目录
        os.chdir(android_studio_dir)
        for channel in self.listChannel:
            print("apk_build:" + channel)
            self.BuildClean()
            mainAppChannel.UpdateChannel(channel,isHD) 
            self.BuildApk()
            self.CopyApk(channel)

        print("apk_build sucess channel="+channel)

mainApkBuild = ApkBuild()
