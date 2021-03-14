#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime
import platform
import json
from hashlib import md5 

# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
# o_path = os.getcwd()  # 返回当前工作目录
# sys.path.append(o_path)  # 添加自己指定的搜索路径
from Common.Platform import Platform
from Common.File.FileUtil import FileUtil
from Common import Source
#http://blog.csdn.net/imzoer/article/details/8733396
#http://blog.sina.com.cn/s/blog_708be8850101bu02.html
##复制文件
#
#shutil.copyfile('listfile.py', 'd:/test.py')
#
##复制目录
#
#shutil.copytree('d:/www', 'c:/temp/')
class Resource(): 
    cmdPath=""  
    def CopyResourceFiles(self,sourceDir,  targetDir):

        #  先清除
        for file in os.listdir(targetDir):
            if file=="Common":
                continue
                
            targetFile = os.path.join(targetDir,  file)
            #目录
            if os.path.isdir(targetFile): 
                shutil.rmtree(targetFile)
            else :
                os.remove(targetFile)

        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
            targetFile = os.path.join(targetDir,  file)
            #目录
            if os.path.isdir(sourceFile): 
                shutil.copytree(sourceFile,targetFile)
            else :
                shutil.copyfile(sourceFile,targetFile)
 
    def SaveResourceFiles(self,sourceDir,  targetDir):

        #  先清除
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir,  file)
            #目录
            if os.path.isdir(targetFile): 
                shutil.rmtree(targetFile)
            else :
                os.remove(targetFile)

        for file in os.listdir(sourceDir):

            if file=="Common":
                continue

            sourceFile = os.path.join(sourceDir,  file)
            targetFile = os.path.join(targetDir,  file)
            #目录
            if os.path.isdir(sourceFile): 
                shutil.copytree(sourceFile,targetFile)
            else :
                shutil.copyfile(sourceFile,targetFile)

    #   

    #返回当前的日期，以便在创建指定目录的时候用：
    # def getCurTime():
    #           nowTime = time.localtime()
    #                 year = str(nowTime.tm_year)
    #                     month = str(nowTime.tm_mon)
    #                         if len(month) < 2:
    #                                 month = '0' + month
    #                                 day =  str(nowTime.tm_yday)
    #                                     if len(day) < 2:
    #                                             day = '0' + day
    #     return (year + '-' + month + '-' + day)

    #获取脚本文件的当前路径
    @staticmethod
    def cur_file_dir():
        #获取脚本路径
        path = sys.path[0]
        #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def SetCmdPath(self,cmdPath):  
        self.cmdPath = cmdPath 
        # print("SetCmdPath cmdPath=",cmdPath)
        key = "/cmd_"
        if Platform.isWindowsSystem():
            key = "\\cmd_"
        idx = cmdPath.find(key)
        # print("SetCmdPath idx=",idx)
        if idx>=0: 
            self.cmdPath = cmdPath[0:idx]
        # if isWindowsSystem():
        #     # windows 系统路径最后一个是\字符，需要删除
        #     self.cmdPath = getLastDirofDir(self.cmdPath)

        # # 跳过cmd_xxx目录
        # self.cmdPath = getLastDirofDir(self.cmdPath)
        # print("SetCmdPath2 self.cmdPath=",self.cmdPath)
   
        
    def getGameName(self):
        # print("getGameName self.cmdPath=",self.cmdPath)
        return FileUtil.GetDirNameofPath(self.cmdPath)

    def getGameType(self):
        return FileUtil.GetDirNameofPath(FileUtil.GetLastDirofDir(self.cmdPath)) 
         

    def get_FileSize(self,filePath):
        fsize = os.path.getsize(filePath) 
        return fsize

    def get_MD5_checksum_file(self,filename):
        with open(filename, 'rb') as f:
            md5obj = md5()
            while 1:
                buf = f.read(1024)
                if not buf:
                    break
                md5obj.update(buf)
        return md5obj.hexdigest()

    def GetProjectName(self): 
        #  F:\sourcecode\unity\product\kidsgame 
        path = self.cmdPath
        # print("GetProjectName path=",path)
        key = "/product/"
        if Platform.isWindowsSystem():
            key = "\\product\\" 
        idx = path.find(key)+len(key) 
        name = path[idx:]
        # print("GetProjectName name=",name)
        key = "/"
        if Platform.isWindowsSystem():
            key = "\\" 
        idx = name.find(key)
        name = name[0:idx]
        # path = getLastDirofDir(path)
        # path = getLastDirofDir(path)
        # name = getDirNameofPath(path)
        # print("GetProjectName,name = "+name)
        
        # print("GetProjectName name=",name)
        return name

    def GetRootDir(self):
        #Users/moon/sourcecode/unity/product/kidsgame
        key = "/"
        if Platform.isWindowsSystem():
            key = "\\"
        dir = self.GetDirProduct()+key+self.GetProjectName()
        # print("GetRootDir dir=",dir)
        return dir

    def GetDirProduct(self): 
        #Users/moon/sourcecode/unity/product 
        key = "/product/"
        if Platform.isWindowsSystem():
            key = "\\product\\"
        idx = self.cmdPath.find(key)+len(key)-1
        dir = self.cmdPath[0:idx]
        # print("GetDirProduct dir=",dir)
        return dir

    def GetDirProductCommon(self):   
        return self.GetDirProduct()+"/Common"


    def GameResApp(self):  
        dir = mainResource.GetResourceDataApp()+"/GameRes" 
        if os.path.exists(dir) ==False:
            dir = self.GameResCommon()
        return os.path.normpath(dir)

    def GameResCommon(self):   
        return self.GetDirProductCommon()+"/GameResCommon"+"/"+self.getGameName()

    def GetResourceDataRoot(self): 
        return self.GetRootDir()+"/ResourceData"

    def GetResourceDataApp(self):  
        gameType = self.getGameType()
        gameName = self.getGameName()
        path = self.GetResourceDataRoot()+"/"+gameType+"/"+gameName
        return os.path.normpath(path)


    def GetRootProjectUnity(self): 
        return self.GetRootDir()+"/"+self.GetProjectName()+Source.Dir_Name_GameEngine 

    def GetRootUnityAssetsResource(self): 
        return self.GetRootUnityAssets()+"/"+Source.Dir_Name_Resources
 

    def GetRootUnityAssets(self): 
        return self.GetRootProjectUnity()+"/"+Source.Dir_Name_Assets

    def GetProjectConfigCommon(self):
        # return self.GetDirProductCommon()+"/PythonCreator/ProjectConfig"
        return self.GetDirProductCommon()+"/Python"+Source.Dir_Name_GameEngine +"/ProjectConfig"

    def GetProjectConfig(self):
        return self.GetRootDir()+"/ProjectConfig"

    def GetProjectIcon(self):
        return self.GetRootDir()+"/ProjectIcon"

    def GetProjectIconApp(self):
        gameType = self.getGameType()
        gameName = self.getGameName()
        return self.GetProjectIcon()+"/"+gameType+"/"+gameName

    def GetProjectOutPut(self):
        return self.GetRootDir()+"/ProjectOutPut"

    def GetProjectOutPutIPA(self):
        dir="shu"
        if self.AppForPad(True):
            dir="heng" 

        return self.GetProjectOutPut()+"/IPA/"+dir

    def GetOutPutIPAName(self):
        gameType = self.getGameType()
        gameName = self.getGameName()

        ipa="ipa"+"_"+gameType+"_"+gameName+"_"+self.GetAppVersionIos()+".ipa"
        if self.AppForPad(True):
            ipa="ipa"+"_"+gameType+"_"+gameName+"_hd_"+self.GetAppVersionIos()+".ipa" 

        return ipa

    def GetProjectOutPutApp(self):
        gameType = self.getGameType()
        gameName = self.getGameName()
        path = self.GetProjectOutPut()+"/"+gameType+"/"+gameName
        return os.path.normpath(path)

    def GetOutPutScreenshot(self,isHd): 
        dirapk = self.GetProjectOutPutApp()+"/screenshot"
        if isHd==True:
            dirapk+="/heng" 
        else:
            dirapk+="/shu"
            
        return os.path.normpath(dirapk)

    def GetOutPutApkPath(self,channel,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        dirapk = self.GetProjectOutPutApp() + "/apk" 
        if isHd==True:
            dirapk+="/heng"
            gameName += "_hd"
        else:
            dirapk+="/shu"

        path = dirapk + "/" + gameType + "_" + gameName + "_" + channel + ".apk"
        return os.path.normpath(path)


    def GetOutPutApkPathWin32(self,rootdir,channel,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        # GetProjectOutPut
        dirapk = rootdir+"\\"+gameType+"\\"+gameName + "\\apk" 
        if isHd==True:
            dirapk+="\\heng"
            gameName += "_hd"
        else:
            dirapk+="\\shu"
        
        
        path = dirapk + "\\" + gameType + "_" + gameName + "_" + channel + ".apk"
        path = os.path.normpath(path)
        if Platform.isMacSystem():
            path = path.replace("\\","/")

        return path

    def GetOutPutIconPathWin32(self,rootdir,channel,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        # GetProjectOutPut
        dirapk = rootdir+"\\"+gameType+"\\"+gameName  
        if isHd==True:
            dirapk+="\\iconhd" 
        else:
            dirapk+="\\icon"

        path = os.path.normpath(dirapk)
        if Platform.isMacSystem():
            path = path.replace("\\","/")

        return path

    def GetOutPutCopyRightPathWin32(self,rootdir,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        # GetProjectOutPut
        dirapk = rootdir+"\\"+gameType+"\\"+gameName  
        if isHd:
            dirapk+="\\copyrighthd" 
        else:
            dirapk+="\\copyright"
            
        return os.path.normpath(dirapk)
        

    def GetOutPutScreenshotPathWin32(self,rootdir,channel,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        # GetProjectOutPut
        dirapk = rootdir+"\\"+gameType+"\\"+gameName+"\\screenshot"
        if isHd==True:
            dirapk+="\\heng" 
        else:
            dirapk+="\\shu"
            
        return os.path.normpath(dirapk)

    def GetOutPutAdPathWin32(self,rootdir,channel,isHd):
        gameType = self.getGameType()
        gameName = self.getGameName() 
        # GetProjectOutPut
        dirapk = rootdir+"\\"+gameType+"\\"+gameName+"\\ad" 
        return os.path.normpath(dirapk)

    def GetRootProjectIos(self):
        if Platform.IsVMWare():
            return self.GetRootProjectIosUser()
        return self.GetRootProjectIosNormal() 

    def GetRootProjectIosUser(self):
        return "/Users/moon/sourcecode/unity/product/"+"project_ios"

    def GetRootProjectIosNormal(self):
        return self.GetDirProduct()+"/project_ios"

    def GetRootProjectAndroid(self):
        return self.GetDirProductCommon()+"/project_android"

    def GetRootProjectWin(self):
        return self.GetRootDir()+"/project_win"



    def GetRootDirAndroidStudio(self):
        return self.GetDirProductCommon()+ "/project_android/game"
        # return self.GetRootDir()+ "/project_android/"+self.GetProjectName()

    def GetRootDirAndroidOutput(self):
        # GetRootProjectUnity()+"/OutPut/Android/"+GetProjectName()
        gameType = self.getGameType()
        gameName = self.getGameName() 
        return self.GetProjectOutPut()+"/Unity"+"/"+gameType+"/"+gameName+"/Android/"+"unityLibrary"
        

    def GetRootDirAndroidAsset(self): 
        return self.GetRootDirAndroidStudio()+ "/src/main/assets"

    def GetRootDirXcode(self): 
        if Platform.IsVMWare():
            return self.GetRootDirXcodeUser()

        return self.GetRootDirXcodeNormal()




    def GetProjectNameAppiOS(self):
        gameType = self.getGameType()
        gameName = self.getGameName()
        # return self.GetProjectName()+"_device"+"_"+gameType+"_"+gameName
        return "game_device"+"_"+gameType+"_"+gameName

    def GetRootDirXcodeNormal(self):
        return self.GetRootProjectIosNormal()+"/"+self.GetProjectNameAppiOS()

    def GetRootDirXcodeUser(self):
        #Users/moon/sourcecode/unity/product/kidsgame
        # "../../"
        return self.GetRootProjectIosUser()+"/"+self.GetProjectNameAppiOS()


    def GetProjectConfigDefault(self):
        return self.GetProjectConfigCommon()+"/CmdDefault"  

    def GetProjectConfigApp(self):
        gameType = self.getGameType()
        gameName = self.getGameName()
        path = self.GetProjectConfig()+"/"+gameType+"/"+gameName
        path = os.path.normpath(path)
        # print("GetProjectConfigApp path =",path+" gameType=",gameType," gameName=",gameName)
        return path

    def GetProjectConfigAppType(self):
        gameType = self.getGameType()
        return self.GetProjectConfig()+"/"+gameType

    def getAndroidProjectGameData(self): 
        path = self.GetDirProductCommon()+"/project_android/game"+"/src/main/assets/GameData"
        return path

    def getAndroidProjectApk(self): 
        # path = self.GetRootDir()+"/project_android/kidsgame/build/outputs/apk/"+"kidsgame-release.apk"
        path = self.GetDirProductCommon()+"/project_android/game"+"/build/outputs/apk/release/game"+"-release.apk"
        # 统一路径 windows是\
        path = os.path.normpath(path)
        return path

        
    def GetConfigDataDir(self): 
        apptype = self.getGameType()
        appname = self.getGameName()
        ret_dir = self.GetResourceDataRoot()+"/"+apptype+"/"+appname
        ret_dir+="/ConfigData"
        return ret_dir

    def GetGameDataDirOfResourceData(self): 
        apptype = self.getGameType()
        appname = self.getGameName()
        ret_dir = self.GetResourceDataRoot()+"/"+apptype+"/"+appname
        ret_dir+="/GameData"
        return ret_dir

    def GetAdConfigDir(self):
        return self.GetGameDataDirOfResourceData()+"/adconfig"

    def GetCommonAdConfigDir(self):
        return self.GetResourceDataRoot()+"/ConfigDataCommon/adconfig/cn"

    def GetConfigDir(self):
        return self.GetConfigDataDir()+"/config"
 
    def GetPackageAndroidFromXml(self):
        fileXml = self.GetRootDirAndroidStudio()+"/src/main/AndroidManifest.xml"
        strFile = FileUtil.GetFileString(fileXml)
        # package="com.moonma.shapecolor.pad"
        strHead = "package=\""
        strEnd = "\""
        idx = strFile.find(strHead)
        package = ""
        if idx>=0:
            idx +=len(strHead)
            strOther = strFile[idx:]
            idx = strOther.find(strEnd)
            package = strOther[0:idx]
        
        return package


    def GetPackageIos(self):
        xcode_plist = self.GetRootDirXcode()+ "/Info.plist" 
        print("xcode_plist="+xcode_plist)
        strFile = FileUtil.GetFileString(xcode_plist)
        # 		<key>CFBundleIdentifier</key>
        #	<string>com.moonma.pinpinle.nongchang</string>
        strHead = "CFBundleIdentifier"
        strMid = "<string>"
        strEnd = "</string>"
        idx = strFile.find(strHead)
        package = ""
        if idx>=0:
            idx +=len(strHead)
            strOther = strFile[idx:] 
            idx = strOther.find(strMid)
            if idx>=0:
                idx +=len(strMid)
                strOther = strOther[idx:] 
                idx = strOther.find(strEnd)
                package = strOther[0:idx]
        
        return package


    def GetAppVersionIos(self):
        xcode_plist = self.GetRootDirXcode()+ "/Info.plist" 
        print("xcode_plist="+xcode_plist)
        strFile = FileUtil.GetFileString(xcode_plist)
        # 		<key>CFBundleIdentifier</key>
        #	<string>com.moonma.pinpinle.nongchang</string>
        strHead = "CFBundleShortVersionString"
        strMid = "<string>"
        strEnd = "</string>"
        idx = strFile.find(strHead)
        package = ""
        if idx>=0:
            idx +=len(strHead)
            strOther = strFile[idx:] 
            idx = strOther.find(strMid)
            if idx>=0:
                idx +=len(strMid)
                strOther = strOther[idx:] 
                idx = strOther.find(strEnd)
                package = strOther[0:idx]
        
        return package

    def AppForPad(self,isIos):
        package = self.GetPackageAndroidFromXml()
        if isIos: 
            package = self.GetPackageIos()

        print("package="+package)

        ret = False
        if package.find(".ipad")>=0 or package.find(".pad")>=0:
            ret = True

        return ret


    def DeleteMetaFiles(self,sourceDir):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print(sourceFile)
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                src_apk_name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext = getFileExt(file) 
                # print(file="+file+" ext="+ext 
                apk_ext='meta'
                if apk_ext==ext:
                    print(sourceFile)
                    os.remove(sourceFile)
                    
            #目录嵌套
            if os.path.isdir(sourceFile):
                # print(sourceFile)
                self.DeleteMetaFiles(sourceFile)

mainResource = Resource() 


 