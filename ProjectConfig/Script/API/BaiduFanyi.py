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
import requests  
#include common.py
#  
o_path = os.getcwd()  # 返回当前工作目录
print(o_path)
# sys.path.append(o_path)  # 添加自己指定的搜索路径
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
# sys.path.append('./')  

dir = os.path.abspath(__file__)
print(dir)
dir = os.path.dirname(dir)
print(dir) 
# sys.path.append("..") #把上级目录加入到变量中
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  


from Common.Common import Common 
# from Config import config
from Common import Source
# from Config import adconfig  
from Common.File.FileUtil import FileUtil    
 

from Common.Platform import Platform
 
#  https://api.fanyi.baidu.com/product/113

# http://api.fanyi.baidu.com/api/trans/vip/translate?q=apple&from=en&to=zh&appid=2015063000000001&salt=1435660288&sign=f89f9594663708c1605f3d736d01d2d4


import http.client
import hashlib
import urllib
import random
import json
 
class BaiduFanyi():   

    driver: None 
    filepathSmail=""

    #构造函数
    def __init__(self): 
        name =""
     
    def GetUrl(self, url): 
        r = requests.get(url)
        return r.content.decode('utf-8',"ignore")

    def RunFanyiEnToCN(self,text):  
        fromLang = 'en'   #原文语种
        toLang = 'zh'   #译文语种
        return self.Fanyi(text,fromLang,toLang)

    def RunFanyiCnToEn(self,text):  
        fromLang = 'zh'   #原文语种
        toLang = 'en'   #译文语种
        return self.Fanyi(text,fromLang,toLang)

    def Fanyi(self,text,fromLang,toLang):  
        # text = "apple"
        # url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="+text+"&from=en&to=zh&appid=2015063000000001&salt=1435660288&sign=f89f9594663708c1605f3d736d01d2d4"  
        # print(url)
        # str = self.GetUrl(url)
        # print(str)
        # rootJson = json.loads(str)
        # return rootJson["trans_result"][0]["dst"]
        # # {"from":"en","to":"zh","trans_result":[{"src":"apple","dst":"\u82f9\u679c"}]}
 

        appid = '20210603000852273'  # 填写你的appid
        secretKey = 'ciTOLU1ECG4VXxKQtEsJ'  # 填写你的密钥

        httpClient = None
        myurl = '/api/trans/vip/translate'

  
        salt = random.randint(32768, 65536)
        # q= 'apple'
        q = text
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            print('翻译：：')
            # print (result)
            list = result["trans_result"]
            ret = ""
            for item in list:
                ret = ret +item["dst"]+"\n"

            return ret

        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()

        return ""

mainBaiduFanyi = BaiduFanyi()
 