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
from Project.Resource import mainResource
 
class Config():  
    jsonRoot:None
    jsonPlat:None
    jsonShare:None
    jsonCommonRoot:None


    #构造函数
    def __init__(self): 
        dir = mainResource.GetRootProjectUnity()+"/Assets/Resources/ConfigData/config"
        # self.LoadCommonJson(dir)


    def GetConfigCommonFile(self,dir): 
        filepath = dir + "/config_common.json"
        return filepath 


    def GetConfigFile(self,osSrc, isHd):
        dir = mainResource.GetConfigDir()
        if isHd:
            filepath = dir + "/config_" + osSrc + "_hd" + ".json"
        else:
            filepath = dir + "/config_" + osSrc + ".json"
        return filepath


    def LoadCommonJson(self,dir): 
        jsonfile = self.GetConfigCommonFile(dir)
        with open(jsonfile) as json_file:
            self.jsonCommonRoot = json.load(json_file) 


    def LoadJson(self,osSrc, isHd): 
        jsonfile = self.GetConfigFile(osSrc, isHd)
        with open(jsonfile) as json_file:
            self.jsonRoot = json.load(json_file)
            self.jsonShare = self.jsonRoot["SHARE"] 
            self.jsonPlat = self.jsonShare["platform"]

    def GetConfigAppType(self,dir):
        self.LoadCommonJson(dir) 
        return self.jsonCommonRoot["APP_TYPE"]
    def GetConfigAppName(self,dir):
        self.LoadCommonJson(dir) 
        return self.jsonCommonRoot["APP_NAME_KEYWORD"]

    def IsForKid(self): 
        dir = mainResource.GetRootProjectUnity()+"/Assets/Resources/ConfigData/config"
        self.LoadCommonJson(dir)
        return self.jsonCommonRoot["APP_FOR_KIDS"]

    def GetShareAppId(self,src, osSrc, isHd):
        self.LoadJson(osSrc, isHd)
        appid = "0"
        for jsontmp in self.jsonPlat:
            if jsontmp["source"] == src:
                appid = jsontmp["id"]
        return appid


    def GetShareAppKey(self,src, osSrc, isHd):
        self.LoadJson(osSrc, isHd)
        appkey = "0"
        for jsontmp in self.jsonPlat:
            if jsontmp["source"] == src:
                appkey = jsontmp["key"]
        return appkey



    # qq: appID：100424468 1、tencent100424468 
    # 2、QQ05fc5b14	QQ05fc5b14为100424468转十六进制而来，因不足8位向前补0，然后加"QQ"前缀
    def QQEncodeAppID(self,appid):
        ret ="QQ" 
        str_hex = hex(int(appid))
        len_hex = len(str_hex)

        # 去除 0x 前缀
        str_hex = str_hex[2:len_hex]

        len_hex = len(str_hex)
        if len_hex<8:
            for i in range(0,8-len_hex):
                ret+="0" 
        
        ret+=str_hex
        return ret
    # CFBundleURLSchemes
    def XcodeUrlScheme(self,src, appid, idx):
        ret = appid
        if src == Source.WEIBO:
            ret = "wb" + appid
        if src == Source.WEIXIN or src == Source.WEIXINFRIEND:
            ret = appid
        if src == Source.QQ or src == Source.QQZONE:
            if idx ==0:
                ret = self.QQEncodeAppID(appid)
            if idx ==1:
                ret = "tencent"+appid


        if ret=="0" or len(ret)==0:
            # xcode UrlScheme 首字母不能为数字
            ret = "wx0"

        return ret 
    
mainConfig = Config()