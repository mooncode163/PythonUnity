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
from Common.File.AndroidManifest import mainAndroidManifest    


from AppInfo.AppInfo import mainAppInfo
from Config.AdConfig import mainAdConfig  

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

from API.BaiduFanyi import mainBaiduFanyi
from API.YoutubeDownload import mainYoutubeDownload

from Common.File.ZipUtil import ZipUtil 

class GooglePlay():   

    driver: None 
    filepathSmail=""

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

    def GetPackageOfGooglePlayUrl(self,url):  
        # https://play.google.com/store/apps/details?id=com.azurgames.stackball
        head = "id="
        idx = url.find(head)+len(head) 
        return url[idx:]


    def GoApp(self,isHD):   
        url = mainAppInfo.GetGooglePlayUrl(isHD)
        package_play = self.GetPackageOfGooglePlayUrl(url)
        print("package_play="+package_play)
        self.driver.get(url)
        time.sleep(1) 

        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType() 
        print("gameName="+gameName)
        print ("gameType="+gameType) 

        webcmd = WebDriverCmd(self.driver)

        # <button class="Q4vdJd" aria-label="Open screenshot 0" jscontroller="DeWHJf" jsaction="click:O1htCb" jsname="WR0adb" data-screenshot-item-index="0">
 
        key = "//button[@aria-label='Open screenshot 0' and @data-screenshot-item-index='0']" 
        webcmd.AddCmdWait(CmdType.CLICK, key)
        webcmd.Run(True)


        # <div class="OeSxze " jsname="ibnC6b" data-expanded-slideshow-item-index="0"> 
        count = 5
        for i in range(0,count):
            key = "//div[@jsname='ibnC6b' and @data-expanded-slideshow-item-index='"+str(i)+"']" 
            div = webcmd.Find(key)
            key = ".//img[@itemprop='image']"
            img = webcmd.FindChild(div,key) 
            pic =img.get_attribute('src')  

            idx = i+1
            dirapp = mainResource.GetOutPutScreenshot(isHD)
            # FileUtil.CreateDir(FileUtil.GetDirOfPath(dirapp))
            # FileUtil.CreateDir(dirapp)
            filepath = mainResource.GetOutPutScreenshot(isHD)+"/"+"cn"+"/"+"1080p"+"/"+str(idx)+".webp"
            FileUtil.CreateDir2(filepath)
            mainFileDownload.Download(pic,filepath)


            w = 1080
            h = 1920  
            self.ConverImage(filepath,filepath,w,h)

            # copy jpg
            filepath_jpg = filepath.replace(".webp",".jpg")
            FileUtil.CopyFile(filepath,filepath_jpg)

            
            # copy
            # filepath_en = mainResource.GetOutPutScreenshot(isHD)+"/"+"en"+"/"+"1080p"+"/"+str(idx)+".jpg"
            # FileUtil.CreateDir2(filepath_en)
            # FileUtil.CopyFile(filepath,filepath_en)


        # key = ".//ul/li" 
        # list = webcmd.FindListChild(div_screenshot,key)
        # idx = 0
        # for li in list:
        #     cl =li.get_attribute('class') 
        #     if cl == "youtube-link":
        #         pic =li.get_attribute('data-src') 
        #         url = pic[2:]
        #         print("video = ",url) 
        #         # self.DeleteAllDownloadFile(downloadDir,".mp4")
                

        #         video_dst = self.GetAdHomeDir(isHD)+"/video.mp4"
        #         mainYoutubeDownload.Download(url,video_dst)
 
     


        # div user-description
        # <div jsname="bN97Pc" class="DWPxHb" itemprop="description"
        description = ""
        key = "//div[@jsname='bN97Pc' and @class='DWPxHb' and @itemprop='description']"
        div = webcmd.Find(key)     

        # <div jsname="sngebd">
        description=description+div.text
            
        print("description=",description) 


        # 
        default_xml = mainResource.GetProjectConfigDefault()+"/appinfo/app_description.xml"
        if isHD:
            default_xml = mainResource.GetProjectConfigDefault()+"/appinfo/app_description_hd.xml"

        dst_xml = mainResource.GetProjectConfigApp()+"/appinfo/app_description.xml"
        if isHD:
            dst_xml = mainResource.GetProjectConfigApp()+"/appinfo/app_description_hd.xml"

        strfile = FileUtil.GetFileString(default_xml)
        strfile = strfile.replace("_KEY_CN_",description)

        description_en = mainBaiduFanyi.RunFanyiCnToEn(description)
        strfile = strfile.replace("_KEY_EN_",description_en)
        FileUtil.SaveString2File(strfile,dst_xml)


 
        downloadDir = self.GetSystemDownloadDir()

        self.DeleteAllDownloadFile(downloadDir,".apk")

        self.DeleteAllDownloadFile(downloadDir,".xapk")

        # 自动下载
        # https://apkpure.com/cn/com.azurgames.stackball/download?from=details
        # https://apkpure.com/cn/stack-ball-android/com.azurgames.stackball/download?from=details
        # url_apk = "https://apkpure.com/cn/"+package_play+"/download?from=details"
        # 手动选择版本下载
        # https://apkpure.com/cn/stack-ball-android/com.azurgames.stackball

        url_apk = "https://apkpure.com/cn/"+package_play
        self.driver.get(url_apk)
        time.sleep(1) 


        # apk_download = ""
        # # 等待xapk下载完成
        # while True:
        #     apk_download = self.GetDownloadFile(downloadDir,".xapk")
        #     time.sleep(1)
        #     print ("waiting for download xapk=") 
        #     if len(apk_download)>1:
        #         break
        
        # file_zip = apk_download
        # # file_zip = apk_download.replace(".xapk",".zip")
        # os.rename(apk_download, file_zip) 
        # ZipUtil.un_zip(file_zip,downloadDir)
                
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
        dirapk = mainResource.GetApkDecodeOutputApp() 
        if isHD==True:
            dirapk+="/heng" 
        else:
            dirapk+="/shu"
  
        return dirapk+"/ApkDecodeOutput"

 
    def ResizeImage(self):
        filesrc = self.GetAdHomeDir(isHD)+"/adhome.png"

        w = 1920
        h = 1080
        filedst = self.GetAdHomeDir(isHD)+"/adhome_"+str(w)+"_"+str(h)+".png"
        self.ConverImage(filesrc,filedst,w,h)

        w = 1024
        h = 500
        filedst = self.GetAdHomeDir(isHD)+"/adhome_"+str(w)+"_"+str(h)+".png"
        self.ConverImage(filesrc,filedst,w,h)

        w = 1080
        h = 480
        filedst = self.GetAdHomeDir(isHD)+"/adhome_"+str(w)+"_"+str(h)+".png"
        self.ConverImage(filesrc,filedst,w,h)

        w = 1256
        h = 706
        filedst = self.GetAdHomeDir(isHD)+"/video_taptap"+".png"
        self.ConverImage(filesrc,filedst,w,h)

        # icon     
        output = self.GetDecodeApkOutputDir(isHD)
        filesrc = output+"/res/mipmap-xxxhdpi/app_icon.png"  
        if not os.path.exists(filesrc):
            filesrc = output+"/res/mipmap-xxhdpi/app_icon.png"  
        if not os.path.exists(filesrc):
            filesrc = output+"/res/mipmap-xhdpi/app_icon.png"  

        w = 512
        h = 512 
        filedst = self.GetAdHomeDir(isHD)+"/icon_512.png"
        self.ConverImage(filesrc,filedst,w,h)

        w = 1024
        h = 1024 
        filedst = self.GetResourceDataIcon(isHD)+"/icon.jpg"
        self.ConverImage(filesrc,filedst,w,h)

        # huawei
        w = 216
        h = 216 
        diricon = "icon"
        if isHD:
            diricon = "iconhd"
        filedst = mainResource.GetProjectOutPutApp()+"/"+diricon+"/huawei/icon_android_216.png"
        FileUtil.CreateDir2(filedst)
        self.ConverImage(filesrc,filedst,w,h)

        FileUtil.RemoveFile(filesrc)
        



    def ConverImage(self,filesrc,filedst,width,height):
        godir = mainResource.GetDirGoRoot()+ "/Image" 
        os.chdir(godir)
        filego = "ImageConvert.go" 
        cmd = "go run "+filego+" "+filesrc+" "+filedst+" "+str(width)+" "+str(height)
        print(cmd)
        os.system(cmd)

    def DownloadApkFinish(self,isHD):
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
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.TAPTAP)
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
        strfile = FileUtil.GetFileString(xml)
        # AndroidManifest
        mainAndroidManifest.Load(xml)
        mainAndroidManifest.ConfigGooglePlay(package)
        # xml = output+"/AndroidManifest2.xml"
        mainAndroidManifest.SaveXml(xml)

        # </application>
        xmlAdGdt = mainResource.GetDirRootSmali()+"/AdGdt.xml"
        key = "</application>"
        # idx = strfile.find(key)
        # strhead = strfile[0:idx]
        # strend = strfile[idx:]
        # strfile=strhead+FileUtil.GetFileString(xmlAdGdt)+strend
        strfile = strfile.replace(key,FileUtil.GetFileString(xmlAdGdt))

        # <application
        key = "<application"
        strfile = strfile.replace(key,"<application android:usesCleartextTraffic=\"true\" ")
        

        # <activity android:name=".AdSplashActivity"  android:theme="@style/UnityThemeSelector">
        #     <intent-filter>
        #         <action android:name="android.intent.action.MAIN"/>
        #         <category android:name="android.intent.category.LAUNCHER"/>
        #     </intent-filter>
        # </activity>



        # 去除原来的main activity
            #  <intent-filter>
            #     <action android:name="android.intent.action.MAIN"/>
            #     <category android:name="android.intent.category.LAUNCHER"/>
            # </intent-filter>

        key = "android.intent.action.MAIN"
        idxmid = strfile.find(key)
        strhead = strfile[0:idxmid]
        key = "<intent-filter>" 
        idx = strhead.rfind(key)
        strhead = strhead[0:idx]


        strend = strfile[idxmid:]
        key = "</intent-filter>" 
        idxend = idxmid+strend.find(key)+len(key)
        strend =  strfile[idxend:]

        strfile = strhead+" "+strend


        # 插入main activity
        key = "<application"
        idx = strfile.find(key)
        strhead = strfile[idx:]
        key = ">"
        idx = idx+strhead.find(key)+len(key)
        strhead = strfile[0:idx]
        strend = strfile[idx:]
        xmlMain = mainResource.GetDirRootSmali()+"/MainActivity.xml"
        strfile=strhead+"\n"+FileUtil.GetFileString(xmlMain)+strend


        head = "package=\""
        end = "\""
        # package="com.unconditionalgames.waterpuzzle"
        package_decode = Common.GetMidString(FileUtil.GetFileString(xml),head,end)
        # mainAppInfo.SetAppPackage(Source.ANDROID,isHD,Source.TAPTAP,package)
          
        strfile = strfile.replace(package_decode,package)
        strfile = strfile.replace("com.moonma.test",package)
        
        FileUtil.SaveString2File(strfile,xml)





        # BuildConfig.smali
        # public static final APPLICATION_ID:Ljava/lang/String; = "com.moonma.ladderclimb"
        head = "Ljava/lang/String; = \""
        end = "\""
        # xml = output+"/smali/222BuildConfig.smali" 
        xml = self.GetBuildConfig_smali(isHD,package_decode)
        print("xml BuildConfig.smali =",xml)
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
 
        self.ResizeImage()

        self.AddCode(isHD,package_decode)



    def GetBuildConfig_smali(self,isHD,package):
        output = self.GetDecodeApkOutputDir(isHD)+"/smali"  
        outFilepath = ""
        self.ScansmaliFiles(output,package,outFilepath)
        return self.filepathSmail

    def ScansmaliFiles(self,sourceDir,package,outFilepath):
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
                src_apk_extension = temp_list[1] 
                if 'BuildConfig.smali'==file:
                    head = "Ljava/lang/String; = \""
                    end = "\""
            
                    strfile = FileUtil.GetFileString(sourceFile) 
                    key = head+package+end
                    if strfile.find(key)>=0:
                        print(sourceFile)
                        outFilepath = sourceFile
                        self.filepathSmail = sourceFile
                        return
                        

            #目录嵌套
            if os.path.isdir(sourceFile):
                # print sourceFile
                self.ScansmaliFiles(sourceFile,package,outFilepath)

    def GetAdHomeDir(self,isHD):
        ret = mainResource.GetResourceDataApp()+"/adhome_GooglePlay"
        FileUtil.CreateDir2(ret)
        return ret

    def GetResourceDataIcon(self,isHD):
        ret = mainResource.GetResourceDataApp()+"/icon"
        if isHD:
           ret = mainResource.GetResourceDataApp()+"/iconhd" 
        FileUtil.CreateDir2(ret)
        return ret

    def RebuildApk(self,isHD):   
        apkdir = self.GetDecodeApkOutputDir(isHD) 
        outputapk = mainResource.GetProjectOutPutApp()+"/outputapk.apk"
        signapk = mainResource.GetOutPutApkPath(Source.TAPTAP, isHD)
        mainApkTool.RebuildApK(apkdir,outputapk,signapk)
        FileUtil.RemoveFile(outputapk)

        self.InstallApk(isHD)
 

    def InstallApk(self,isHD):    
        apk = mainResource.GetOutPutApkPath(Source.TAPTAP, isHD) 
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.TAPTAP)  
        try:   
            os.system("adb uninstall "+package)
            os.system("adb install "+apk) 
        except Exception as e:  
            print("InstallApk eror=",e)

    # smail 逆向添加广告和统计等代码
    def AddCode(self,isHD,package_decode):  
        print("AddCode package_decode=",package_decode)
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.TAPTAP) 
        code = ""
        # assets
        src = mainResource.GetDirRootSmali()+"/assets/gdt_plugin"
        dst = self.GetDecodeApkOutputDir(isHD)+"/assets/gdt_plugin"
        FileUtil.CopyDir(src,dst,True)
        #lib
        cpulist  = ["armeabi-v7a","arm64-v8a","armeabi","x86"]
        for dirtmp in cpulist:
            src = mainResource.GetDirRootSmali()+"/lib/"+dirtmp
            dst = self.GetDecodeApkOutputDir(isHD)+"/lib/"+dirtmp
            if os.path.exists(dst):
                FileUtil.CoverFiles(src,dst)
        #res
        src = mainResource.GetDirRootSmali()+"/res/xml"
        dst = self.GetDecodeApkOutputDir(isHD)+"/res/xml" 
        FileUtil.CreateDir(dst)
        FileUtil.CoverFiles(src,dst)

        #smali
        src = mainResource.GetDirRootSmali()+"/smali/com"
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/com"
        listdir = []
        FileUtil.GetSubDirList(src,listdir)
        for dirtmp in listdir:  
            FileUtil.CopyDir(dirtmp,dst+"/"+dirtmp.replace(src,""),True)
 
        src = mainResource.GetDirRootSmali()+"/smali/gnu"
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/gnu"
        listdir = []
        FileUtil.GetSubDirList(src,listdir)
        for dirtmp in listdir:  
            FileUtil.CopyDir(dirtmp,dst+"/"+dirtmp.replace(src,""),True)

 
        src = mainResource.GetDirRootSmali()+"/smali/org"
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/org"
        listdir = []
        FileUtil.GetSubDirList(src,listdir)
        for dirtmp in listdir:  
            FileUtil.CopyDir(dirtmp,dst+"/"+dirtmp.replace(src,""),True)


        src = mainResource.GetDirRootSmali()+"/smali/androidx"
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/androidx"
        listdir = []
        FileUtil.GetSubDirList(src,listdir)
        for dirtmp in listdir:  
            FileUtil.CopyDir(dirtmp,dst+"/"+dirtmp.replace(src,""),True)


        # AdSplashActivity.smali AdSplashActivity$1.smali UmengActivity.smali
        liststr = package_decode.split(".")
        idx = 0
        strdir = ""
        for dirtmp in liststr: 
            strdir=strdir+dirtmp+"/"
            idx=idx+1
        
        src = mainResource.GetDirRootSmali()+"/smali/moonma/AdSplashActivity.smali"
        strfile = FileUtil.GetFileString(src) 
        strfile = strfile.replace("com/moonma/ladderclimb/",package.replace(".","/")+"/")

        appid = "0"
        keysplash = "0"
        try:  
            appid = mainAdConfig.GetAppId(Source.GDT,Source.ANDROID,isHD)
            keysplash = mainAdConfig.GetAppKeySplash(Source.GDT,Source.ANDROID,isHD)
        except Exception as e:  
            print("mainAdConfig eror=",e," file =")

        strfile = strfile.replace("_GDT_APP_ID_",appid)
        strfile = strfile.replace("_GDT_POS_ID_",keysplash)
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/"+strdir+"AdSplashActivity.smali"
        FileUtil.SaveString2File(strfile,dst) 
        # _GDT_APP_ID_  _GDT_POS_ID_


        src = mainResource.GetDirRootSmali()+"/smali/moonma/AdSplashActivity$1.smali"
        strfile = FileUtil.GetFileString(src) 
        strfile = strfile.replace("com/moonma/ladderclimb/",package.replace(".","/")+"/")
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/"+strdir+"AdSplashActivity$1.smali"
        FileUtil.SaveString2File(strfile,dst)  

        src = mainResource.GetDirRootSmali()+"/smali/moonma/UmengActivity.smali"
        strfile = FileUtil.GetFileString(src) 
        strfile = strfile.replace("com/moonma/ladderclimb/",package.replace(".","/")+"/")
        dst = self.GetDecodeApkOutputDir(isHD)+"/smali/"+strdir+"UmengActivity.smali"
        FileUtil.SaveString2File(strfile,dst)   


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
    
    p = GooglePlay() 
    if "download"==arg2:
    # 
        p.Init()
        p.GoApp(isHD)

    if "rebuild"==arg2:
        p.RebuildApk(isHD)

    if "decode"==arg2:
        p.DecodeApk(isHD)     
 
    if "InstallApk"==arg2:
        p.InstallApk(isHD)
        # p.ResizeImage()
 

    print("GooglePlay sucess arg=",arg2)
