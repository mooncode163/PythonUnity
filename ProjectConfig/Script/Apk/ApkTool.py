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

class ApkTool():  
    
    # 使用apktool解包
    def DecodeApK(self,apk,output):
        cmd = "apktool d -f "+apk+" -o "+output
        os.system(cmd)

# 使用apktool重新打包
    def RebuildApK(self,apkdir,outputapk,signapk):
        # apktool b -f ./test/  -o test.apk
        cmd = "apktool b -f "+apkdir+" -o "+outputapk
        os.system(cmd)      



        apk_unsign = outputapk 
        apk_sign = signapk
        jks = mainResource.GetDirProductCommon()+"/Ad/moonma.jks"

        # jarsigner -verbose -keystore ~/sourcecode/mssp_baidu/moonma.jks -signedjar ~/sourcecode/mssp_baidu/signed.apk ~/sourcecode/mssp_baidu/empty.apk moonma -storepass qianlizhiwai
        cmd = "jarsigner -verbose -keystore "+jks+" -signedjar "+apk_sign+" "+apk_unsign+" moonma -storepass qianlizhiwai"
            
        print(cmd)
        os.system(cmd)

# 主函数的实现
    def Run(self,channel,isHD):  
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        print("ApkBuild isHD="+str(isHD))
        print("gameName="+gameName)
        print ("gameType="+gameType) 
      

        print("mainApkTool sucess channel="+channel)

mainApkTool = ApkTool()
