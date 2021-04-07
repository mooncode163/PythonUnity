#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime
o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./')  
from Config.Config import mainConfig
from Common import Source
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
from Project.IPABuild import mainIPABuild
from Common.Platform import Platform
from Project.ConfigSDKAndroid import mainConfigSDKAndroid
 
class CopyConfig(): 
    def UpdateXcodeProjectFile(self,fileProject,isHD):
        flag = os.path.exists(fileProject)
        if not flag:
            return

        package = mainAppInfo.GetPackage(Source.IOS,isHD) 

        # 读取xcode文件的包名
        # PRODUCT_BUNDLE_IDENTIFIER = com.moonma.xiehanzi.pad;
        strFile = FileUtil.GetFileString(fileProject)
        strHead = "PRODUCT_BUNDLE_IDENTIFIER = "
        strEnd = ";"
        idx = strFile.find(strHead)
        if idx>=0:
            idx +=len(strHead)
            strOther = strFile[idx:]
            idx = strOther.find(strEnd)
            packageold = strOther[0:idx]
            print("packageold="+packageold) 
            strFile = strFile.replace(packageold,package)
            FileUtil.SaveString2File(strFile,fileProject)

        


        
    def CopyAndroidJavaFile_Weixin(self,rootStudio,isHD):
        dirroot = mainResource.GetProjectConfigApp()
        strFileFrom = dirroot+"/android/src/wxapi/WXEntryActivity.java"
        strFileTo = rootStudio+"/src/main/java/com/moonma/common/share/wxapi/WXEntryActivity.java"
        
        # loadJson
        package = AppInfo.GetPackage(source.ANDROID,isHD)  
        # 替换包名
        f = open(strFileFrom, 'r')
        strFile = f.read()
        f.close()  

        strOut = strFile.replace("_PACKAGE_", package)
        mainResource.saveString2File(strOut,strFileTo) 

#主函数的实现
    def Run(self,isHD): 
        print("CopyConfig isHD="+str(isHD))
    # rootDir ="/Users/jaykie/sourcecode/cocos2dx/product/game/ertong"
        rootAndroidStudio = mainResource.GetRootDirAndroidStudio()
        rootiOSXcode = mainResource.GetRootDirXcode()
        xcodeProject = rootiOSXcode+"/Unity-iPhone.xcodeproj/project.pbxproj"
        resDataName = mainResource.getGameName()#sys.argv[1]
        
        # adDirName = sys.argv[3]

        project_ios = "ios/project"
        project_android = "android/project"
        iconDirName = "icon"
        if isHD: 
            iconDirName = "iconhd"
            # project_ios = "ios/project_hd"
            # project_android = "android/project_hd"
    
        print("CopyConfig project_android="+project_android)
        # project
        iconRoot =mainResource.GetProjectOutPutApp()
        reousceDataRoot = mainResource.GetResourceDataRoot() 
        sourceDir = mainResource.GetProjectConfigApp()
        # sourceAdDir = "../../../../ad_src/"+adDirName
        # adCommonDir = "../../../../../common_ad"
        # adSrcDir = adCommonDir+"/ad_src/"+adDirName
        targetDir = rootAndroidStudio+"/src/main"
        
        # resoucedata 
        # dirname = "Resources"
        # dir1 = reousceDataRoot+"/"+resDataName+"/"+dirname
        # dir2 = reousceUnity
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

    
        # ios icon
        #先清除unity自动生成的目录
        dir1 =mainResource.GetDirProductCommon()+"/LaunchScreenIcon_ios/Unity-iPhone"
        dir2 = rootiOSXcode + "/Unity-iPhone"
        flag = os.path.exists(dir1) and os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        dir1 = iconRoot+"/"+iconDirName+"/ios"
        dir2 = rootiOSXcode + "/Unity-iPhone/Images.xcassets/AppIcon.appiconset"
        flag = os.path.exists(dir1) and os.path.exists(dir2)
        if flag:
            FileUtil.CoverFiles(dir1,   dir2)


        #android icon
        dir1 = iconRoot+"/"+iconDirName+"/android"
        # dir1 = os.path.normpath(dir1)
        # dir2 = sourceDir+"/res"
        dir2 = mainResource.GetProjectConfigApp()+"/"+project_android+"/res"
        # dir2 = os.path.normpath(dir2)
        # if iconDirName=="iconhd":
        #     dir2 = "./android/project/res_hd"
        print(dir1) 
        
        print(dir2) 
        # FileUtil.CoverFiles(dir1,dir2)

        # 
        project = sourceDir+"/"+project_android+"/xml"
        # FileUtil.CoverFiles(project,   targetDir)

        project = sourceDir+"/android"+"/gradle"
        targetDir = rootAndroidStudio
        # FileUtil.CoverFiles(project,   targetDir)


        
        #res android
        # dir1 = sourceDir+"/"+project_android + "/res"  
        # targetDir = rootAndroidStudio+"/src/main"
        # dir2 = targetDir+"/res"
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)

        # shutil.copytree(dir1,dir2)
    

        # ios
        # appname
        # dir1 = sourceDir+"/"+project_ios+"/appname"
        # dir2 = rootiOSXcode+"/appname"
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)
        # shutil.copytree(dir1,dir2)

        #info
        # file1 = sourceDir + "/"+project_ios+"/info.plist"
        # file2 = rootiOSXcode + "/info.plist"
        # print("info.plist file1= "+file1)
        # print("info.plist file2= "+file2)
        # FileUtil.CopyOneFile(file1,file2) 

    
        # win res 
        dir1 = iconRoot+"/"+iconDirName+"/microsoft"
        dir2 = mainResource.GetRootProjectWin()+"/"+mainResource.GetProjectName()+"/Assets"
        if os.path.exists(dir2):
            FileUtil.CoverFiles(dir1,   dir2)

        # win strings 
        dir_src_string = mainResource.GetProjectConfigApp()+"/"+Source.WIN + "/project"
        # if isHD:
        #     dir_src_string = mainResource.GetProjectConfigApp()+"/"+Source.WIN + "/project_hd"
        dir1 = dir_src_string+"/strings"
        dir2 = mainResource.GetRootProjectWin()+"/"+mainResource.GetProjectName()+"/strings" 
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
            shutil.copytree(dir1,dir2)
        
        

    # ad src
        # dir1 = adSrcDir;
        # dir2 =  rootAndroidStudio+"/src/main/java/com/moonma/common/ad"
        # flag = os.path.exists(dir2)
        # if flag:
        #     shutil.rmtree(dir2)

        # shutil.copytree(dir1,dir2)

        # CopyAndroidJavaFile_Weixin(rootAndroidStudio,isHD)

        # if not mainResource.isWindowsSystem():
        self.UpdateXcodeProjectFile(xcodeProject,isHD)

        # AD LIB JAVA CODE

 


        appid_xiaomi = mainAdConfig.GetAppId(Source.XIAOMI,Source.ANDROID,isHD)
        if "0"==appid_xiaomi:
            print("no xiaomi ad appid")
            # VUNGLE 和 XIAOMI sdk gson库 冲突
            mainConfigSDKAndroid.SetAdSdk(Source.XIAOMI, False)
            # True
            mainConfigSDKAndroid.SetAdSdk(Source.VUNGLE, False)
        else:
            mainConfigSDKAndroid.SetAdSdk(Source.XIAOMI, False)
            mainConfigSDKAndroid.SetAdSdk(Source.VUNGLE, False)
    
        
        appid_gdt = mainAdConfig.GetAppId(Source.GDT,Source.ANDROID,isHD)
        if "0"==appid_gdt:
            print("no gdt ad appid")
            mainConfigSDKAndroid.SetAdSdk(Source.GDT, False)
        else:
            mainConfigSDKAndroid.SetAdSdk(Source.GDT, True)


        mainConfigSDKAndroid.SetAdSdk(Source.ADVIEW, False) 
        
        mainConfigSDKAndroid.SetAdSdk(Source.UNITY, True)
        # mainConfigSDKAndroid.SetAdSdk(Source.ADMOB, True)
        
        if Platform.isMacSystem():
            mainIPABuild.ChmodSh();

        print("copy_config sucess")

mainCopyConfig = CopyConfig() 
