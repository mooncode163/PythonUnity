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

# o_path = os.getcwd()  # 返回当前工作目录
# sys.path.append(o_path)  # 添加自己指定的搜索路径
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
 
from Common import Source 
from Common.Common import Common
from Project.Resource import mainResource
# from Config import config
from Common import Source
# from Config import adconfig  
from Common.File.FileUtil import FileUtil 

class AdConfig():
    jsonRoot:None
    jsonPlat:None
    def GetConfigFile(self,osSrc, isHd):
        dir = mainResource.GetAdConfigDir()
        if isHd:
            filepath = dir + "/ad_config_" + osSrc + "_hd"+".json"
        else:
            filepath = dir + "/ad_config_" + osSrc+".json"
        return filepath

    def GetCommonConfigFile(self,osSrc, isHd):
        dir = mainResource.GetCommonAdConfigDir() 
        filepath = dir + "/ad_config_common_" + osSrc+".json"
        return filepath

    def LoadJson(self,osSrc, isHd): 
        jsonfile = self.GetConfigFile(osSrc, isHd)
        with open(jsonfile, 'rb') as json_file:
            self.jsonRoot = json.load(json_file)
            self.jsonPlat = self.jsonRoot["platform"]


    def LoadJsonFile(self,jsonfile): 
        with open(jsonfile, 'rb') as json_file:
            self.jsonRoot = json.load(json_file)
            self.jsonPlat = self.jsonRoot["platform"]


    def GetCommonAppId(self,src, osSrc, isHd):
        jsonfile = self.GetCommonConfigFile(osSrc, isHd)
        self.LoadJsonFile(jsonfile)
        appid = "0"
        for jsontmp in self.jsonPlat:
            if jsontmp["source"] == src:
                appid = jsontmp["appid"]
        return appid

    def GetAppId(self,src, osSrc, isHd):
        self.LoadJson(osSrc, isHd)
        appid = "0"
        for jsontmp in self.jsonPlat:
            if jsontmp["source"] == src:
                appid = jsontmp["appid"]
        return appid

    def GetAppKey(self,src, osSrc, isHd):
        self.LoadJson(osSrc, isHd)
        appkey = "0"
        for jsontmp in self.jsonPlat:
            if jsontmp["source"] == src:
                appkey = jsontmp["appkey"]
        return appkey

mainAdConfig = AdConfig()
