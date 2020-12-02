# 导入selenium的浏览器驱动接口 
  
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import sys
import os
import json
sys.path.append('../../') 
sys.path.append('./') 
from Project.Resource import mainResource
from Common import Source
from Common.Common import Common
from Project.Resource import mainResource 
from Common import Source
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo

import pyperclip
from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo  
 

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AdBase():
    driver: None 
    adIdBanner="0"
    adIdInsert="0"
    adIdVideo="0"
    adIdNative="0"
    appName="0"
    appId="0"
    appKey="0"
    adIdSplash="0"

    def SetJosnValue(self, item,adSource):
        item["appname"] = self.appName
        item["appid"] = self.appId
        item["key_splash"] = self.adIdSplash
        item["key_splash_insert"] = self.adIdInsert
        item["key_insert"] = self.adIdInsert
        item["key_native"] = self.adIdNative
        item["key_banner"] = self.adIdBanner 
        item["key_video"] = self.adIdVideo
        item["source"] = adSource 

    def SaveAdIdToJson(self, os, ishd,adSource):
        dirconfig = mainResource.GetAdConfigDir()
        filepath = ""
        if os == Source.ANDROID:
            filepath = dirconfig+"/ad_config_android.json"
            if ishd:
                filepath = dirconfig+"/ad_config_android_hd.json"

        if os == Source.IOS:
            filepath = dirconfig+"/ad_config_ios.json"
            if ishd:
                filepath = dirconfig+"/ad_config_ios_hd.json"

        with open(filepath, 'rb') as json_file:
            data = json.load(json_file) 
            platform = data["platform"]
            isInJson = False
            for ad in platform: 
                if ad["source"] == adSource: 
                    isInJson = True
                    break 

            if isInJson:
                for ad in platform: 
                    if ad["source"] == adSource:
                        self.SetJosnValue(ad,adSource)
                        break 
            else:
                print("not in json")
                jsonitem = json.loads("{}")
                self.SetJosnValue(jsonitem,adSource)
                platform.append(jsonitem)
                

            self.SaveJson(filepath,data)
    
    
    def SaveJson(self,filePath,dataRoot):   
        # 保存json 
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True).encode('utf8',"ignore")
        json_str = json.dumps(dataRoot,ensure_ascii=False,indent=4,sort_keys = True)
        FileUtil.SaveString2File(json_str,filePath)
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True)

    

 



         