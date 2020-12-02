#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time
import datetime
import json

#include mainResource.py
# sys.path.append('./common')

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
sys.path.append('../../') 
sys.path.append('./') 
from Config.Config import Config
from Common import Source
from Config.AdConfig import AdConfig  
from Project.Resource import mainResource
from Common.File.JsonUtil import JsonUtil 
from xml.dom.minidom import parse
 
 
class AppInfoOld():  
    rootJsonData: None 
    isHd:None
    #构造函数
    def __init__(self,isHd):
        self.isHd = isHd
        self.rootJsonData = self.loadJson(isHd)

    def saveString2File(self, str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8', "ignore")
        f.write(b)
        f.close()

 



    def GetJsonFile(self,isHd):
        cur_path = mainResource.GetProjectConfigApp()+"/appinfo"
        jsonfile = cur_path+'/appinfo.json'
        if isHd:
            jsonfile = cur_path+'/appinfo_hd.json'
        return jsonfile

    def loadJson(self,isHd): 
        jsonfile = self.GetJsonFile(isHd) 
        
        with  open(jsonfile, 'rb') as json_file:
            data = json.load(json_file)
            return data

    def IsOldVersion(self):
        isOld = True
        if ("appname" in self.rootJsonData) :
            isOld = False  
        return isOld
    

    def saveString2File(self,str, file):
        mainResource.saveString2File(str, file)

        
    def GetPackage(self,osSrc): 
        jsonData = self.rootJsonData  
        ret = "" 
        key = "PACKAGE_IOS"
        if osSrc == Source.ANDROID:
            key = "PACKAGE_ANDROID" 
        ret = jsonData[key]
        return ret

    def GetConfigDataAppId(self,os,chanel):
        dirconfig = mainResource.GetConfigDataDir()
        filepath = ""
        appid = ""
        if os==Source.ANDROID:
            filepath = dirconfig+"/config/config_android.json"
            if self.isHd:
                filepath = dirconfig+"/config/config_android_hd.json"
    
        if os==Source.IOS:
            filepath = dirconfig+"/config/config_ios.json"
            if self.isHd:
                filepath = dirconfig+"/config/config_ios_hd.json"
        

        with open(filepath) as json_file:
            data = json.load(json_file)
            appid = data["APPID"][chanel] 

        return appid
    
    def APPSTORE_PROMOTION(self,lan): 
        data = self.rootJsonData["APPSTORE_PROMOTION"]
        name = data[lan] 
        return name 

    def APPSTORE_VERSION_UPDATE(self,lan): 
        data = self.rootJsonData["APPSTORE_VERSION_UPDATE"]
        name = data[lan] 
        return name 

    def APPSTORE_TITLE(self,lan): 
        data = self.rootJsonData["APPSTORE_TITLE"]
        name = data[lan] 
        return name 

    def APPSTORE_SUBTITLE(self,lan): 
        data = self.rootJsonData["APPSTORE_SUBTITLE"]
        name = data[lan] 
        return name 

    def APPSTORE_KEYWORD(self,lan): 
        data = self.rootJsonData["APPSTORE_KEYWORD"]
        name = data[lan] 
        return name 
 
    def need_upload_screenshot(self):  
        return self.rootJsonData["need_upload_screenshot"]

    def software_url(self):  
        return self.rootJsonData["software_url"]

    def privacy_url(self):  
        return self.rootJsonData["privacy_url"]

    def support_url(self):  
        return self.rootJsonData["support_url"]
    def sku_app(self):  
        return self.rootJsonData["sku_app"]

    def GetAppVersion(self,os): 
        # loadJson
        data = self.rootJsonData   
        if os==Source.ANDROID:
            name = data["APPVERSION_ANDROID"]
        if os==Source.IOS:
            name = data["APPVERSION_IOS"]

        return name

    def GetAppVersionCode(self,os): 
        # loadJson
        data = self.rootJsonData   
        if os==Source.ANDROID:
            name = data["APPVERSION_CODE_ANDROID"]
        if os==Source.IOS:
            name = data["APPVERSION_IOS"]
            name = name.replace(".","")

        return name


    def GetAppName(self,os,lan): 
        # loadJson
        data = self.rootJsonData 
 
        
        APP_NAME_CN_ANDROID = data["APP_NAME_CN_ANDROID"]
        APP_NAME_EN_ANDROID = data["APP_NAME_EN_ANDROID"]
        APP_NAME_CN_IOS = data["APP_NAME_CN_IOS"]
        APP_NAME_EN_IOS = data["APP_NAME_EN_IOS"] 
        name = ""
        if os==Source.ANDROID:
            if lan==Source.LANGUAGE_CN:
                name = APP_NAME_CN_ANDROID
            if lan==Source.LANGUAGE_EN:
                name = APP_NAME_EN_ANDROID

        if os==Source.IOS:
            if lan==Source.LANGUAGE_CN:
                name = APP_NAME_CN_IOS
            if lan==Source.LANGUAGE_EN:
                name = APP_NAME_EN_IOS


        return name     
        
            
    def GetAppId(self,channel): 
        # loadJson
        data = self.rootJsonData 
   
        if channel==Source.APPSTORE:
            appid = self.GetConfigDataAppId(Source.IOS,Source.APPSTORE)
        else:
            appid = self.GetConfigDataAppId(Source.ANDROID,channel)
 

        return appid 
 
    
  


# 主函数的实现
if __name__ == "__main__":
    # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    is_auto_plus_version = False
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = mainResource.cur_file_dir()
    count = len(sys.argv)
    for i in range(1,count):
        print("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i]
        if i==2:
            if sys.argv[i]=="true":
                is_auto_plus_version = True

    mainResource.SetCmdPath(cmdPath)
    
 
    
    print("AppInfoOld sucess")
