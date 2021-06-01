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
from Project.Resource import mainResource 

# from Config import config
from Common import Source
# from Config import adconfig  
from Common.File.FileUtil import FileUtil    

from AppInfo.AppInfo import mainAppInfo

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver

from Common.Platform import Platform

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

from Common.File.FileDownload import mainFileDownload
from Apk.ApkTool import mainApkTool
class SellMyApp():   

    driver: None 
    #构造函数
    def __init__(self): 
        name =""
    
    def Init(self):
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # 全屏
        self.driver.maximize_window()
        # 具体大小
        # driver.set_window_size(width, height)

        # self.GoHome()
        # self.Login()
        # time.sleep(2)
        # GoAppgallery(driver)

        #     # 快照显示已经成功登录
        # print(driver.save_screenshot('jietu.png'))
        # driver.quit()

    def GoApp(self,isHD):   
        url = mainAppInfo.GetSellmyappUrl(isHD)
        self.driver.get(url)
        time.sleep(1) 

        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType() 
        print("gameName="+gameName)
        print ("gameType="+gameType) 

        webcmd = WebDriverCmd(self.driver)
        # div id screenshot-gallery
          # div id screenshot-gallery
        key = "//div[@id='screenshot-gallery']"
        div_screenshot = webcmd.Find(key,True)


        # adhome
        key = "//div[@class='product-banner']"
        div_banner = webcmd.Find(key)
        key = ".//img" 
        img = webcmd.FindChild(div_banner,key)
        pic =img.get_attribute('srcset')  
        filepath = self.GetAdHomeDir(isHD)+"/adhome.png"
        FileUtil.CreateDir2(filepath)
        mainFileDownload.Download(pic,filepath)


        key = ".//ul/li" 
        list = webcmd.FindListChild(div_screenshot,key)
        idx = 0
        for li in list:
            cl =li.get_attribute('class') 
            if cl == "youtube-link":
                pic =li.get_attribute('data-src') 
                url = pic[2:]
                print("video = ",url)
            else:
                pic =li.get_attribute('data-src') 
                print(pic)
                idx =idx+1
                if idx<=5:
                    dirapp = mainResource.GetOutPutScreenshot(isHD)
                    # FileUtil.CreateDir(FileUtil.GetDirOfPath(dirapp))
                    # FileUtil.CreateDir(dirapp)
                    filepath = mainResource.GetOutPutScreenshot(isHD)+"/"+"cn"+"/"+"1080p"+"/"+str(idx)+".jpg"
                    FileUtil.CreateDir2(filepath)
                    mainFileDownload.Download(pic,filepath)
         


        # div user-description
        description = ""
        key = "//div[@class='user-description']"
        list = webcmd.FindList(key)    
        for div in list: 
            description=description+div.text
            
        print(description) 


        # 
        default_xml = mainResource.GetProjectConfigDefault()+"/appinfo/app_description.xml"
        if isHD:
            default_xml = mainResource.GetProjectConfigDefault()+"/appinfo/app_description_hd.xml"

        dst_xml = mainResource.GetProjectConfigApp()+"/appinfo/app_description.xml"
        if isHD:
            dst_xml = mainResource.GetProjectConfigApp()+"/appinfo/app_description_hd.xml"

        strfile = FileUtil.GetFileString(default_xml)
        strfile = strfile.replace("_KEY_EN_",description)
        strfile = strfile.replace("_KEY_CN_",description)
        FileUtil.SaveString2File(strfile,dst_xml)


 
        downloadDir = self.GetSystemDownloadDir()

        self.DeleteAllDownloadFile(downloadDir,".apk")

        try:  
                  
# <span class="store-links" style=""> <a href="https://drive.google.com/file/d/1SW3a2vIT_WXhObGIBEvnuNJ4pEgLiZ2u/view" rel="nofollow" target="_blank" class="google-play-button"></a> </span>    #    
            key = "//span[@class='store-links']/a"
            a = webcmd.Find(key)
            href =a.get_attribute('href') 
            print(href)
            # https://drive.google.com/file/d/1SW3a2vIT_WXhObGIBEvnuNJ4pEgLiZ2u/view

            head = "file/d/"
            end = "/view" 
            # strid = href[href.find(head)+len(head):href.find(end)]
            strid = Common.GetMidString(href,head,end)
            # https://drive.google.com/u/0/uc?id=1SW3a2vIT_WXhObGIBEvnuNJ4pEgLiZ2u&export=download
            url = "https://drive.google.com/u/0/uc?id="+strid+"&export=download"
            print(url)
            self.GoApk(url,isHD)
        except Exception as e: 
            isfilter = True
            print("download apk eror=",e," file =")
 

        apk_download = ""
        # 等待apk下载完成
        while True:
            apk_download = self.GetDownloadFile(downloadDir,".apk")
            time.sleep(1)
            print ("waiting for download apk=") 
            if len(apk_download)>1:
                break
        
        self.DownloadApkFinish(isHD)

# apk

    def GetSystemDownloadDir(self):
        ret = ""
        if Platform.isWindowsSystem():
            ret = "C:\\Users\\moon\\Downloads"

        if Platform.isMacSystem():
            ret = "/Users/moon/Downloads"
        return ret

 
# .apk
    def DeleteAllDownloadFile(self,sourceDir,file_ext):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print sourceFile
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                src_apk_name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext = temp_list[1]
                # apk_ext='.apk';
                if file_ext==ext:
                    print(sourceFile)
                    os.remove(sourceFile)
# .apk
    def GetDownloadFile(self,sourceDir,file_ext):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print sourceFile
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                src_apk_name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext = temp_list[1] 
                if file_ext==ext:
                    print(sourceFile)
                    return sourceFile

        return ""

    def GetDownloadApkPath(self,isHD): 
        dirapk = mainResource.GetProjectOutPutApp() + "/apk" 
        if isHD==True:
            dirapk+="/heng" 
        else:
            dirapk+="/shu"
  
        return dirapk+"/sellmyapp.apk"


    def GetDecodeApkOutputDir(self,isHD): 
        dirapk = mainResource.GetProjectOutPutApp() + "/apk" 
        if isHD==True:
            dirapk+="/heng" 
        else:
            dirapk+="/shu"
  
        return dirapk+"/ApkDecodeOutput"

    def DownloadApkFinish(self,url,isHD):
        downloadDir = self.GetSystemDownloadDir()
        apk_download = self.GetDownloadFile(downloadDir,".apk")
        # copy apk 
        apk_dst = self.GetDownloadApkPath(isHD)
        FileUtil.CreateDir2(apk_dst)
        FileUtil.CopyFile(apk_download,apk_dst)

        
        self.DecodeApk(isHD)
        self.RebuildApk(isHD)


    def GoApk(self,url,isHD): 

        self.driver.get(url)
        time.sleep(1) 
        webcmd = WebDriverCmd(self.driver) 
  
        key = "//a[@id='uc-download-link']"
        webcmd.AddCmdWait(CmdType.CLICK, key)
        webcmd.Run(True)
        # time.sleep(100)
        
    

    def DecodeApk(self,isHD): 
        apk = self.GetDownloadApkPath(isHD)
        output = self.GetDecodeApkOutputDir(isHD)
        mainApkTool.DecodeApK(apk,output)


#   versionCode: '1'
#   versionName: '0.1'
        apktool_yml = output+"/apktool.yml"
        strfile = FileUtil.GetFileString(apktool_yml)
        head = "versionCode: '"
        end = "'"
        vesioncode_decode = Common.GetMidString(strfile,head,end)
        vesioncode_app = mainAppInfo.GetAppVersionCode(Source.ANDROID,isHD,Source.TAPTAP)
        strfile = strfile.replace(head+vesioncode_decode+end,head+vesioncode_app+end)
       
        head = "versionName: '"
        end = "'"
        versionName_decode = Common.GetMidString(strfile,head,end)
        versionName_app = mainAppInfo.GetAppVersion(Source.ANDROID,isHD,Source.TAPTAP)
        strfile = strfile.replace(head+versionName_decode+end,head+versionName_app+end)
        FileUtil.SaveString2File(strfile,apktool_yml)


        # package
        xml = output+"/AndroidManifest.xml"
        head = "package=\""
        end = "\""
        # package="com.unconditionalgames.waterpuzzle"
        package_decode = Common.GetMidString(FileUtil.GetFileString(xml),head,end)
        # mainAppInfo.SetAppPackage(Source.ANDROID,isHD,Source.TAPTAP,package)
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.TAPTAP) 
        strfile = FileUtil.GetFileString(xml)
        strfile = strfile.replace(head+package_decode+end,head+package+end)
        FileUtil.SaveString2File(strfile,xml)


        # BuildConfig.smali
        # public static final APPLICATION_ID:Ljava/lang/String; = "com.moonma.ladderclimb"
        head = "Ljava/lang/String; = \""
        end = "\""
        xml = output+"/smali/222BuildConfig.smali" 
        if os.path.exists(xml):
            # package_decode = Common.GetMidString(FileUtil.GetFileString(xml),head,end)
            strfile = FileUtil.GetFileString(xml)
            strfile = strfile.replace(head+package_decode+end,head+package+end)
            FileUtil.SaveString2File(strfile,xml)


        # name
        head = "\"app_name\">"
        end = "</string>"
        # cn
        name = mainAppInfo.GetAppName(Source.ANDROID,isHD,Source.LANGUAGE_CN,Source.TAPTAP)
        xml = output+"/res/values/strings.xml" 
        if os.path.exists(xml): 
            strfile = FileUtil.GetFileString(xml)
            name_decode = Common.GetMidString(strfile,head,end)
            print("name cn =",name," name_decode="+name_decode)
            strfile = strfile.replace(head+name_decode+end,head+name+end)
            # print("strfile =",strfile)
            FileUtil.SaveString2File(strfile,xml)

        name = mainAppInfo.GetAppName(Source.ANDROID,isHD,Source.LANGUAGE_EN,Source.TAPTAP)
        xml = output+"/res/values-en/strings.xml" 
        if os.path.exists(xml): 
            strfile = FileUtil.GetFileString(xml)
            name_decode = Common.GetMidString(strfile,head,end)
            strfile = strfile.replace(head+name_decode+end,head+name+end)
            FileUtil.SaveString2File(strfile,xml)


        # icon
        icon = output+"/res/mipmap-xxxhdpi/app_icon.png" 
        dst_icon = self.GetAdHomeDir(isHD)+"/app_icon.png"
        FileUtil.CreateDir2(dst_icon)
        FileUtil.CopyFile(icon,dst_icon)

    def GetAdHomeDir(self,isHD):
        ret = mainResource.GetProjectOutPutApp(isHD)+"/adhome"
        FileUtil.CreateDir2(ret)
        return ret

    def RebuildApk(self,isHD):   
        apkdir = self.GetDecodeApkOutputDir(isHD) 
        outputapk = mainResource.GetProjectOutPutApp()+"/outputapk.apk"
        signapk = mainResource.GetOutPutApkPath(Source.TAPTAP, isHD)
        mainApkTool.RebuildApK(apkdir,outputapk,signapk)
        FileUtil.RemoveFile(outputapk)
 
# 主函数的实现
if __name__ == "__main__": 
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)
    arg2 = ""
    arg3 = ""
    arg4 = ""
    for i in range(1,count):
        print("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i] 
        if i==2:
            arg2 = sys.argv[i]
        if i==3:
            arg3 = sys.argv[i]
        if i==4:
            arg4 = sys.argv[i]


    isHD = False
    if arg3 =="hd":
        isHD = True

    mainResource.SetCmdPath(cmdPath)
    
    p = SellMyApp() 
    if "download"==arg2:
    # 
        p.Init()
        p.GoApp(isHD)

    if "rebuild"==arg2:
        p.RebuildApk(isHD)

    if "decode"==arg2:
        p.DecodeApk(isHD)     
 

    print("SellMyApp sucess arg=",arg2)
