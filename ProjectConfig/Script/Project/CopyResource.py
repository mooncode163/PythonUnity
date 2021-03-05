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
from Common.File.ZipUtil import ZipUtil
from Config.Config import mainConfig
from Common import Source

class CopyResource(): 
    def CopyPlugins(self):
        dirname = "Plugins"
        dir1 = mainResource.GetDirProductCommon()+"/"+dirname
        dir2 = mainResource.GetRootUnityAssets()+"/"+dirname
        flag = os.path.exists(dir2)
        if not flag:
            # shutil.rmtree(dir2)
            shutil.copytree(dir1,dir2)

        self.ConfigiOSPluginsCode()

    def IsNoIDFASDK(self):
        return mainConfig.IsNoIDFASDK()


    def DeleteMACOSX(self,root_dir):
        macosx_dir = root_dir+"/__MACOSX"
        flag = os.path.exists(macosx_dir)
        if flag:
            shutil.rmtree(macosx_dir)


    def ConfigiOSLib(self,source_lib):
        dirRoot = mainResource.GetRootUnityAssets()+"/Plugins/iOS"
        dirLib = dirRoot+"/ThirdParty"

        FileUtil.RemoveDir(dirLib+"/"+source_lib)
        if not self.IsNoIDFASDK():
            zipfile = dirLib+"/"+source_lib+".zip"
            ZipUtil.un_zip(zipfile,dirLib)

        self.DeleteMACOSX(dirLib)

    def ConfigiOSAdkitCode(self,source_ad):
        dirRoot = mainResource.GetRootUnityAssets()+"/Plugins/iOS"
        dirCodeAdkitPlatform = dirRoot+"/Common/AdKit/Platform"

        FileUtil.RemoveDir(dirCodeAdkitPlatform+"/"+source_ad)
        if not self.IsNoIDFASDK():
            zipfile = dirCodeAdkitPlatform+"/"+source_ad+".zip"
            ZipUtil.un_zip(zipfile,dirCodeAdkitPlatform)

    def ConfigiOSPluginsCode(self):
        dirRoot = mainResource.GetRootUnityAssets()+"/Plugins/iOS"
        dirCodeCommon = dirRoot+"/Common"
 
        dirCodeAdkit = dirRoot+"/Common/AdKit"

        # tongji
        FileUtil.RemoveDir(dirCodeCommon+"/Tongji")
        zipfile = dirCodeCommon+"/Tongji.zip" 
        if self.IsNoIDFASDK(): 
            zipfile = dirCodeCommon+"/Tongji_NoSDK.zip" 
        flag = os.path.exists(zipfile)
        if flag:
            ZipUtil.un_zip(zipfile,dirCodeCommon)

        # share
        FileUtil.RemoveDir(dirCodeCommon+"/Share")
        zipfile = dirCodeCommon+"/Share.zip" 
        if self.IsNoIDFASDK(): 
            zipfile = dirCodeCommon+"/Share_NoSDK.zip" 
        flag = os.path.exists(zipfile)
        if flag:
            ZipUtil.un_zip(zipfile,dirCodeCommon)


        # adconfig
        FileUtil.RemoveDir(dirCodeAdkit+"/AdConfig")
        zipfile = dirCodeAdkit+"/AdConfig.zip" 
        if self.IsNoIDFASDK(): 
            zipfile = dirCodeAdkit+"/AdConfig_NoSDK.zip" 
        flag = os.path.exists(zipfile)
        if flag:
            ZipUtil.un_zip(zipfile,dirCodeAdkit)



        # adkit
        self.ConfigiOSLib(Source.GDT)
        self.ConfigiOSLib(Source.BAIDU)
        self.ConfigiOSLib(Source.ADMOB)
        self.ConfigiOSLib(Source.CHSJ)
        self.ConfigiOSLib(Source.UNITY)
        self.ConfigiOSLib(Source.UMENG)

        self.ConfigiOSAdkitCode(Source.GDT)
        self.ConfigiOSAdkitCode(Source.BAIDU)
        self.ConfigiOSAdkitCode(Source.ADMOB)
        self.ConfigiOSAdkitCode(Source.CHSJ)
        self.ConfigiOSAdkitCode(Source.UNITY) 



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
