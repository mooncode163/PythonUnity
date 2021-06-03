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
  
# https://www.jianshu.com/p/e18cdb1053d0
# pip3 install pytube

from pytube import YouTube


# Youtube视频下载网站  https://zh.savefrom.net/7/
class YoutubeDownload():   

    
    #构造函数
    def __init__(self): 
        name =""
     
    # pytube http://youtu.be/rJ18V_NNq8g --itag=22

    #  http://youtu.be/rJ18V_NNq8g
    def Download(self, url): 
        print("YoutubeDownload Download url=",url)
        url = "http://youtu.be/rJ18V_NNq8g"
        # YouTube(url).streams.first().download()

 

mainYoutubeDownload = YoutubeDownload()
 