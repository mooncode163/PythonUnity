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
import xml.etree.ElementTree as ET  
#include common.py
sys.path.append('../../') 
sys.path.append('./')  
from Config.Config import mainConfig
from Common import Source
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
from AppStore.AppstoreUploadiOS import mainAppstoreUploadiOS

DEVICE_IPADPRO = "ipadpro"
DEVICE_IPADPRO_2018 = "ipadpro"
DEVICE_IPHONE_6_5 = "iphone_6_5"
DEVICE_IPHONE_5_5 = "iphone"

list_language = ["cn", "en"] 
listCountry = ["en-US", "zh-Hans","en-CA","en-AU","en-GB"]  
listCountryLanguage = ["en", "cn","en","en","en"] 


totalScreenshot = 5 
# "Mac", "appletvos", "iOS-3.5-in", "iOS-4-in", "iOS-4.7-in", "iOS-5.5-in", "iOS-5.8-in", "iOS-Apple-Watch", "iOS-iPad", "iOS-iPad-Pro" or "iOS-iPad-Pro-10.5-in"

list_device = [DEVICE_IPHONE_5_5,DEVICE_IPADPRO]
#list_device = [DEVICE_IPADPRO, DEVICE_IPHONE_6_5,DEVICE_IPHONE_5_5]
gameName = " "
gameType = " "
enableScrenshot = False
class UpdateAppstore(): 
    def loadJson(self,isHd):
        cur_path = mainResource.GetProjectConfigApp()+"/appinfo"
        jsonfile = cur_path+'/appinfo.json'
        if isHd:
            jsonfile = cur_path+'/appinfo_hd.json'

        with open(jsonfile) as json_file:
            data = json.load(json_file)
            return data

    def loadXmlDescription(self,isHd):
        cur_path = mainResource.GetProjectConfigApp()+"/appinfo"
        xmlfile = cur_path+'/app_description.xml'
        if isHd:
            xmlfile = cur_path+'/app_description_hd.xml'

        tree = ET.parse(xmlfile)  
        root = tree.getroot()  

        # cn = root.find('en')
        # print cn.tag
        # print cn.text

        return root

    def getXmlDescriptionText(self,root,key):
        for child in root.findall(key): 
            return child.text
        # return root.find(key).text

    def replaceIAP_noad(self,filePath,strReplace):
        f = open(filePath, 'r')
        strContent = f.read() 
        
        strStart = "<in_app_purchase>"
        idx = strContent.find(strStart)
        strHead = strContent[0:idx] + strStart

        idx = idx + len(strStart)
        strOther = strContent[idx:]
        
        strMid = "<product_id>"
        idx = strOther.find(strMid)
        strHead2 = strOther[0:idx] + strMid
        strHead += strHead2

        strEnd = "</product_id>"
        idx = strOther.find(strEnd)
        strOther = strOther[idx:] 
        strRet = strHead + strReplace + strOther

        f.close()
        self.saveString2File(strRet,filePath) 


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


    def replaceString2(self,strContent, strStart, strMid, strEnd, strReplace):
        idx = strContent.find(strStart)
        strHead = strContent[0:idx] + strStart

        idx = idx + len(strStart)
        strOther = strContent[idx:]
        # print "strOther1:"+strOther
        idx = strOther.find(strMid)
        strHead2 = strOther[0:idx] + strMid
        strHead += strHead2

        idx = strOther.find(strEnd)
        strOther = strOther[idx:]
        # print "strOther2:"+strOther
        strRet = strHead + strReplace + strOther
        return strRet


    def replaceStringOfFile2(self,filePath, strStart, strMid, strEnd, strReplace):
        f = open(filePath, 'r')
        strFile = f.read()
        # print strFile
        strOut = self.replaceString2(strFile, strStart, strMid, strEnd, strReplace)
        # print strOut
        # fp_name.seek(0)
        # fp_name.write(strOut)
        f.close()
        return strOut
 
    def saveString2File(self,str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8',"ignore")
        f.write(b)
        f.close()

    def replaceXmlKey(self,filepath,language,key,title):
    
        strStart = language
        # <keyword>
        strMid = "<"+key+">" 
        # </keyword>
        strEnd = "</"+key+">" 
        strOut = self.replaceStringOfFile2(
            filepath, strStart, strMid, strEnd, title)
        self.saveString2File(strOut, filepath)
    # <software_screenshots></software_screenshots>
    # <!-- <software_screenshots></software_screenshots> -->
    # 注释xmlkey
    def disableXmlKey(self,filePath,key):
        strFrom = "<"+key+">"+"</"+key+">"
        strTo = "<!-- <"+key+">"+"</"+key+"> -->"
        strFile = FileUtil.GetFileString(filePath)
        strFile = strFile.replace(strFrom,strTo)
        self.saveString2File(strFile,filePath)
    
    def getScreenshotFileName(self,device,language,idx): 
        return language+"_"+device+"_"+str(idx+1)+".jpg";

    def getScreenshotFullFilePath(self,isHd,device,language,idx): 
        strDir_itmsp = "app.itmsp"
        if isHd:
            strDir_itmsp = "app_pad.itmsp"
        strDirRootTo = mainResource.GetProjectConfigApp()+"/appstore/ios/"+strDir_itmsp
        strFileTo = strDirRootTo+"/"+self.getScreenshotFileName(device,language,idx)
        return strFileTo

    def copy_or_delete_one_screenshot(self,isHd,device,language,idx,isDel):
        strDirHorV = "shu"
        if isHd:
            strDirHorV = "heng" 

        strDirRootFrom =mainResource.GetProjectOutPutApp()+"/screenshot"
        strFileFrom = strDirRootFrom+"/"+strDirHorV+"/"+language+"/"+device+"/"+str(idx+1)+".jpg";
    
        strFileTo = self.getScreenshotFullFilePath(isHd,device,language,idx)

        if isDel:
            if os.path.isfile(strFileTo):
                os.remove(strFileTo)
        else:
            # print strFileFrom
            if os.path.isfile(strFileFrom):
                shutil.copyfile(strFileFrom,strFileTo)

    def copy_screenshots(self): 
        list_hd = [False, True]
        
        for device in list_device:
            print ("copy_screenshots device="+device)
            for language in list_language:
                for ishd in list_hd:
                    for i in range(0, totalScreenshot):
                        self.copy_or_delete_one_screenshot(ishd,device,language,i,False) 


    def delete_screenshots(self): 
        list_hd = [False, True]
        
        for device in list_device:
            for language in list_language:
                for ishd in list_hd:
                    for i in range(0, totalScreenshot):
                        self.copy_or_delete_one_screenshot(ishd,device,language,i,True) 

    # /*
    # <software_screenshot display_target="iOS-5.5-in" position="1">
    #                                   <file_name>iphone_1.jpg</file_name>
    #                                   <size>263616</size>
    #                                   <checksum type="md5">dc695d677a5c33392bc88ba4eb9d719f</checksum>
    #                                </software_screenshot> 
    #                                */
    def getXmlStringOneScreenshot(isHd,device,language,idx):  
        filePath = self.getScreenshotFullFilePath(isHd,device,language,idx)
        strRet = " " 
        if enableScrenshot:
            strRet = "<software_screenshot display_target=\""+getAppStoreScreenshotDeviceName(device)+"\" position=\""+str(idx+1)+"\"> <file_name>"+getScreenshotFileName(device,language,idx)+"</file_name> <size>"+str(mainResource.get_FileSize(filePath))+"</size> <checksum type=\"md5\">"+mainResource.get_MD5_checksum_file(filePath)+"</checksum> </software_screenshot>"       
        return strRet

    def getXmlStringScreenshots(self,isHd,language):
        
        strRet = " "
        for device in list_device:
            for i in range(0, totalScreenshot):
                strFileTo = self.getScreenshotFullFilePath(isHd,device,language,i)
                if os.path.isfile(strFileTo):
                    strRet+="\n"+getXmlStringOneScreenshot(isHd,device,language,i)
        return strRet

    def getAppStoreScreenshotDeviceName(self,device):
        strRet = device
        if device==DEVICE_IPADPRO:
            strRet = "iOS-iPad-Pro"
        if device==DEVICE_IPHONE_5_5:
            strRet = "iOS-5.5-in"
        if device==DEVICE_IPHONE_6_5:
            strRet = "iOS-6.5-in"
            
        return strRet

    def DeleteInAppPurchasesScreenshot(self,isHd):    
        rootConfig = mainResource.GetProjectConfigApp() 
        dst = rootConfig + "/appstore/ios/app.itmsp" 
        if isHd:
            dst = rootConfig + "/appstore/ios/app_pad.itmsp"  
        filepath =dst+"/in_app_purchases_screenshot.png"
        
        if os.path.exists(filepath):
            os.remove(filepath)


    def CopyInAppPurchasesScreenshot(self,isHd):   
        # src =mainResource.GetProjectConfig() + "/default/appstore/in_app_purchases_screenshot.png"
        src =mainResource.GetDirProductCommon() + "/in_app_purchases_screenshot.png"
        rootConfig = mainResource.GetProjectConfigApp() 
        dst = rootConfig + "/appstore/ios/app.itmsp" 
        if isHd:
            dst = rootConfig + "/appstore/ios/app_pad.itmsp"  
        dst =dst+"/in_app_purchases_screenshot.png"
        
        if not os.path.isfile(dst):
            shutil.copyfile(src,dst)

    def IsOldVersion(self,data):
        isOld = True
        if ("appname" in data) :
            isOld = False  

        return isOld


    def LoadJsonIAP(self,isHD,stros):  

        if stros==Source.ANDROID:
            jsonfile = mainResource.GetConfigDataDir()+"/IAP/IAP_android.json"  
            if isHD:
                jsonfile = mainResource.GetConfigDataDir()+"/IAP/IAP_android_hd.json"  

        if stros==Source.IOS:  
            jsonfile = mainResource.GetConfigDataDir()+"/IAP/IAP_ios.json"  
            if isHD:
                jsonfile = mainResource.GetConfigDataDir()+"/IAP/IAP_ios_hd.json"  

        jsonfile = os.path.normpath(jsonfile)
        strfile = FileUtil.GetFileString(jsonfile)
        return json.loads(strfile) 
 

    def DeleteAllScreenshots(self,isHd): 
        verison = mainAppInfo.GetAppVersion(Source.IOS,isHd) 
        
        rootConfig = mainResource.GetProjectConfigDefault()  
        str_metadata_xml = FileUtil.GetFileString(rootConfig + "/appstore/metadata_clear_screenshots.xml")
        str_metadata_xml=str_metadata_xml.replace("_VENDOR_ID_",mainAppInfo.GetAppSKU(isHd))
        str_metadata_xml=str_metadata_xml.replace("_VERSION_",verison)
  
        rootConfig = mainResource.GetProjectConfigApp()
        file_metadata_ios = rootConfig + "/appstore/ios/app.itmsp/metadata.xml" 
        if isHd:
            file_metadata_ios = rootConfig + "/appstore/ios/app_pad.itmsp/metadata.xml" 
        
        FileUtil.SaveString2File(str_metadata_xml,file_metadata_ios)
        mainAppstoreUploadiOS.Run(isHd)

    def UpdateIAPInfo(self,isHd):
        self.CopyInAppPurchasesScreenshot(isHd)
        self.UploadIAPInfo(isHd,Source.IOS)
        self.DeleteInAppPurchasesScreenshot(isHd)
        

    def UploadIAPInfo(self,isHd,stros):
        package = mainAppInfo.GetAppPackage(stros,isHd)
        rootJson = self.LoadJsonIAP(isHd,stros)
        rootConfig = mainResource.GetProjectConfigDefault() 
        striap = FileUtil.GetFileString(rootConfig + "/appstore/KEY_IAP.xml")
         
        listIAP =[] 
        for item in rootJson["items"]:
            if item["isSkip"]:
                continue

            name = item["key"]
            striap=striap.replace("_NAME_",name)
            product_id = package+"."+item["id"]
            striap=striap.replace("_ID_",product_id)

            # consumable non-consumable
            isConsume = item["isConsume"] 
            product_type = "non-consumable"
            if isConsume:
                product_type = "consumable"

            striap=striap.replace("_TYPE_",product_type)
            

            title_cn = item["title"]["cn"]
            striap=striap.replace("_TITLE_CN_",title_cn)
            title_en = item["title"]["en"]
            striap=striap.replace("_TITLE_EN_",title_en)

            title_cn = item["detail"]["cn"]
            striap=striap.replace("_DETAIL_CN_",title_cn)
            title_en = item["detail"]["en"]
            striap=striap.replace("_DETAIL_EN_",title_en)
            
            price = item["price_tier"]
            striap=striap.replace("_PRICE_",price)

            listIAP.append(striap)

        str_metadata_xml = FileUtil.GetFileString(rootConfig + "/appstore/IAP_metadata.xml")
        str_metadata_xml=str_metadata_xml.replace("_VENDOR_ID_",mainAppInfo.GetAppSKU(isHd))
        strkeyiap = ""
        for strtmp in listIAP:
            strkeyiap+=strtmp

        str_metadata_xml=str_metadata_xml.replace("_KEY_IAP_",strkeyiap)


        rootConfig = mainResource.GetProjectConfigApp()
        file_metadata_ios = rootConfig + "/appstore/ios/app.itmsp/metadata.xml" 
        if isHd:
            file_metadata_ios = rootConfig + "/appstore/ios/app_pad.itmsp/metadata.xml" 
        
        FileUtil.SaveString2File(str_metadata_xml,file_metadata_ios)
        mainAppstoreUploadiOS.Run(isHd) 

        

    def updateAppstore(self,isHd):
        
        self.CopyInAppPurchasesScreenshot(isHd)

        rootConfig = mainResource.GetProjectConfigApp()
        strHD = "HD"

        metadata_ios = rootConfig + "/appstore/ios/app.itmsp/metadata.xml" 

        if isHd:
            metadata_ios = rootConfig + "/appstore/ios/app_pad.itmsp/metadata.xml" 

        xmlRoot = self.loadXmlDescription(isHd) 

        # filePath = rootConfig + "appstore/ios/app.itmsp/in_app_purchases_screenshot.png" 
        # print mainResource.get_MD5_checksum_file(filePath)

        # loadJson
        data = self.loadJson(isHd)

        isOld = self.IsOldVersion(data)
        if isOld:
            # APP_NAME_CN_ANDROID = data["APP_NAME_CN_ANDROID"]
            APPSTORE_VERSION_UPDATE = data["APPSTORE_VERSION_UPDATE"]
            APPSTORE_TITLE = data["APPSTORE_TITLE"]
            APPSTORE_SUBTITLE = data["APPSTORE_SUBTITLE"]
            APPSTORE_PROMOTION = data["APPSTORE_PROMOTION"]
            PACKAGE = data["PACKAGE_IOS"]
            # APPSTORE_DESCRIPTION = data["APPSTORE_DESCRIPTION"]
            APPSTORE_KEYWORD = data["APPSTORE_KEYWORD"]
            APPVERSION_IOS = data["APPVERSION_IOS"]
        else:
            APPVERSION_IOS =  data["appversion"][Source.IOS]["value"]
            APPSTORE_KEYWORD =  data["appstore"]["aso"]
            PACKAGE = data["apppackage"][Source.IOS]["default"]
            APPSTORE_VERSION_UPDATE = data["appstore"]["version_update"]
            APPSTORE_PROMOTION =  data["appstore"]["promotion"]
            APPSTORE_SUBTITLE = data["appstore"]["subtitle"]
            APPSTORE_TITLE = data["appstore"]["title"]

        software_url = data["software_url"]
        privacy_url = data["privacy_url"]
        support_url = data["support_url"]
        sku_app = data["sku_app"]
        # need_upload_screenshot = data.get("need_upload_screenshot",False)
        need_upload_screenshot = False
        global enableScrenshot
        enableScrenshot = False 
    
    # ios
    #     sku_app
        strStart = "<vendor_id>"
        strEnd = "</vendor_id>"
        
        strOut = self.replaceStringOfFile(
            metadata_ios, strStart, strEnd, sku_app)
        self.saveString2File(strOut, metadata_ios)
        
        print("APPVERSION_IOS=",APPVERSION_IOS)
        # APPVERSION_IOS
        # <version string="1.0.0">
        strStart = "<version string=\""
        strEnd = "\">"
        strOut = self.replaceStringOfFile(
            metadata_ios, strStart, strEnd, APPVERSION_IOS)
        self.saveString2File(strOut, metadata_ios)
    
        # 版本更新说明 
        key = "version_whats_new"
        if APPVERSION_IOS=="1.0.0": 
            self.disableXmlKey(metadata_ios,key)
        else:
            jsonData = APPSTORE_VERSION_UPDATE
            idx = 0
            for country in listCountry:
                lan = listCountryLanguage[idx]
                self.replaceXmlKey(metadata_ios,country,key,jsonData[lan])
                idx += 1


        # APPSTORE_TITLE
        key = "title"
        jsonData = APPSTORE_TITLE
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData[lan])
            idx += 1

    
        # APPSTORE_TITLE
        key = "subtitle"
        jsonData = APPSTORE_SUBTITLE
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData[lan])
            idx += 1
    
    # APPSTORE_PROMOTION
        key = "promotional_text"
        jsonData = APPSTORE_PROMOTION
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData[lan])
            idx += 1

        # APPSTORE_DESCRIPTION
        key = "description"
        # jsonData = APPSTORE_DESCRIPTION 
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            desc = self.getXmlDescriptionText(xmlRoot,lan)
            self.replaceXmlKey(metadata_ios,country,key,desc)
            idx += 1

    
        # APPSTORE_KEYWORD
        key = "keyword"
        jsonData = APPSTORE_KEYWORD
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData[lan])
            idx += 1
    
        # software_url
        key = "software_url"
        jsonData = software_url
        idx = 0
        for country in listCountry: 
            self.replaceXmlKey(metadata_ios,country,key,jsonData)
            idx += 1

        # support_url
        key = "support_url"
        jsonData = support_url
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData)
            idx += 1

        # privacy_url
        key = "privacy_url"
        jsonData = privacy_url
        idx = 0
        for country in listCountry:
            lan = listCountryLanguage[idx]
            self.replaceXmlKey(metadata_ios,country,key,jsonData)
            idx += 1

    # screenshot
        # key = "software_screenshots" 
        # if enableScrenshot:
        #     screenshot_cn = self.getXmlStringScreenshots(isHd,"cn")
        #     screenshot_en = self.getXmlStringScreenshots(isHd,"en")
        #     self.replaceXmlKey(metadata_ios,"en-US",key,screenshot_en)
        #     self.replaceXmlKey(metadata_ios,"zh-Hans",key,screenshot_cn)
        #     # replaceXmlKey(metadata_ios,"en-CA",key,screenshot_en)
        #     # replaceXmlKey(metadata_ios,"en-AU",key,screenshot_en)
        #     # replaceXmlKey(metadata_ios,"en-GB",key,screenshot_en) 
        # else:
        #     self.disableXmlKey(metadata_ios,"software_screenshots")


    # noad
        self.replaceIAP_noad(metadata_ios,PACKAGE+".noad")
        # replaceIAP_noad(metadata_ios,"noad")

# 主函数的实现
    def Run(self,isHd):
        print ("UpdateAppstore Run")
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
    
        print (gameName)
        print (gameType)

        if len(sys.argv)>2:
            if sys.argv[2] == "delete_screenshot":
                # delete_screenshots()
                sys.exit(0)   


        #先从default 拷贝 文件模版
        dir_default = mainResource.GetProjectConfigDefault()
        dir_to = mainResource.GetProjectConfigApp()
        dir1 = dir_default+"/appstore"
        dir2 = dir_to + "/appstore"
        flag = os.path.exists(dir2)
        print ("UpdateAppstore dir1="+dir1+"dir2="+dir2)
        if flag:
            shutil.rmtree(dir2)

        shutil.copytree(dir1,dir2)

        # self.copy_screenshots()
        

        self.updateAppstore(isHd)
        # self.updateAppstore(True)

        print ("UpdateAppstore sucess")

mainUpdateAppstore = UpdateAppstore()
