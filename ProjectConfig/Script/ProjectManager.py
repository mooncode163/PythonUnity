#!/usr/bin/python
# coding=utf-8
from Project.UpdateAppstore import mainUpdateAppstore
from Common.File.FileUtil import FileUtil
from xml.dom.minidom import parse
from AppInfo.AppInfo import mainAppInfo
from AppStore.AppStoreApple import mainAppStoreApple
from AppInfo.AppCode import mainAppCode
from Project.CopyGamedata import mainCopyGamedata
from Project.IPABuild import IPABuild
from Project.IPABuild import mainIPABuild
from AppStore.AppstoreUploadiOS import mainAppstoreUploadiOS
from AppStore.AppStoreTaptap import mainAppStoreTaptap

from Project.CopyAllCmd import mainCopyAllCmd
from Project.UnityBuild import UnityBuild
from Project.CleanScreenshot import mainCleanScreenshot
from Project.CopyAndroidOutputAsset import mainCopyAndroidOutputAsset
from Project.SaveResource import mainSaveResource
from Project.CopyResource import mainCopyResource
from Project.CopyConfig import mainCopyConfig
from Common import Source
from Apk.ApkBuild import mainApkBuild
from Project.Resource import mainResource
from Common.Common import Common
import sys
import zipfile
import shutil
import os
import os.path
import time
import datetime
import json

# include common.py
#
o_path = os.getcwd()  # 返回当前工作目录
print(o_path)
sys.path.append(o_path)  # 添加自己指定的搜索路径
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../')
sys.path.append('./')

fille = os.path.abspath(__file__)
print(fille)
dir = os.path.dirname(fille)
print(dir)
# sys.path.append("..") #把上级目录加入到变量中
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)
print(dir)
# sys.path.insert(0,dir)
# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(sys.path)


# from Config import config
# from Config import adconfig


class ProjectManager():
    # 构造函数
    def __init__(self):
        name = ""

    # def CopyProjectConfig(self):
    #     listname ={"default","script"}
    #     for name in listname:
    #         src = mainResource.GetDirProductCommon()+"/ProjectConfig/"+name
    #         dst = mainResource.GetProjectConfig()+"/"+name
    #         isremove = True
    #         if name=="script":
    #             isremove = False
    #         FileUtil.CopyDir(src,dst,isremove)

    # def SaveProjectConfig(self):
    #     listname ={"default","script"}
    #     for name in listname:
    #         src = mainResource.GetProjectConfig()+"/"+name
    #         dst = mainResource.GetDirProductCommon()+"/ProjectConfig/"+name
    #         print(src)
    #         print(dst)
    #         FileUtil.CopyDir(src,dst)

    def CopyCommonScript(self):
        listname = {"AppBase", "Common"}
        for name in listname:
            src = mainResource.GetDirProductCommon()+"/ProjectUnity/Assets/Script/"+name
            dst = mainResource.GetRootUnityAssets()+"/Script/"+name
            FileUtil.CopyDir(src, dst)

    def SaveCommonScript(self):
        listname = {"AppBase", "Common"}
        for name in listname:
            src = mainResource.GetRootUnityAssets()+"/Script/"+name
            dst = mainResource.GetDirProductCommon()+"/ProjectUnity/Assets/Script/"+name
            print(src)
            print(dst)
            FileUtil.CopyDir(src, dst)

    def DoCopyConfig(self, isHd):
        # mainCopyConfig.Run(False)
        mainCopyConfig.Run(isHd)
        self.CopyAppInfo(isHd)
 
    def CopyResource(self):
        mainCopyResource.Run()
        mainCopyGamedata.DoCopyGameData()
        mainAppCode.Run("copy")

    def SaveResource(self):
        mainSaveResource.Run()
        mainAppCode.Run("save")

    def CopyGamedata(self):
        mainCopyGamedata.Run()

    def UpdateAppInfo(self,channel=""):
        mainUpdateAppstore.Run(False)
        mainAppInfo.Run(False,channel) 
        mainAppStoreTaptap.UpLoadVesionDB()

    def UpdateAso(self):
        mainAppStoreApple.UpdateAso(False)
        mainAppStoreApple.UpdateAso(True)

    def UpdateAppInfoAuto(self,channel=""):
        # mainAppInfo.Run(True)
        # mainUpdateAppstore.Run(False)
        mainAppInfo.Run(True,channel) 
        mainAppStoreTaptap.UpLoadVesionDB()
 

    def CopyAndroidOutputAsset(self):
        mainCopyAndroidOutputAsset.Run()

    def CopyAppInfo(self,isHd,channel=""):
        # mainAppInfo.Run(True)
        # mainUpdateAppstore.Run(False)
        mainAppInfo.Copy(isHd,channel)

    def ApkBuild(self, channel, isHd):
        self.CopyAppInfo(isHd,channel)
        mainCopyAndroidOutputAsset.Run()
        mainCopyConfig.Run(isHd)
        mainCleanScreenshot.Run()
        mainApkBuild.Run(channel, isHd)

    def InstallApk(self, channel, isHd):
        apk = mainApkBuild.GetApk(channel,isHd)
        print("apk=",apk)
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHd,channel) 
        try: 
            os.system("adb uninstall "+package)
        except Exception as e:  
            print("adb uninstall eror=",e," package =",package)

        os.system("adb install "+apk)

    def CopyAllCmd(self):
        mainCopyAllCmd.Run()

    def UnityBuild(self, stros):
        UnityBuild.Run(stros)
        # mainCopyGamedata.DoCopyGameData()

    def IPABuild(self, type):
        mainIPABuild.Run(type)

    def UpdateAppstore(self, isHd):
        mainUpdateAppstore.Run(isHd)
        self.AppstoreUploadiOS(isHd) 

    def AppstoreUploadiOS(self, isHd):
        mainAppstoreUploadiOS.Run(isHd)


# 主函数的实现
if __name__ == "__main__":
    # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    is_auto_plus_version = False
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)
    arg3 = ""
    arg4 = ""
    for i in range(1, count):
        print("参数", i, sys.argv[i])
        if i == 1:
            cmdPath = sys.argv[i]
        if i == 3:
            arg3 = sys.argv[i]
        if i == 4:
            arg4 = sys.argv[i]

    mainResource.SetCmdPath(cmdPath)

    p = ProjectManager()

    print(mainResource.GetDirProduct())
    print(mainResource.GetRootDir())
    arg = sys.argv[2]
    if arg == "CopyProjectConfig":
        p.CopyProjectConfig()
    if arg == "SaveProjectConfig":
        p.SaveProjectConfig()
    if arg == "CopyCommonScript":
        p.CopyCommonScript()
    if arg == "SaveCommonScript":
        p.SaveCommonScript()
    if arg == "CopyConfig":
        isHd = False
        if arg3 == "hd":
            isHd = True
        p.DoCopyConfig(isHd)
    if arg == "CopyResource":
        p.CopyResource()
    if arg == "SaveResource":
        p.SaveResource()
    if arg == "UpdateAppInfo":
        p.UpdateAppInfo()
        
    if arg == "UpdateAso":
        p.UpdateAso()
    if arg == "UpdateAppInfoAuto":
        p.UpdateAppInfo()
        p.UpdateAppInfoAuto()

    if arg == "CopyGamedata":
        p.CopyGamedata()

    if arg == "CopyAndroidOutputAsset":
        p.CopyAndroidOutputAsset()

    if arg == "ApkBuild":
        # isHd = False
        # if arg4 =="hd":
        #     isHd = True

        p.ApkBuild(arg3, False)
        p.ApkBuild(arg3, True)

    if arg == "InstallApk":
        isHd = False
        if arg4 =="hd":
            isHd = True
        p.InstallApk(arg3, isHd) 

    if arg == "CopyAllCmd":
        p.CopyAllCmd()

    if arg == "UnityBuild":
        if Source.ScreenShot==arg3:
            p.CopyResource()
        p.UnityBuild(arg3)
 
    if arg == "IPABuild":
        p.IPABuild(arg3)

    if arg == "CopyXcodeProject":
        p.IPABuild(arg3)


    if arg == "UpdateAppstore":
        p.UpdateAppstore(False)
        p.UpdateAppstore(True)

    if arg == "AppstoreUploadiOS":
        p.AppstoreUploadiOS(False)

    if arg == "AppstoreUploadHDiOS":
        p.AppstoreUploadiOS(True)

    if arg == "test":
        p.CopyAllCmd()

    print("ProjectManager sucess arg=", arg)
