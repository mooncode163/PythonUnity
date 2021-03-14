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
# sys.path.append(o_path)  # 添加自己指定的搜索路径
# from Common import common
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Config.Config import Config
from Common import Source
from Config.AdConfig import AdConfig  
from Project.Resource import mainResource
from Common.File.JsonUtil import JsonUtil 
from xml.dom.minidom import parse
 
 
class AppInfoNew():  
    rootJsonData: None 
    rootJsonDataConvert: None 
    isHd:None
    #构造函数
    def __init__(self,isHd):
        self.isHd = isHd
        self.rootJsonData = self.loadJson(isHd) 
        self.rootJsonDataConvert = json.loads("{}")
 


    def GetJsonFile(self,isHd):
        cur_path = mainResource.GetProjectConfigApp()+"/appinfo"
        jsonfile = cur_path+'/appinfo.json'
        if isHd:
            jsonfile = cur_path+'/appinfo_hd.json'
        return jsonfile

    def GetJsonFileConVert(self,isHd):
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
  
        
    def GetPackage(self,osSrc): 
        jsonData = self.rootJsonData  
        ret = "" 
        key = "PACKAGE_IOS"
        if osSrc == source.ANDROID:
            key = "PACKAGE_ANDROID" 
        ret = jsonData[key]
        return ret

    def GetConfigDataAppId(self,os,chanel):
        dirconfig = mainResource.GetConfigDataDir()
        filepath = ""
        appid = ""
        if os==source.ANDROID:
            filepath = dirconfig+"/config/config_android.json"
            if self.isHd:
                filepath = dirconfig+"/config/config_android_hd.json"
    
        if os==source.IOS:
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

    def GetPROMOTION(self,lan): 
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
        if os==source.ANDROID:
            name = data["APPVERSION_ANDROID"]
        if os==source.IOS:
            name = data["APPVERSION_IOS"]

        return name

    def GetAppVersionCode(self,os): 
        # loadJson
        data = self.rootJsonData   
        if os==source.ANDROID:
            name = data["APPVERSION_CODE_ANDROID"]
        if os==source.IOS:
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
        if os==source.ANDROID:
            if lan==source.LANGUAGE_CN:
                name = APP_NAME_CN_ANDROID
            if lan==source.LANGUAGE_EN:
                name = APP_NAME_EN_ANDROID

        if os==source.IOS:
            if lan==source.LANGUAGE_CN:
                name = APP_NAME_CN_IOS
            if lan==source.LANGUAGE_EN:
                name = APP_NAME_EN_IOS


        return name     
            
            
    def GetAppId(self,channel): 
        # loadJson
        data = self.rootJsonData 
   
        if channel==source.IOS:
            appid = GetConfigDataAppId(source.IOS,source.APPSTORE)
        else:
            appid = GetConfigDataAppId(source.ANDROID,channel)
 

        return appid 
 
    
    def Save(self): 
        JsonUtil.SaveJson(self.GetJsonFileConVert(self.isHd),self.rootJsonDataConvert)

    def SetAppId(self,channel,appid):  
        data = self.rootJsonDataConvert 
        
        if "appid" in data:
            dataAppId = data["appid"]
        else:
            dataAppId = json.loads("{}")
            data["appid"] = dataAppId

        dataAppId[channel] = appid 
 
        

    def SetAppName(self,os,lan,name):

        data = self.rootJsonDataConvert 
        if "appname" in data:
            dataApp = data["appname"]
        else:
            dataApp = json.loads("{}")
            data["appname"] = dataApp

        if os in dataApp:
            dataOS = dataApp[os]
        else:
            dataOS = json.loads("{}")
            dataApp[os] = dataOS

        dataOS[lan] = name
 

    def SetAppPackage(self,os,value):

        data = self.rootJsonDataConvert 
        if "apppackage" in data:
            dataApp = data["apppackage"]
        else:
            dataApp = json.loads("{}")
            data["apppackage"] = dataApp

        if os in dataApp:
            dataOS = dataApp[os]
        else:
            dataOS = json.loads("{}")
            dataApp[os] = dataOS

        dataOS["default"] = value
 


    def SetJsonItem(self,dataApp,lan,key,value): 
        if key in dataApp:
            dataItem = dataApp[key]
        else:
            dataItem = json.loads("{}")
            dataApp[key] = dataItem

        dataItem[lan] = value


    def SetAppstore(self,lan,aso,aso_xiaomi,promotion,subtitle,title,version_update):

        data = self.rootJsonDataConvert 
        if "appstore" in data:
            dataApp = data["appstore"]
        else:
            dataApp = json.loads("{}")
            data["appstore"] = dataApp
 
        self.SetJsonItem(dataApp,lan,"aso",aso)
        self.SetJsonItem(dataApp,lan,"aso_xiaomi",aso_xiaomi)
        self.SetJsonItem(dataApp,lan,"promotion",promotion)
        self.SetJsonItem(dataApp,lan,"subtitle",subtitle)
        self.SetJsonItem(dataApp,lan,"title",title)
        self.SetJsonItem(dataApp,lan,"version_update",version_update)
  

    def SetAppversion(self,os,code,value):

        data = self.rootJsonDataConvert 
        key = "appversion"
        if key in data:
            dataApp = data[key]
        else:
            dataApp = json.loads("{}")
            data[key] = dataApp
 
        if os in dataApp:
            dataOS = dataApp[os]
        else:
            dataOS = json.loads("{}")
            dataApp[os] = dataOS

        dataOS["code"] = code
        dataOS["value"] = value
        

    def Set_email(self,value):
        data = self.rootJsonDataConvert 
        key = "email"  
        data[key] = value

    def Set_need_upload_screenshot(self,value):
        data = self.rootJsonDataConvert 
        key = "need_upload_screenshot"  
        data[key] = value

    def SetKeyVaule(self,key,value):
        data = self.rootJsonDataConvert  
        data[key] = value      
  
    # "privacy_url": "https://6c69-lianlianle-shkb3-1259451541.tcb.qcloud.la/PrivacyPolicy.txt", 
    # "privacy_url2": "https://6d6f-moonma-dbb297-1258816908.tcb.qcloud.la/Moonma/privacyPolicy_kidsgame.txt", 
    # "privacy_url3": "http://www.mooncore.cn/index/privacyPolicy_kidsgame.shtml", 
    # "sku_app": "idiomdict", 
    # "software_url": "http://www.mooncore.cn", 
    # "support_url": "http://blog.sina.com.cn/s/blog_1736372fb0102xb49.html"


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
