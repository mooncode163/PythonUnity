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

# include common.py
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Common import Source
from Project.Resource import mainResource
# import config 
from Project.ConfigSDKAndroid import mainConfigSDKAndroid
from Common.File.FileUtil import FileUtil 
from Common.File.ZipUtil import ZipUtil
from AppInfo.AppInfo import mainAppInfo
from Config.Config import mainConfig

class AppChannel(): 
    def getConfigJsonFile(self):
        return mainResource.getAndroidProjectGameData() + "/common/channel.json"


    def replaceString(self,strContent, strStart, strEnd, strReplace):
        idx = strContent.find(strStart)
        if idx < 0:
            return strContent

        strHead = strContent[0:idx]

        idx = idx + len(strStart)
        strOther = strContent[idx:]
        # print "strOther1:"+strOther
        idx = strOther.find(strEnd)
        strOther = strOther[idx:]
        # print(strOther2:"+strOther
        strRet = strHead + strStart + strReplace + strOther
        return strRet


    def replaceStringOfFile(self,filePath, strStart, strEnd, strReplace):
        f = open(filePath, 'r')
        strFile = f.read()
        # print strFile
        strOut = self.replaceString(strFile, strStart, strEnd, strReplace)
        # print strOut
        # fp_name.seek(0)
        # fp_name.write(strOut)
        f.close()
        return strOut

 


    def DeleteAndroidAssetGameRes(self):  
        # delete
        dir = mainResource.GetRootDirAndroidAsset()+"/GameRes" 
        if os.path.exists(dir): 
            shutil.rmtree(dir) 
         


    def UpdateChannel(self,channel,ishd): 
        print("updateChannel")
        # project_config = common.GetProjectConfigApp() + "/android" + "/gradle"
        targetDir = mainResource.GetRootDirAndroidStudio()
        sourceDir = mainResource.GetProjectConfigApp()
        project_android = "android/project"
        project_android_common = project_android
        rootAndroidStudio = mainResource.GetRootDirAndroidStudio()
        targetDir = rootAndroidStudio+"/src/main"

        # if ishd==True: 
        #     project_android = "android/project_hd"

        if channel == Source.GP:
            # self.MakeGooglePlayObbFile(ishd)
            if mainConfig.IsCloudRes():
                self.DeleteAndroidAssetGameRes()
                
            mainConfigSDKAndroid.SetShareSdk(False)
            mainConfigSDKAndroid.SetAdSdk(Source.ADMOB, True) 
            mainConfigSDKAndroid.SetAdSdk(Source.ADVIEW, False)
            mainConfigSDKAndroid.SetAdSdk(Source.GDT, False)
            mainConfigSDKAndroid.SetAdSdk(Source.BAIDU, False)
            mainConfigSDKAndroid.SetAdSdk(Source.XIAOMI, False)
            enable = True
            if mainConfig.IsForKid():
                enable = False
            print("mainConfig.IsForKid()=",mainConfig.IsForKid())
            # enable = False
            mainConfigSDKAndroid.SetAdSdk(Source.UNITY, enable)
            mainConfigSDKAndroid.SetAdSdk(Source.MOBVISTA, False)   
                # 
            project_config = sourceDir+"/"+project_android+"/config" 
            xml = sourceDir+"/"+project_android+"/xml_gp" 

            
        else:
            xml = sourceDir+"/"+project_android+"/xml"
            mainConfigSDKAndroid.SetAdSdk(Source.ADMOB, True)
            mainConfigSDKAndroid.SetAdSdk(Source.MOBVISTA, False)
            mainConfigSDKAndroid.SetAdSdk(Source.UNITY, True)
            mainConfigSDKAndroid.SetAdSdk(Source.BAIDU, True)

            # True
            mainConfigSDKAndroid.SetShareSdk(False)
            

                # 
            project_config = sourceDir+"/"+project_android+"/config"
            
        # FileUtil.CoverFiles(project_config,   targetDir)
        # FileUtil.CoverFiles(xml,   targetDir)

        build_gradle = mainResource.GetProjectConfigDefault() + "/android" + "/gradle/build"
        # or (channel == Source.GP)
        # if (channel == Source.TAPTAP) :
        #     build_gradle = build_gradle+"_"+channel 
        if (channel == Source.GP) :
            build_gradle = build_gradle+"_"+channel 

        build_gradle = build_gradle+".gradle"

        #配置build.grade
        #common.coverFiles(build_gradle,   targetDir)

        build_gradle_dst = rootAndroidStudio+"/build.gradle"
        flag = os.path.exists(build_gradle_dst)
        if flag:
            os.remove(build_gradle_dst)

        FileUtil.CopyOneFile(build_gradle,build_gradle_dst)

        #  "channel_android": "xiaomi"
        file = self.getConfigJsonFile()
        print ("channel_android="+file)
        strStart = "channel_android\": \""
        strEnd = "\""
        strOut = self.replaceStringOfFile(file, strStart, strEnd, channel)
        FileUtil.SaveString2File(strOut, file)


    def DeleAllObbFile(self,dir):
        for file in os.listdir(dir):
            path = os.path.join(dir,  file)  
            if os.path.isfile(path): 
                ext = FileUtil.GetFileExt(path)
                if ext =="obb" :
                    os.remove(path)
                
            #目录嵌套
            # if os.path.isdir(path): 
            #     self.DeleAllObbFile(path)


    def MakeGooglePlayObbFile(self,isHD):  
        print("MakeGooglePlayObbFile start")
        dir = mainResource.GameResApp() 
        print("MakeGooglePlayObbFile GameRes=",dir)
        self.DeleAllObbFile(FileUtil.GetLastDirofDir(dir))
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.GP)
        versioncode = mainAppInfo.GetAppVersionCode(Source.ANDROID,isHD)
        dir = FileUtil.GetLastDirofDir(dir)
        print("MakeGooglePlayObbFile file_zip dir =",dir)
        file_zip = dir+"/main."+str(versioncode)+"."+package+".obb"
        file_zip = dir+"/GameRes.zip"
        # main.13.com.itant.wuji.obb
        print("MakeGooglePlayObbFile obb file=",file_zip)
        # if os.path.exists(file_zip):
        #     os.remove(file_zip)

        # os.system("git config --global credential.helper store")
        # jobb -d D:\contents\ main\assets\ -o D:\obb\output.obb -pn com.example.app -pv 25
                # 压缩目录
        ZipUtil.zipDir(dir,file_zip)

        # delete
        dir = mainResource.GetRootDirAndroidAsset()+"/GameRes" 
        if os.path.exists(dir): 
            shutil.rmtree(dir) 
        
        print("MakeGooglePlayObbFile end")
        


mainAppChannel = AppChannel()

# 主函数的实现
# if __name__ == "__main__":
#     # 设置为utf8编码
#     # reload(sys)
#     # sys.setdefaultencoding("utf-8")

#     # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
#     cmdPath = FileUtil.cile_dir()
#     count = len(sys.argv)
#     for i in range(1, count):
#         print("参数", i, sys.argv[i])
#         if i == 1:
#             cmdPath = sys.argv[i]

#     common.SetCmdPath(cmdPath)

#     # updateChannel(Source.TAPTAP)

#     print ("appchannel sucess")
