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
#include mainResource.py
# sys.path.append('./common')

# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Config.Config import mainConfig
from Common import Source 
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource

from xml.dom.minidom import parse
from AppStore.AppVersionHuawei import mainAppVersionHuawei
from AppStore.AppVersionTapTap import mainAppVersionTapTap


from AppStore.AppVersionApple import mainAppVersionApple
from AppStore.Huawei.HuaweiAppGalleryApi import mainHuaweiAppGalleryApi
from AppStore.AppStoreAcount import mainAppStoreAcount

from AppInfo.AppInfoOld import AppInfoOld
from AppInfo.AppInfoNew import AppInfoNew
from Common.File.JsonUtil import JsonUtil 
from Common.File.FileUtil import FileUtil 

class AppInfo(): 
    versionCode = 100
    rootJson=None

    def GetUrl(self, url): 
        r = requests.get(url)
        return r.content.decode('utf-8',"ignore")

    def GetSmsCode(self):  
        # url = "http://47.242.56.146:5000/GetSmsCode" 
        url = "http://mooncore.cn:5000/GetSmsCode"  
        return self.GetUrl(url) 

    def SetSmsCode(self,code):  
        url = "http://mooncore.cn:5000/SetSmsCode?code="+code
        return self.GetUrl(url) 

    def SetCmdPath(self,cmdPath):  
        mainResource.SetCmdPath(cmdPath)

    def GetJsonAppId(self,jsonData, channel):  
        return jsonData["appid"][channel] 
    

    def GetPackage(self,osSrc,isHD): 
        jsonData = self.loadJson(isHD) 
        isOld = self.IsOldVersion(jsonData)
        ret = ""
        if isOld:
            key = "PACKAGE_IOS"
            if osSrc == Source.ANDROID:
                key = "PACKAGE_ANDROID" 
            ret = jsonData[key]
        else:      
            if osSrc == Source.ANDROID:
                ret = jsonData["apppackage"][Source.ANDROID]["default"] 
            if osSrc == Source.IOS:
                ret = jsonData["apppackage"][Source.IOS]["default"]

        return ret

    def GetJsonFile(self,isHd):
        cur_path = mainResource.GetProjectConfigApp()+"/appinfo"
        jsonfile = cur_path+'/appinfo.json'
        if isHd:
            jsonfile = cur_path+'/appinfo_hd.json'
        return os.path.normpath(jsonfile)

    def loadJson(self,isHd,isReload=False):  
        if self.rootJson is None or isReload is True:
            jsonfile = self.GetJsonFile(isHd) 
            strfile = FileUtil.GetFileString(jsonfile)
            self.rootJson = json.loads(strfile)

        return self.rootJson
        
        # with  open(jsonfile, 'rb') as json_file:
        #     data = json.load(json_file)
        #     return data


    def replaceString(self,strContent, strStart, strEnd, strReplace):
        idx = strContent.find(strStart)
        strHead = strContent[0:idx]

        idx = idx + len(strStart)
        strOther = strContent[idx:]
        # print "strOther1:"+strOther
        idx = strOther.find(strEnd)
        strOther = strOther[idx:]
        # print "strOther2:"+strOther
        strRet = strHead + strStart + strReplace + strOther
        return strRet


    def replaceFile(self,filePath, strOld, strReplace): 
        strFile = FileUtil.GetFileString(filePath)
        strOut = strFile.replace(strOld, strReplace) 
        self.saveString2File(strOut, filePath)


    def replaceStringOfFile(self,filePath, strStart, strEnd, strReplace):
        # f = open(filePath)
        # f = open(filePath,'r', encoding='UTF-8') 
        strFile = FileUtil.GetFileString(filePath)
        # strFile.decode('utf-8')
        # print strFile
        strOut = self.replaceString(strFile, strStart, strEnd, strReplace)
        # print strOut
        # fp_name.seek(0)
        # fp_name.write(strOut) 
        return strOut

    def replacePackage(self,filePath,package):
        strFile = FileUtil.GetFileString(filePath) 
        strFile = strFile.replace("_PACKAGE_", package)
        FileUtil.SaveString2File(strFile,filePath)

    def replaceFileForKey(self,filePath,key,content):
        # f = open(filePath, 'rb')
        # f = open(filePath,'r', encoding='utf-8')
        strFile = FileUtil.GetFileString(filePath) 
        strFile = strFile.replace(key, content)
        FileUtil.SaveString2File(strFile,filePath)

    def replaceFile(self,filePath,key,value):
        strFile = FileUtil.GetFileString(filePath) 
        strFile = strFile.replace(key, value)
        FileUtil.SaveString2File(strFile,filePath) 
 

    def replaceString2(self,strContent, strStart, strMid, strEnd, strReplace):
        idx = strContent.find(strStart)
        if idx<0:
            return strContent
        strHead = strContent[0:idx] + strStart

        idx = idx + len(strStart)
        strOther = strContent[idx:] 
        idx = strOther.find(strMid)
        strHead2 = strOther[0:idx] + strMid
        strHead += strHead2

        # print "strOther1="+strOther 
        strOther = strOther[idx+len(strMid):]
        # print "strOther2="+strOther

        idx = strOther.find(strEnd)
        strOther = strOther[idx:] 
        strRet = strHead + strReplace + strOther
        return strRet


    def replaceStringOfFile2(self,filePath, strStart, strMid, strEnd, strReplace):
        strFile = FileUtil.GetFileString(filePath)
        # print strFile
        strOut = self.replaceString2(strFile, strStart, strMid, strEnd, strReplace)
        # print strOut
        # fp_name.seek(0)
        # fp_name.write(strOut) 
        return strOut


    def saveString2File(self,str, file):
        FileUtil.SaveString2File(str, file)


    def replaceGoogleServiceFile(self,filepath,fileoutput, package):
        strfile = FileUtil.GetFileString(filepath)
        
        # version  
        strStart = "client_id\": \"android:"
        strEnd = "\""
        strfile = self.replaceString(strfile, strStart, strEnd, package)
        

        strStart = "package_name\": \""
        strEnd = "\""
        strfile = self.replaceString(strfile, strStart, strEnd, package)
      

        strStart = "\"android_info\""
        strMid = "package_name\": \""
        strEnd = "\","
        strfile = self.replaceString2(strfile, strStart, strMid, strEnd, package)
        self.saveString2File(strfile, fileoutput)

    def replaceXcodeUrlScheme(self,strFile,src, appid,idx): 
        # <string>WEIXIN_APPID</string>
        if src==Source.WEIXIN or src==Source.WEIXINFRIEND:
            strOld = "<string>WEIXIN_APPID</string>"
        if src==Source.WEIBO:
            strOld = "<string>WEIBO_APPID</string>"
        if src==Source.QQ or src==Source.QQZONE:
            if idx==0:
                strOld = "<string>QQ_APPID0</string>"
            if idx==1:
                strOld = "<string>QQ_APPID1</string>"

        strNew = "<string>"+mainConfig.XcodeUrlScheme(src,appid,idx)+"</string>"  

        return strFile.replace(strOld, strNew) 
        # print("strOld =",strOld,"strNew =",strNew,"strOut =",strOut)
    
        



    def updateXiaoASOkeyword(self,jsonData,isHd):
        jsonfile = self.GetJsonFile(isHd)
        isOld = self.IsOldVersion(jsonData)
        if isOld:
            APPSTORE_KEYWORD = jsonData["APPSTORE_KEYWORD"]
            strStart = "XIAOMI_KEYWORD"
        else:
            APPSTORE_KEYWORD =  jsonData["appstore"]["aso"]
            strStart = "aso_xiaomi"

        
        cn = APPSTORE_KEYWORD["cn"]
        en = APPSTORE_KEYWORD["en"]
        cn = cn.replace(","," ")
        en = en.replace(","," ")

        
        strEnd = "\""

        strFile = FileUtil.GetFileString(jsonfile)

        strMid = "\"cn\": \""
        strFile = self.replaceString2(strFile, strStart, strMid, strEnd, cn)

        strMid = "\"en\": \""
        strFile = self.replaceString2(strFile, strStart, strMid, strEnd, en)
        FileUtil.SaveString2File(strFile, jsonfile)

    def copyResFiles(self,str):
        dir_default = mainResource.GetProjectConfigDefault()
        # "../../../default"
        dir_to = mainResource.GetProjectConfigApp()

        dir1 = dir_default+"/"+str
        dir2 = dir_to + "/"+str
        print(dir2)
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

    # def SaveJson(filePath,dataRoot): 
    #     oldvalue = ""
    #     # "huawei": "0",
    #     # str1 = "\""+key+"\""+": \""+oldvalue+"\""
    #     # str2 = "\""+key+"\""+": \""+value+"\""
    #     # replaceFile(filePath, str1, str2)

    #     # 保存json
    #     with open(filePath, 'w') as f:
    #         json.dump(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True)


    def autoPlusVersion(self,isHd,chanel=""): 
        jsonfile = self.GetJsonFile(isHd) 

       
        if chanel==Source.APPSTORE:
        # ios 
            appversionjson = self.GetAppVersionJson(Source.IOS,isHd,"")
            codeios = appversionjson["code"]
            int_v = int(codeios)
            int_v=int_v+1
            codeios = str(int_v)
            appversionjson["code"]=codeios
            # self.versionCode = codeios
            appversionjson["value"]=self.versionCodeToVersion(codeios)
            print(" codeios =",codeios)
        else:
            self.versionCode = self.GetAppVersionCode(Source.ANDROID, isHd,chanel) 
            int_v = int(self.versionCode)
            int_v=int_v+1
            self.versionCode = str(int_v) 
            appversionjson = self.GetAppVersionJson(Source.ANDROID,isHd,chanel)
            # dataCode = self.GetAppVersionCode(Source.ANDROID, isHd,chanel)
            appversionjson["code"]=self.versionCode
            appversionjson["value"]=self.versionCodeToVersion(self.versionCode)

        # SaveJson(jsonfile,jsonData)
        JsonUtil.SaveJson(jsonfile,self.loadJson(isHd))  
        # strnew_version_ios = "\"APPVERSION_IOS\": \""+versionCodeToVersion()+"\""



        


    # 161 to 1.6.1
    def versionCodeToVersion(self,value):
        print ("versionCodeToVersion=", value)
        code_v = int(value)
        # 
        v0 = int(code_v/100)
        v1 =int((code_v-v0*100)/10)
        v2 = code_v-v0*100-v1*10
        ret = str(v0)+"."+str(v1)+"."+str(v2)
        return ret

    def updateAndroidManifest(self,filepath,fileoutput,package,appversion,appversioncode,isHd):
        strfile = FileUtil.GetFileString(filepath)
        
        # version 
        strfile = strfile.replace("_VERSIONNAME_",appversion)
        strfile = strfile.replace("_VERSIONCODE_",appversioncode) 

        # package 
        strfile = strfile.replace("_PACKAGE_",package) 
        # ScreenOrientation 
        str = "sensorPortrait"
        if isHd:
            str = "sensorLandscape"

        strfile = strfile.replace("_SCREENORIENTATION_", str)

        # baidu
        appid_baidu = mainAdConfig.GetAppId(Source.BAIDU,Source.ANDROID,isHd)
        strfile = strfile.replace("_BAID_AD_APPID_",appid_baidu)  
        FileUtil.SaveString2File(strfile,fileoutput)
        


    def IsOldVersion(self,data):
        isOld = True
        if ("appname" in data) :
            isOld = False  
        
        return isOld

    def GetCSVName(self,strContent,isHd): 
        idxstart = strContent.find("APP_NAME")
        if isHd:
            idxstart = strContent.find("APP_NAME_HD")

        strContent = strContent[idxstart:] 
        idxend = strContent.find("\r\n")
        if idxend<0:
            idxend = strContent.find("\n")

        strContent = strContent[0:idxend] 
        return strContent


    def UpdateLanguageName(self,csvfile,name_cn,name_en,ishd): 
        strContent = FileUtil.GetFileString(csvfile)
        key_name = self.GetCSVName(strContent,ishd) 

        head = "APP_NAME"
        if ishd:
            head = "APP_NAME_HD"

        str_new = head+","+name_cn+"," +name_en
        # +"\n"
        self.replaceFile(csvfile,key_name,str_new)


    def GetConfigDataAppId(self,os,chanel,ishd):
        dirconfig = mainResource.GetConfigDataDir()
        filepath = ""
        appid = ""
        if os==Source.ANDROID:
            filepath = dirconfig+"/config/config_android.json"
            if ishd:
                filepath = dirconfig+"/config/config_android_hd.json"
    
        if os==Source.IOS:
            filepath = dirconfig+"/config/config_ios.json"
            if ishd:
                filepath = dirconfig+"/config/config_ios_hd.json"
        

        with open(filepath) as json_file:
            data = json.load(json_file)
            appid = data["APPID"][chanel] 

        return appid

    def SetConfigDataAppId(self,os,chanel,appid,ishd):
        dirconfig = mainResource.GetConfigDataDir()
        filepath = ""
        if os==Source.ANDROID:
            filepath = dirconfig+"/config/config_android.json"
            if ishd:
                filepath = dirconfig+"/config/config_android_hd.json"
    
        if os==Source.IOS:
            filepath = dirconfig+"/config/config_ios.json"
            if ishd:
                filepath = dirconfig+"/config/config_ios_hd.json"
        

        with open(filepath) as json_file:
            data = json.load(json_file)
            data["APPID"][chanel] = appid
            # SaveJson(filepath,data)
            JsonUtil.SaveJson(filepath,data)

    def GetAppUpdate(self,isHd,lan): 
        data = self.loadJson(isHd) 
        name = data["appstore"]["version_update"][lan]
        return name 

    def GetAppSubtitle(self,isHd,lan): 
        data = self.loadJson(isHd) 
        name = data["appstore"]["subtitle"][lan]
        return name 



    def GetAppDetail(self,isHd,lan): 
        src = mainResource.GetProjectConfigApp()+"/appinfo/app_description.xml"
        if isHd:
            src = mainResource.GetProjectConfigApp()+"/appinfo/app_description_hd.xml"

        domTree = parse(src)
        # 文档根元素root = domTree.documentElement
        root = domTree.documentElement
        # print(root.nodeName)
        
        strret =" " 
        key = lan
        # if lan==Source.LANGUAGE_CN:
        #     key = "cn"

        list = root.getElementsByTagName(key)
        for item in list:
            strret = item.childNodes[0].data 

        # print(strret)
        return strret
        # for customer in customers:
        # 	if customer.hasAttribute("ID"):
        # 		print("ID:", customer.getAttribute("ID"))
        # 		# name 元素
        # 		name = customer.getElementsByTagName("name")[0]
        # 		print(name.nodeName, ":", name.childNodes[0].data)
        # 		# phone 元素
        # 		phone = customer.getElementsByTagName("phone")[0]
        # 		print(phone.nodeName, ":", phone.childNodes[0].data)
        # 		# comments 元素
        # 		comments = customer.getElementsByTagName("comments")[0]
        # 		print(comments.nodeName, ":", comments.childNodes[0].data)


    def GetAppVersionJson(self,os,isHd,channel=""): 
        # loadJson
        data = self.loadJson(isHd)    
        key = os
        appversion = data["appversion"]
        if os==Source.ANDROID:
            if len(channel)>0 and channel in appversion: 
                key = channel 
        
        # if channel==Source.HUAWEI:
        #     key = os

        return appversion[key]


    def GetAppVersion(self,os,isHd,channel=""): 
        # loadJson
        data = self.loadJson(isHd)     
        appversion = self.GetAppVersionJson(os,isHd,channel) 
        name =  appversion["value"]
        return name

    def GetAppVersionCode(self,os,isHd,channel=""): 
        # loadJson
        data = self.loadJson(isHd)    
        appversion = self.GetAppVersionJson(os,isHd,channel) 
        name =  appversion["code"] 
        return name

    def LoadJsonConfigCommon(self):  
        jsonfile = mainResource.GetConfigDataDir()+"/config/config_common.json"  
        jsonfile = os.path.normpath(jsonfile)
        strfile = FileUtil.GetFileString(jsonfile)
        return json.loads(strfile) 

    def GetAppStoreAcount(self,isHd,appstore): 
        data = self.LoadJsonConfigCommon()
        key = "appstore_acount"
        name = "chyfemail163@163.com"
        if appstore==Source.IOS:
            name = "chyfemail163@163.com"
        if key in data:
            name = data[key][appstore]
        print(" GetAppStoreAcount name=",name)

        return name 

    def GetAppPromotion(self,isHd,lan): 
        data = self.loadJson(isHd) 
        name = data["appstore"] ["promotion"][lan]
        return name 
    
    def GetAppName(self,os,isHd,lan,channel = ""): 
        # loadJson
        data = self.loadJson(isHd)
        appname = data["appname"]
        name = appname[os][lan]
        if len(channel)>0 and channel in appname:
            name = appname[channel][lan]
        return name 

    def GetAppPackage(self,os,isHd,channel = ""): 
        # loadJson
        data = self.loadJson(isHd) 
        apppackage = data["apppackage"]  
        name = apppackage[os]["default"]
        if len(channel)>0 and channel in apppackage[os]:
            name = apppackage[os][channel]
        return name 

    def GetAppPrivacyUrl(self,isHd): 
        # loadJson
        data = self.loadJson(isHd)  
        name = data["privacy_url"]
        return name   

    def GetAppSKU(self,isHd): 
        # loadJson
        data = self.loadJson(isHd)  
        name = data["sku_app"]
        return name   

    def GetAppSoftwareUrl(self,isHd): 
        # loadJson
        data = self.loadJson(isHd)  
        name = data["software_url"]
        return name   

    def GetAppSupportUrl(self,isHd): 
        # loadJson
        data = self.loadJson(isHd)  
        name = data["support_url"]
        return name   

    def GetAppUrl(self,os,isHd,channel): 
        # loadJson
        appid = self.GetAppId(isHd, channel)
        url = ""
        if os == Source.ANDROID:
            if channel == Source.TAPTAP:
                url = "https://www.taptap.com/app/"+appid
            else: 
                url = "https://appgallery1.huawei.com/#/app/C"+appid               

        if os == Source.IOS:
            appid = self.GetAppId(isHd, Source.APPSTORE)
            url = "https://apps.apple.com/cn/app/id"+appid

        return url   

                
            
    def GetAppId(self,isHd,channel): 
        # loadJson
        data = self.loadJson(isHd) 
        appid = data["appid"][channel] 
        return appid 
 
    def SetAppVersion(self,isHd,os,value,channel=""):  
        appversionjson = self.GetAppVersionJson(os,isHd,channel)  
        appversionjson["value"] = value
        filePath = self.GetJsonFile(isHd)
        data = self.loadJson(isHd) 
        JsonUtil.SaveJson(filePath,data)

    def SetAppVersionCode(self,isHd,os,value,channel=""): 
        appversionjson = self.GetAppVersionJson(os,isHd,channel)  
        appversionjson["code"] = value 
        filePath = self.GetJsonFile(isHd)
        data = self.loadJson(isHd) 
        JsonUtil.SaveJson(filePath,data)      

    def SetAppId(self,isHd,os,channel,appid):
        # loadJson
        data = self.loadJson(isHd)  
        data["appid"][channel] =appid
        filePath = self.GetJsonFile(isHd)
        JsonUtil.SaveJson(filePath,data)

    def SetAso(self,isHd,channel,lan,aso):
        # loadJson
        if len(aso)==0:
            return
            
        data = self.loadJson(isHd)  
        key = "aso"
        data["appstore"][key][lan] =aso
        filePath = self.GetJsonFile(isHd)
        JsonUtil.SaveJson(filePath,data)  

    def GetAso(self,isHd,channel,lan): 
        data = self.loadJson(isHd)  
        key = "aso"
        ret = data["appstore"][key][lan]
        if len(ret)>100:
            ret = ret[0:100]
        print(" aso count =",len(ret))
        return ret 

    def ConvertOld2New(self,isHd,appinfoOld):
        appinfoNew = AppInfoNew(isHd)

        # appid
        appid = appinfoOld.GetAppId(Source.HUAWEI)
        appinfoNew.SetAppId(Source.HUAWEI,appid)

        appid = appinfoOld.GetAppId(Source.TAPTAP)
        appinfoNew.SetAppId(Source.TAPTAP,appid)

        appid = appinfoOld.GetAppId(Source.APPSTORE) 
        appinfoNew.SetAppId(Source.APPSTORE,appid)

        appid = "0"
        appinfoNew.SetAppId(Source.XIAOMI,appid)

        # appname 
        name = appinfoOld.GetAppName(Source.ANDROID,Source.LANGUAGE_CN)
        appinfoNew.SetAppName(Source.ANDROID,Source.LANGUAGE_CN,name)
        name = appinfoOld.GetAppName(Source.ANDROID,Source.LANGUAGE_EN)
        appinfoNew.SetAppName(Source.ANDROID,Source.LANGUAGE_EN,name)
        name = appinfoOld.GetAppName(Source.IOS,Source.LANGUAGE_CN)
        appinfoNew.SetAppName(Source.IOS,Source.LANGUAGE_CN,name)
        name = appinfoOld.GetAppName(Source.IOS,Source.LANGUAGE_EN)
        appinfoNew.SetAppName(Source.IOS,Source.LANGUAGE_EN,name)

        # apppackage
        name = appinfoOld.GetPackage(Source.ANDROID)
        appinfoNew.SetAppPackage(Source.ANDROID,name)
        name = appinfoOld.GetPackage(Source.IOS)
        appinfoNew.SetAppPackage(Source.IOS,name)


        # appstore
        aso = appinfoOld.APPSTORE_KEYWORD(Source.LANGUAGE_CN)
        aso_xiaomi = appinfoOld.APPSTORE_KEYWORD(Source.LANGUAGE_CN)
        promotion = appinfoOld.APPSTORE_PROMOTION(Source.LANGUAGE_CN)
        subtitle = appinfoOld.APPSTORE_SUBTITLE(Source.LANGUAGE_CN)
        title = appinfoOld.APPSTORE_TITLE(Source.LANGUAGE_CN)
        version_update = appinfoOld.APPSTORE_VERSION_UPDATE(Source.LANGUAGE_CN)
        appinfoNew.SetAppstore(Source.LANGUAGE_CN,aso,aso_xiaomi,promotion,subtitle,title,version_update)

        aso = appinfoOld.APPSTORE_KEYWORD(Source.LANGUAGE_EN)
        aso_xiaomi = appinfoOld.APPSTORE_KEYWORD(Source.LANGUAGE_EN)
        promotion = appinfoOld.APPSTORE_PROMOTION(Source.LANGUAGE_EN)
        subtitle = appinfoOld.APPSTORE_SUBTITLE(Source.LANGUAGE_EN)
        title = appinfoOld.APPSTORE_TITLE(Source.LANGUAGE_EN)
        version_update = appinfoOld.APPSTORE_VERSION_UPDATE(Source.LANGUAGE_EN)
        appinfoNew.SetAppstore(Source.LANGUAGE_EN,aso,aso_xiaomi,promotion,subtitle,title,version_update)


    # appversion
        version =  appinfoOld.GetAppVersion(Source.ANDROID)
        code =  appinfoOld.GetAppVersionCode(Source.ANDROID)
        appinfoNew.SetAppversion(Source.ANDROID,code,version)

        version =  appinfoOld.GetAppVersion(Source.IOS)
        code =  appinfoOld.GetAppVersionCode(Source.IOS)
        appinfoNew.SetAppversion(Source.IOS,code,version)


        appinfoNew.SetKeyVaule("need_upload_screenshot",appinfoOld.need_upload_screenshot())

        appinfoNew.SetKeyVaule("email","chyfemail163@163.com")
        appinfoNew.SetKeyVaule("privacy_url","https://6c69-lianlianle-shkb3-1259451541.tcb.qcloud.la/PrivacyPolicy.txt")
        appinfoNew.SetKeyVaule("privacy_url2","https://6d6f-moonma-dbb297-1258816908.tcb.qcloud.la/Moonma/privacyPolicy_kidsgame.txt")
        appinfoNew.SetKeyVaule("privacy_url3"," http://www.mooncore.cn/index/privacyPolicy_kidsgame.shtml")
        appinfoNew.SetKeyVaule("software_url"," http://www.mooncore.cn")
        appinfoNew.SetKeyVaule("support_url"," http://blog.sina.com.cn/s/blog_1736372fb0102xb49.html")
        appinfoNew.SetKeyVaule("sku_app",appinfoOld.sku_app())
        
        appinfoNew.Save()   



    


    def SaveAppVersion(self,isHd,osSrc,version,channel=""):
        strcode = version.replace(".","")
        # key = osSrc 
        # if osSrc==Source.ANDROID:
        #     if len(channel)>0: 
        #         key = channel
            
          # 保存版本
        self.SetAppVersion(isHd,osSrc,version,channel)
        self.SetAppVersionCode(isHd,osSrc,strcode,channel)
 

    def CopyAppInfoAndroid(self,isHd,chanel=""):
        name = mainAppInfo.GetAppStoreAcount(isHd,Source.HUAWEI) 
        mainHuaweiAppGalleryApi.ClientId = mainAppStoreAcount.GetClientId(Source.HUAWEI,name)
        mainHuaweiAppGalleryApi.ClientSecret = mainAppStoreAcount.GetClientSecret(Source.HUAWEI,name) 

        # build.gradle
        filename = "build.gradle"
        file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/"+filename
        file2 = mainResource.GetRootDirAndroidStudioGame()+"/"+filename
        FileUtil.CopyFile(file1, file2)

        # gradle.properties
        filename = "gradle.properties"
        file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/"+filename
        file2 = mainResource.GetRootDirAndroidStudioGame()+"/"+filename
        FileUtil.CopyFile(file1, file2)

        # local.properties
        filename = "local.properties"
        file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/"+filename
        file2 = mainResource.GetRootDirAndroidStudioGame()+"/"+filename
        FileUtil.CopyFile(file1, file2)
        

        # launcher 
        dir1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/launcher"
        dir2 = mainResource.GetRootDirAndroidStudioLauncher()
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)

        # mipmap-hdpi mipmap-mdpi mipmap-xhdpi mipmap-xxhdpi mipmap-xxxhdpi 
        listIconDir = ["mipmap-hdpi", "mipmap-mdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"] 
        for name in listIconDir:
            dir1 = mainResource.GetProjectOutPutApp()+"/icon/android/"+name
            if isHd:
                dir1 = mainResource.GetProjectOutPutApp()+"/iconhd/android/"+name
            dir2 = mainResource.GetRootDirAndroidStudioLauncher()+"/src/main/res/"+name
            flag = os.path.exists(dir2)
            if flag:
                shutil.rmtree(dir2)
            shutil.copytree(dir1,dir2)



        # unityLibrary  build.gradle AndroidManifest.xml 
        
        if chanel==Source.GP:
            file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/unityLibrary/build_gp.gradle"
        else:
            file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/unityLibrary/build.gradle"

        file2 = mainResource.GetRootDirAndroidStudio()+"/build.gradle"
        FileUtil.CopyFile(file1, file2)
        

        filename = "AndroidManifest.xml"
        if chanel==Source.GP:
            filename = "AndroidManifest_gp.xml"

        file1 = mainResource.GetProjectConfigDefaultAndroidstudio()+"/unityLibrary/src/main/"+filename
        file2 = mainResource.GetRootDirAndroidStudio()+"/src/main/AndroidManifest.xml"
        FileUtil.CopyFile(file1, file2)


        # 修改名字  name
        strStart = "app_name\">"
        strEnd = "<"
        project_android = mainResource.GetRootDirAndroidStudioLauncher()+"/src/main/res"
        APP_NAME_CN_ANDROID =self.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_CN,chanel)
        APP_NAME_EN_ANDROID =self.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_EN,chanel)
        file_name_cn_android = project_android + "/values/strings.xml"
        file_name_en_android = project_android + "/values-en/strings.xml"
        # cn
        strfile = FileUtil.GetFileString(file_name_cn_android)
        strOut = self.replaceString(strfile, strStart, strEnd, APP_NAME_CN_ANDROID) 
        self.saveString2File(strOut, file_name_cn_android)
        # en 
        strfile = FileUtil.GetFileString(file_name_en_android)
        strOut = self.replaceString(strfile, strStart, strEnd, APP_NAME_EN_ANDROID)
        self.saveString2File(strOut, file_name_en_android)



        PACKAGE_ANDROID = self.GetAppPackage(Source.ANDROID,isHd,chanel) 
        self.versionCode =  self.GetAppVersionCode(Source.ANDROID,isHd,chanel)
        APPVERSION_ANDROID = self.versionCodeToVersion(self.versionCode)
        APPVERSION_CODE_ANDROID = self.versionCode

        print("android version:"+APPVERSION_ANDROID)

        file_AndroidManifest_launcher = mainResource.GetRootDirAndroidStudioLauncher() + "/src/main/AndroidManifest.xml"
        file_AndroidManifest_unityLibrary = mainResource.GetRootDirAndroidStudio() + "/src/main/AndroidManifest.xml"
              # if chanel==Source.GP:
        #     self.updateAndroidManifest(file_AndroidManifest_GP,file_AndroidManifest_androidstudio,PACKAGE_ANDROID,APPVERSION_ANDROID,APPVERSION_CODE_ANDROID,isHd)
        # else:
        self.updateAndroidManifest(file_AndroidManifest_launcher,file_AndroidManifest_launcher,PACKAGE_ANDROID,APPVERSION_ANDROID,APPVERSION_CODE_ANDROID,isHd)
        self.updateAndroidManifest(file_AndroidManifest_unityLibrary,file_AndroidManifest_unityLibrary,PACKAGE_ANDROID,APPVERSION_ANDROID,APPVERSION_CODE_ANDROID,isHd)
      

        file_google_service_android = mainResource.GetProjectConfigDefault() + "/android/project/config/google-services.json"
        file_google_service_android_androidstudio = mainResource.GetRootDirAndroidStudioLauncher()+"/src/main/google-services.json" 
        self.replaceGoogleServiceFile(file_google_service_android,file_google_service_android_androidstudio, PACKAGE_ANDROID)


        # xiaomi aso keyword
        data = self.loadJson(isHd)
        self.updateXiaoASOkeyword(data,isHd)


    def CopyAppInfoiOS(self,isHd,chanel=""): 
        rootConfig = mainResource.GetProjectConfigDefault()
       
        project_ios = rootConfig + "/ios/project" 
 
        APPVERSION_IOS =  self.GetAppVersion(Source.IOS,isHd)


 
        APP_NAME_CN_IOS = self.GetAppName(Source.IOS,isHd,Source.LANGUAGE_CN,chanel)
        APP_NAME_EN_IOS = self.GetAppName(Source.IOS,isHd,Source.LANGUAGE_EN,chanel)  
        
        PACKAGE_IOS = self.GetAppPackage(Source.IOS,isHd,chanel)  

        print("ios version:"+APPVERSION_IOS)

        # android

   

        # ios
        file_name_cn_ios = project_ios + "/appname/zh-Hans.lproj/InfoPlist.strings"
        file_name_en_ios = project_ios + "/appname/en.lproj/InfoPlist.strings"
        file_info_plist_ios = project_ios + "/Info.plist"


        file_name_cn_ios_xcode = mainResource.GetRootDirXcode() + "/appname/zh-Hans.lproj/InfoPlist.strings"
        file_name_en_ios_xcode = mainResource.GetRootDirXcode() + "/appname/en.lproj/InfoPlist.strings"
        file_info_plist_ios_xcode = mainResource.GetRootDirXcode() + "/Info.plist"     
    
    
        
    # ios
        if os.path.exists(file_info_plist_ios_xcode):
        # info
            strfile = FileUtil.GetFileString(file_info_plist_ios)
            strfile = strfile.replace("_APP_NAME_",APP_NAME_CN_IOS)
            strfile = strfile.replace("_APP_PACKAGE_",PACKAGE_IOS)
            strfile = strfile.replace("_APP_VERSION_",APPVERSION_IOS)
            appid = mainAdConfig.GetCommonAppId(Source.ADMOB,Source.IOS,isHd)
            strfile = strfile.replace("_APP_ID_ADMOB_",appid) 


            # CFBundleURLSchemes
            src = Source.WEIBO
            appid = mainConfig.GetShareAppId(src,Source.IOS,isHd) 
            print("ios WEIBO:"+appid) 
            strfile =self.replaceXcodeUrlScheme(strfile,src,appid,0)

            src = Source.WEIXIN
            appid = mainConfig.GetShareAppId(src,Source.IOS,isHd)
            strfile =self.replaceXcodeUrlScheme(strfile,src,appid,0)

            src = Source.QQ
            appid = mainConfig.GetShareAppId(src,Source.IOS,isHd)
            strfile =self.replaceXcodeUrlScheme(strfile,src,appid,0)
            strfile =self.replaceXcodeUrlScheme(strfile,src,appid,1)


            # Orientation

            if isHd:
                strfile = strfile.replace("_KEY_Orientation0","UIInterfaceOrientationLandscapeLeft")
                strfile = strfile.replace("_KEY_Orientation1","UIInterfaceOrientationLandscapeRight")
            else:
                strfile = strfile.replace("_KEY_Orientation0","UIInterfaceOrientationPortraitUpsideDown")
                strfile = strfile.replace("_KEY_Orientation1","UIInterfaceOrientationPortrait")
    
            FileUtil.SaveString2File(strfile,file_info_plist_ios_xcode)

            #appname

            # cn
            FileUtil.CreateDir(mainResource.GetRootDirXcode() + "/appname")
            strfile = FileUtil.GetFileString(file_name_cn_ios)  
            strfile = strfile.replace("_APP_NAME_",APP_NAME_CN_IOS)
            FileUtil.CreateDir(FileUtil.GetLastDirofDir(file_name_cn_ios_xcode))
            FileUtil.SaveString2File(strfile,file_name_cn_ios_xcode)

            # en 
            strfile = FileUtil.GetFileString(file_name_en_ios)  
            strfile = strfile.replace("_APP_NAME_",APP_NAME_EN_IOS)
            FileUtil.CreateDir(FileUtil.GetLastDirofDir(file_name_en_ios_xcode))
            FileUtil.SaveString2File(strfile,file_name_en_ios_xcode) 


            



    def CopyAppInfo(self,isHd,chanel=""):
        # 重新加载
        self.loadJson(isHd,True)

        self.CopyAppInfoAndroid(isHd,chanel)
        self.CopyAppInfoiOS(isHd,chanel)
 

    def updateName(self,isHd,isAuto,chanel=""):
        data = self.loadJson(isHd,True)

        self.AddChannelInfo(isHd,chanel)
    
        name = mainAppInfo.GetAppStoreAcount(isHd,Source.HUAWEI)
        mainHuaweiAppGalleryApi.ClientId = mainAppStoreAcount.GetClientId(Source.HUAWEI,name)
        mainHuaweiAppGalleryApi.ClientSecret = mainAppStoreAcount.GetClientSecret(Source.HUAWEI,name) 
        
        
        # appinfoOld = AppInfoOld(isHd)
        # if appinfoOld.IsOldVersion():
        #     # 转换
        #     self.ConvertOld2New(isHd,appinfoOld)
 

        # loadJson 
        APPVERSION_IOS =  self.GetAppVersion(Source.IOS, isHd,chanel) 

    
        APP_NAME_CN_ANDROID =mainAppInfo.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_CN,chanel)
        APP_NAME_EN_ANDROID = mainAppInfo.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_EN,chanel)
        APP_NAME_CN_IOS = mainAppInfo.GetAppName(Source.IOS,isHd,Source.LANGUAGE_CN,chanel)
        APP_NAME_EN_IOS = mainAppInfo.GetAppName(Source.IOS,isHd,Source.LANGUAGE_EN,chanel)  
        PACKAGE_ANDROID = mainAppInfo.GetAppPackage(Source.ANDROID,isHd,chanel) 
        PACKAGE_IOS = mainAppInfo.GetAppPackage(Source.IOS,isHd,chanel) 
        self.versionCode = self.GetAppVersionCode(Source.ANDROID, isHd,chanel)  
   
        
        #appid 
        appid_ios = self.GetJsonAppId(data,Source.APPSTORE)
        appid_taptap = self.GetJsonAppId(data,Source.TAPTAP)
        appid_huawei = self.GetJsonAppId(data,Source.HUAWEI)
        self.SetConfigDataAppId(Source.IOS,Source.APPSTORE,appid_ios,isHd)
        self.SetConfigDataAppId(Source.ANDROID,Source.TAPTAP,appid_taptap,isHd)
        self.SetConfigDataAppId(Source.ANDROID,Source.HUAWEI,appid_huawei,isHd)

        csvfile = mainResource.GetConfigDataDir()+"/language/language.csv" 
        self.UpdateLanguageName(csvfile,APP_NAME_CN_ANDROID,APP_NAME_EN_ANDROID,isHd)

        csvfile = mainResource.GetRootUnityAssetsResource()+"/ConfigData/language/language.csv" 
        self.UpdateLanguageName(csvfile,APP_NAME_CN_ANDROID,APP_NAME_EN_ANDROID,isHd)

        
        # if data.has_key("PACKAGE_HD_ANDROID"):
        #     PACKAGE_HD_ANDROID = data["PACKAGE_HD_ANDROID"]


        
    
        if isAuto==True: 
            self.autoPlusVersion(isHd,chanel)
            self.loadJson(isHd,True)
            # 重新加载 
            APPVERSION_IOS =  self.GetAppVersion(Source.IOS, isHd,chanel)
            self.versionCode =  self.GetAppVersionCode(Source.ANDROID, isHd,chanel) 

        APPVERSION_ANDROID = self.versionCodeToVersion(self.versionCode)
       

        # appversion.json
        if isAuto==False: 
            # src = mainResource.GetProjectConfigDefault()+"/appinfo/appversion.json"
            # dst = mainResource.GetProjectConfigApp()+"/appinfo/appversion.json"
            # flag = os.path.exists(dst)
            # # 
            # if not isHd:
            #     shutil.copyfile(src,dst)

            # strfile = FileUtil.GetFileString(dst)
            # key = "_VERSION_ANDROID_"
            # if isHd:
            #     key = "_VERSION_HD_ANDROID_"

            # 保存版本
            # android
 
            print("appid_huawei=",appid_huawei+" appid_taptap="+appid_taptap+" ishd=",isHd) 
            

            if chanel == Source.TAPTAP:
                version_web = mainAppVersionTapTap.ParseVersion(appid_taptap)
                print("SaveAppVersion version_web=",version_web)
                self.SaveAppVersion(isHd,Source.ANDROID,version_web,chanel)

            if chanel == Source.HUAWEI:
                version_web = mainHuaweiAppGalleryApi.GetVersion(appid_huawei)
                print("SaveAppVersion version_web=",version_web)
                self.SaveAppVersion(isHd,Source.ANDROID,version_web,chanel)

            # strfile = strfile.replace(key,version_web) 
            # FileUtil.SaveString2File(strfile,dst) 


                
                
       

            # ios
            appid_apple = self.GetJsonAppId(data,Source.APPSTORE)
            if chanel == Source.APPSTORE:
                version_web = mainAppVersionApple.ParseVersion(appid_apple)
                print("AppVersionApple=",version_web+" appid_apple=",appid_apple)
                self.SaveAppVersion(isHd,Source.IOS,version_web,chanel)

            # filepath = mainResource.GetProjectConfigAppType()+"/appversion.json" 
            # flag = os.path.exists(filepath)
            # strFileJson = "{}"
            # if flag:
            #     strFileJson = FileUtil.GetFileString(filepath)
            # dataRoot = json.loads(strFileJson)
            # dataRoot[mainResource.getGameName()]= json.loads(strfile)
            # JsonUtil.SaveJson(filepath,dataRoot)


            

        # 重新加载 
        self.loadJson(isHd,True)
        APPVERSION_IOS = self.GetAppVersion(Source.IOS, isHd,chanel)
        self.versionCode = self.GetAppVersionCode(Source.IOS, isHd,chanel) 
        APPVERSION_ANDROID = self.versionCodeToVersion(self.versionCode)
        APPVERSION_CODE_ANDROID = self.versionCode

        print (APP_NAME_CN_ANDROID)
        print (APP_NAME_EN_ANDROID)
        print (APP_NAME_CN_IOS)
        print (APP_NAME_EN_IOS)
        print (PACKAGE_ANDROID)

        print("android version:"+APPVERSION_ANDROID)
        print("ios version:"+APPVERSION_IOS)

  
    # win
        # self.updateNameWin(isHd,isAuto)


    def updateNameWin(self,isHd,isAuto):
        strOld = "_APP_NAME_"
        rootConfig = mainResource.GetProjectConfigApp()
        project = rootConfig + "/win/project"
        # if isHd:
        #     project = rootConfig + "/win/project_hd"

        file_name_cn = project + "/strings/zh-cn/resources.resw"
        file_name_en= project + "/strings/en-us/resources.resw"

        data = self.loadJson(isHd)
        isOld = self.IsOldVersion(data)
        
        if not isOld : 
            appname = data["appname"]

        if isOld:
            APP_NAME_CN= data["APP_NAME_CN_ANDROID"]
            APP_NAME_EN = data["APP_NAME_EN_ANDROID"]
            PACKAGE = data["PACKAGE_ANDROID"]
        else:
            APP_NAME_CN = appname["android"]["cn"]
            APP_NAME_EN = appname["android"]["en"]
            PACKAGE = data["apppackage"]["android"]["default"]
    
        # cn
        self.replaceFile(file_name_cn, strOld, APP_NAME_CN)
        # en
        self.replaceFile(file_name_en, strOld, APP_NAME_EN)

        
    
        filepath= project + "/strings/mainResource.resw"
        if os.path.exists(filepath):
            self.replaceFile(filepath, "_APP_PACKAGE_", PACKAGE)
    
        # # <Identity Name="47113moonma.KidsShapeColor"
        # strStart = "<Identity Name=\""
        # strEnd = "\""
        # filepath= mainResource.GetRootProjectWin()+"/"+ mainResource.GetProjectName()+ "/Package.appxmanifest"
        # strOut = replaceStringOfFile(file, strStart, strEnd, PACKAGE)
        # saveString2File(strOut, file)
 

    def Copy(self,isHd,channel=""):  
        # self.CopyAppInfo(False,channel)
        self.CopyAppInfo(isHd,channel)


    def AddChannelInfo(self,isHd,channel):  
        if len(channel)==0:
            return
        jsonfile = self.GetJsonFile(isHd)
        data = self.loadJson(isHd,False)
        appversion = data["appversion"] 
        print("AddChannelInfo  channel=",channel)
        if channel in appversion: 
            return

        # do add
    #        "ios": {
    #     "code": "103",
    #     "value": "1.0.3"
    # }
        item= json.loads("{}")
        item["code"]="100"
        item["value"]="1.0.0"
        appversion[channel] =item
        
        JsonUtil.SaveJson(jsonfile,data)
        data = self.loadJson(isHd,True)


    # 主函数的实现
    def Run(self,is_auto_plus_version,channel=""):  
        
    #先从default 拷贝 工程文件模版
        # ios project file
        # self.copyResFiles(Source.IOS)
        # # android project file
        # self.copyResFiles(Source.ANDROID)
        # # win 
        # self.copyResFiles(Source.WIN)
    
        # rename
        src = mainResource.GetProjectConfigApp()+"/appname"
        dst = mainResource.GetProjectConfigApp()+"/appinfo"
        flag = os.path.exists(src)
        if flag:
            os.rename(src,dst)

        src = mainResource.GetProjectConfigApp()+"/appinfo/appname.json"
        dst = mainResource.GetProjectConfigApp()+"/appinfo/appinfo.json"
        flag = os.path.exists(src)
        if flag:
            os.rename(src,dst)

        src = mainResource.GetProjectConfigApp()+"/appinfo/appname_hd.json"
        dst = mainResource.GetProjectConfigApp()+"/appinfo/appinfo_hd.json"
        flag = os.path.exists(src)
        if flag:
            os.rename(src,dst)

        

        # channel = ""
        # channel = Source.HUAWEI
        self.updateName(False,is_auto_plus_version,Source.HUAWEI)
        self.updateName(True,is_auto_plus_version,Source.HUAWEI)

        self.updateName(False,is_auto_plus_version,Source.TAPTAP)
        self.updateName(True,is_auto_plus_version,Source.TAPTAP)   


        self.updateName(False,is_auto_plus_version,Source.APPSTORE)
        self.updateName(True,is_auto_plus_version,Source.APPSTORE)   

        print("appname sucess")

mainAppInfo = AppInfo()
