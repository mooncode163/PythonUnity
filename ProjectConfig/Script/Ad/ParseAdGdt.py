import os
import shutil
import zipfile
import sys 

sys.path.append('../../') 
sys.path.append('./') 
from Project.Resource import mainResource
from Config.Config import mainConfig
from Config.AdConfig import mainAdConfig  
from Common import Source
from Common.Common import Common
from Project.Resource import mainResource 
from Common import Source
from Common.File.FileUtil import FileUtil 

import pyperclip
from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

import json

from bs4 import BeautifulSoup

from urllib.request import urlopen
import json

import ssl
# 跳过ssl证书
ssl._create_default_https_context = ssl._create_unverified_context





class ParseAdGdt():
    title = ""
    author = ""
    listSort = []
    strAdIdSplash = None
    strAdIdInsert = None
    strAdIdBanner = None
    strAdIdVideo = None
    strAdIdNative = None
    strAppId = None
    strAppName = None

    def LoadJson(self, filepath):
        data = None
        with open(filepath) as json_file:
            data = json.load(json_file)
            return data

    def GetHtml(self, url):
        # return  urlopen(url).read().decode('utf-8')
        return open(url, 'r', encoding='utf-8')

    def GetAdId(self, tr, key):
        adid = None
        array_div = tr.find_all("div", class_="inner")
        for div in array_div:
            if div.get_text() == key:
                span = tr.find("span", class_="field-value")
                adid = span.get_text()

        return adid

    # def ParseAd(self,url,json):
    #     html = self.GetHtml(url)
    #     self.ParseAdData(html,json)

    def ParseAdData(self, data,ishd,osApp):
        # url = WEB_HOME_URL
        html = data
    # 本质上是一个tag类型,生成一个tag实例对象，调用tag的方法
        soup = BeautifulSoup(html, "lxml")
        ad_table = soup.find(
            "table", class_="table media-table js-media-details")
        if ad_table is None:
            return

        div = soup.find("div", class_="media media-info-general")
        h4 = div.find("span", class_="text")
        self.strAppName = h4.get_text()
        print(self.strAppName)

        span = div.find("span", class_="field-value")
        self.strAppId = span.get_text()
        print(self.strAppId)

        array_tr = ad_table.find_all('tr')
        for tr in array_tr:
            # 横幅
            if self.strAdIdBanner is None:
                self.strAdIdBanner = self.GetAdId(tr, "Banner2.0")

            # 插屏
            if self.strAdIdInsert is None:
                self.strAdIdInsert = self.GetAdId(tr, "插屏2.0")

            # 激励视频
            if self.strAdIdVideo is None:
                self.strAdIdVideo = self.GetAdId(tr, "激励视频")
            # 原生
            if self.strAdIdNative is None:
                self.strAdIdNative = self.GetAdId(tr, "原生")

            # 开屏
            if self.strAdIdSplash is None:
                self.strAdIdSplash = self.GetAdId(tr, "开屏")

        if self.strAdIdNative is None:
            self.strAdIdNative = "0"

        if self.strAdIdSplash is None:
            self.strAdIdSplash = "0"

        if self.strAdIdVideo is None:
            self.strAdIdVideo = "0"

        if self.strAdIdBanner is None:
            self.strAdIdBanner = "0"

        if self.strAdIdInsert is None:
            self.strAdIdInsert = "0"

        print("Banner:", self.strAdIdBanner)
        print("插屏:", self.strAdIdInsert)
        print("激励视频:", self.strAdIdVideo)
        print("原生:", self.strAdIdNative)
        print("开屏:", self.strAdIdSplash)

        # dictad = dict (source="gdt",appname= self.strAppName,appid= self.strAppId,key_splash= self.strAdIdSplash,key_splash_insert= self.strAdIdInsert,key_insert= self.strAdIdInsert,key_native= self.strAdIdNative,key_video= self.strAdIdVideo,key_banner= self.strAdIdBanner)
        # jsonroot = dict (List=dictad)
        # self.SaveJson(json,jsonroot)
        self.SaveAdIdToJson(osApp,ishd)

    # def SaveJson(self,filePath,dataRoot):
    #     # 保存json
    #     with open(filePath, 'w') as f:
    #         json.dump(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = False)

    def SaveAdIdToJson(self, os,  ishd):
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
            for ad in platform: 
                if ad["source"] == "gdt":
                    ad["appname"] = self.strAppName
                    ad["appid"] = self.strAppId
                    ad["key_splash"] = self.strAdIdSplash
                    ad["key_splash_insert"] = self.strAdIdInsert
                    ad["key_insert"] = self.strAdIdInsert
                    ad["key_native"] = self.strAdIdNative
                    ad["key_banner"] = self.strAdIdBanner 
                    ad["key_video"] = self.strAdIdVideo 
                    break 

            self.SaveJson(filepath,data)
    
    
    def SaveJson(self,filePath,dataRoot):   
        # 保存json 
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True).encode('utf8',"ignore")
        json_str = json.dumps(dataRoot,ensure_ascii=False,indent=4,sort_keys = True)
        FileUtil.SaveString2File(json_str,filePath)
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True)
            

 
# parse = ParseAdGdt()
# parse.ParseAd("gdt.htm","gdt.json")
# parse.ParseAd("gdt_hd.htm","gdt_hd.json")



     

