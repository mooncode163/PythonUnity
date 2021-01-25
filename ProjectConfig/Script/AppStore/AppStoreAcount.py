# 导入selenium的浏览器驱动接口


import datetime
from Common.File.FileUtil import FileUtil 
# pip3 install connectcli
# from connectapi import ConnectApi

import gzip
import requests
import platform 
if 'Darwin' not in platform.system():
    import jwt
from Project.Resource import mainResource 
import time
import sqlite3 
import sys
import os
import json 
import base64 

from Common.File.FileUtil import FileUtil 

o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径

 
 
class AppStoreAcount:
    fileJosn = "AppStoreAcount.json" 
    dataRoot:None

    def __init__(self):
        self.LoadJson()

    def GetPassword(self,appstore,name): 
        password = ""
        for item in self.dataRoot[appstore]:
            if name == item["name"]:
                password = item["password"]
        return password

    def GetPrivacy(self,appstore,name): 
        password = ""
        for item in self.dataRoot[appstore]:
            if name == item["name"]:
                password = item["privacy"]
        return password

        

    def GetClientId(self,appstore,name): 
        password = ""
        for item in self.dataRoot[appstore]:
            if name == item["name"]:
                password = item["ClientId"]
        return password

    def GetClientSecret(self,appstore,name): 
        password = ""
        for item in self.dataRoot[appstore]:
            if name == item["name"]:
                password = item["ClientSecret"]
        return password

    def GetiOSAPI_KEY_ID(self,name): 
        ret = ""
        for item in self.dataRoot["appstore"]:
            if name == item["name"]:
                ret = item["API_KEY_ID"]
        return ret
    def GetiOSAPI_USER_ID(self,name): 
        ret = ""
        for item in self.dataRoot["appstore"]:
            if name == item["name"]:
                ret = item["API_USER_ID"]
        return ret
    def GetiOSteamID(self,name): 
        ret = ""
        for item in self.dataRoot["appstore"]:
            if name == item["name"]:
                ret = item["teamID"]
        return ret
    def GetiOSCertificateID(self,name): 
        ret = ""
        for item in self.dataRoot["appstore"]:
            if name == item["name"]:
                ret = item["CertificateID"]
        return ret


    def LoadJson(self): 
        strjson = FileUtil.GetFileString(self.fileJosn)
        self.dataRoot = json.loads(strjson) 


mainAppStoreAcount = AppStoreAcount()
