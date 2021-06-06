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
  

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 


# https://www.jianshu.com/p/e18cdb1053d0
# pip3 install pytube
# pytube http://youtu.be/rJ18V_NNq8g

from pytube import YouTube

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
# urllib.error.URLError: <urlopen error [Errno 61] Connection refused>

# Youtube视频下载网站  https://zh.savefrom.net/7/
class YoutubeDownload():   
    driver: None 
    URL_HEAD = "http://47.242.56.146"
    URL_PORT = "5000"
    

    #构造函数
    def __init__(self): 
        name ="" 
        self.Init()
 
    def Init(self):
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # 全屏
        self.driver.maximize_window()
        # 具体大小
        # driver.set_window_size(width, height)
 
        #     # 快照显示已经成功登录
        # print(driver.save_screenshot('jietu.png'))
        # driver.quit()

    # pytube http://youtu.be/rJ18V_NNq8g --itag=22

    #  http://youtu.be/rJ18V_NNq8g
    def Download(self, url,savefilepath): 
        print("YoutubeDownload Download url=",url)
        # url = "http://youtu.be/rJ18V_NNq8g"
        # YouTube(url).streams.first().download()
        # self.DownloadByBrowser(url)
        self.DownloadServer(url,savefilepath)


    def DownloadServer(self, url,savefilepath):
        # http://47.242.56.146:5000/YoutubDownload?keyid=rJ18V_NNq8g
        idx = url.rfind("/")
        idx=idx+1 
        keyid = url[idx:] 
        url_server = self.URL_HEAD+":"+self.URL_PORT+"/YoutubDownload?keyid="+keyid
        print("YoutubeDownload url_server=",url_server)
        name = self.GetUrl(url_server) 
        url_video = self.URL_HEAD+"/"+name
        print("YoutubeDownload url_video=",url_video)

        r = requests.get(url_video)
        with open(savefilepath, "wb") as code:
            code.write(r.content)



    def GetUrl(self, url): 
        r = requests.get(url)
        return r.content.decode('utf-8',"ignore")

# Youtube视频下载网站  https://zh.savefrom.net/7/
    def DownloadByBrowser(self, url,savefilepath):
        # 加载百度页面 
        self.driver.get("https://zh.savefrom.net/7/")
        time.sleep(1)
        webcmd = WebDriverCmd(self.driver)

        key = "//input[@id='sf_url']"
        webcmd.AddCmdWait(CmdType.INPUT,key,url)
        # <input type="text" name="sf_url" value="" autofocus="" placeholder="在这里粘贴视频链接" onfocus="if(this.value &amp;&amp; this.select){this.select()}" id="sf_url">
        # <button type="submit" name="sf_submit" class="submit" id="sf_submit">下载</button>
        key = "//button[@id='sf_submit']"
        webcmd.AddCmd(CmdType.CLICK,key)
        webcmd.Run(True)


mainYoutubeDownload = YoutubeDownload()
 