# 导入selenium的浏览器驱动接口


import datetime
from Common.File.FileUtil import FileUtil 
# pip3 install connectcli
# from connectapi import ConnectApi

import gzip
import requests
import platform 
if 'Darwin' not in platform.system():
    import jwt
from Project.Resource import mainResource 
import time
import sqlite3 
import sys
import os
import json 
import base64
from AppStore.UploadAssetApple import mainUploadAssetApple 


o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径


# pip3 install pyjwt
# pip3 install cryptography


# pip3 install connectcli --default-timeout=1000
# https://github.com/hepburnv/connectcli
# https://github.com/Jaykie/connectcli


# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项

# api docs https://developer.apple.com/cn/app-store-connect/api/

# pip3 install pywin32

# sys.path.append('../common')

# connectcli -k MVG9NGFVX7 -i 69a6de89-f844-47e3-e053-5b8c7c11a4d1 devices
# connectcli -k MVG9NGFVX7 -i 69a6de89-f844-47e3-e053-5b8c7c11a4d1 createprofile -n fillcoloanimal -b 249GXC99SV  -c 3K9293L64L  -t IOS_APP_STORE
class AppConnectApi:
    # api: None
    # moon key 访问类型	App 管理
    API_KEY_ID = ""
    API_USER_ID = ""
    teamID = ""
    KeyToken =  ""

    # Apple Distribution: YuanFang Chen 发布证书 
    # Certificate.json 调用ListAllCertificates 获取
    CertificateID = '24BC8G8FMA'

    # hellen
    # API_KEY_ID = "XS8PLC2XUG" 
    # API_USER_ID = "69a6de87-8bec-47e3-e053-5b8c7c11a4d1"  
    # teamID = "W3MTRE96VL"
    # CertificateID = '4X3N45JD59'


    DIR_HOME = "C:\Home"
    DIR_private_key = "C:\Home\.private_keys" 
    base_api = 'https://api.appstoreconnect.apple.com/v1/'
    
    fileScreenshot = "F:\\sourcecode\\unity\\product\\Common\\PythonUnity\\ProjectConfig\\Script\\1.jpg"
    # 设备
    # connect_api_devices = base_api+'devices',

    # # 包名
    # connect_api_bundle_ids = base_api+'bundleIds',

    # #证书
    # connect_api_certificates = base_api+'certificates',

    # app store versions
    connect_api_app_versions = "https://api.appstoreconnect.apple.com/v1/appStoreVersions"

    # provision file
    # connect_api_profiles = base_api+'profiles',

    # # 财务报告
    # connect_api_financeReports = base_api+'financeReports'

    # # apps
    # connect_api_apps = base_api + 'apps'

    # 构造函数
    def __init__(self):

        dir = self.DIR_private_key
        dir = os.path.normpath(dir)
        if os.path.exists(dir) == False:
            os.mkdir(dir)

        filename = "AuthKey_"+self.API_KEY_ID+".p8"

        dir = os.getcwd()
        src = dir+"/AppStore/"+filename
        src = os.path.normpath(src)

        dst = self.DIR_private_key+"/"+filename
        dst = os.path.normpath(dst)
        FileUtil.CopyFile(src, dst)

        # self.api = ConnectApi(self.API_KEY_ID, self.API_USER_ID)

 
 

    def GetKEY_PRIVATE(self):
        dir = os.getcwd()
        filepath = dir+"/AppStore/AuthKey_"+self.API_KEY_ID+".p8"
        filepath = os.path.normpath(filepath)
        # print(filepath)
        KEY_PRIVATE = FileUtil.GetFileString(filepath)
        return KEY_PRIVATE



    def GetUrl(self, url): 
        r = requests.get(url)
        return r.content.decode('utf-8',"ignore")

    def GetTokenByWeb(self, key_id, user_id,key_private): 
        key_private =  self.GetKEY_PRIVATE()
        url = "http://47.242.56.146:5000/AppleJWTToken?keyid="+key_id+"&userid="+user_id+"&KEY_PRIVATE="+key_private
        # print("url=",url)
        result = self.GetUrl(url)
        # print("result=",result)
        return result

    def GetToken(self): 
        return self.CreateJWTToken(self.API_KEY_ID,self.API_USER_ID)

    def CreateJWTToken(self, keyid, userid):
        KEY_PRIVATE = self.GetKEY_PRIVATE()

        # if len(self.KeyToken)==0:
        self.KeyToken = self.GetTokenByWeb(keyid,userid,KEY_PRIVATE)
        
        return self.KeyToken
 
        # 构造header

        # headers = {
        # 'typ': 'jwt',
        # 'alg': 'HS256'
        # }

        headers = {
            "alg": "ES256",
            # "kid": "MVG9NGFVX7",
            "kid": keyid,
            "typ": "JWT"
        }

        # 构造payload
        # payload = {
        # 'user_id': 1, # 自定义用户ID
        # 'username': 'pig',
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
        # }

        now_timestamp = int(time.time())+60*10
        # print(str(now_timestamp))

        payload = {
            # "iss": "69a6de89-f844-47e3-e053-5b8c7c11a4d1",
            "iss": userid,
            # 1528408800

            "exp": now_timestamp,
            "aud": "appstoreconnect-v1"
        }
        # print(payload)
        
        # print(KEY_PRIVATE)
        result = "result"
        result = jwt.encode(payload=payload, key=KEY_PRIVATE,
                            algorithm='ES256', headers=headers).decode('utf8')
        # print("CreateJWTToken =",result)
        return result

    def GetApiUrlHead(self):
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        header = {
            # 'Content-Type': 'application/json',
            # 'Authorization': 'Bearer %s'%str(token, encoding='utf-8')
            # 'Authorization': strauthor
            'Authorization': 'Bearer %s' % token
            # 指定JWT
        }
        return header



    def SaveData2Json(self, data, savepath):
        json_str = json.dumps(data, ensure_ascii=False,
                              indent=4, sort_keys=True)
        FileUtil.SaveString2File(json_str, savepath)

    def GetBundleIdByPackage(self, package):
        result = self.GetBundleIdOfPackage(package)
        if len(result)==0:
            return self.CreateBundleID(package)

        return result
        # jsonRoot = json.loads(result)
        # list = jsonRoot["data"]
        # for data in list:
        #     if data["attributes"]["identifier"] == package:
        #         return data["id"]
 
        # return self.CreateBundleID(package) 

    def ReadAppAllVersion(self, app_id):
        header = self.GetApiUrlHead() 
        # url = "https://api.appstoreconnect.apple.com/v1/appStoreVersions/"+app_id
        url = "https://api.appstoreconnect.apple.com/v1/apps/"+app_id+"/appStoreVersions"
        # print(header) 

        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        ) 
        # print(mdl_rqt.content.decode("utf-8"))
        return mdl_rqt.content.decode("utf-8")

    def GetAppCurentSubmitVersionId(self, app_id):
        strret = self.ReadAppAllVersion(app_id)
        jsonRoot = json.loads(strret)
        id = jsonRoot["data"][0]["id"]
        return id

# Read App Store Version Information
# https://api.appstoreconnect.apple.com/v1/appStoreVersions/{id}
    def ReadAppVersionInfo(self, id):
        header = self.GetApiUrlHead()
        id = "fe097c65-e7f2-4092-84b7-8f3060837545"
        url = "https://api.appstoreconnect.apple.com/v1/appStoreVersions/"+id
        # url = "https://api.appstoreconnect.apple.com/v1/apps/"+app_id+"/appStoreVersions"
        print(header) 

        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        ) 
        print(mdl_rqt.content.decode("utf-8"))


    def GetAppInfoLocalizationsUrl(self, app_id):
        header = self.GetApiUrlHead()  
        url = "https://api.appstoreconnect.apple.com/v1/apps/"+app_id+"/appInfos" 
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        ) 
        strret = mdl_rqt.content.decode("utf-8")
        # print("GetAppInfoLocalizationsUrl=",strret)
        jsonRoot = json.loads(strret)
        return jsonRoot["data"][0]["relationships"]["appInfoLocalizations"]["links"] ["related"]

    def GetAppInfoLocalizationsID(self, app_id,lan): 
        header = self.GetApiUrlHead()  
        url = self.GetAppInfoLocalizationsUrl(app_id)
        # url = "https://api.appstoreconnect.apple.com/v1/appInfos/b01d1adb-22c0-4186-94d7-9d70cd0785c2/appInfoLocalizations"
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        ) 
        strret = mdl_rqt.content.decode("utf-8") 
        jsonRoot = json.loads(strret)
        # print("GetAppInfoLocalizationsID=",strret)
        for data in jsonRoot["data"]:
            if data["attributes"]["locale"]==lan:
                return data["id"] 

        return ""

# https://developer.apple.com/documentation/appstoreconnectapi/app_metadata/app_info_localizations
# https://developer.apple.com/documentation/appstoreconnectapi/modify_an_app_info_localization
    def UpdateAppName(self, appid,version,lan,name,policyText,policyUrl,subtitle): 
        # applocalization_id = mainUploadAssetApple.GetAppLocalizationId(appid,"IOS",version,lan)
        appInfoLocalizations_id = self.GetAppInfoLocalizationsID(appid,lan)
        print("UpdateAppName appInfoLocalizations_id=",appInfoLocalizations_id)
        url = "https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/"+appInfoLocalizations_id
        header = self.GetApiUrlHead()  
         
        attributes = {       
            "name":name,
            # "privacyPolicyText": policyText,
            "privacyPolicyUrl":policyUrl,
            "subtitle": subtitle, 
        } 
 
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        auth_header = 'Bearer %s' % token
        mainUploadAssetApple.make_http_request(
            "PATCH",
            f"https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/{appInfoLocalizations_id}",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({ 
                "data": {
                    "attributes":attributes,
                    "id": appInfoLocalizations_id,
                    "type": "appInfoLocalizations"
            }
            })
        )    


    def UpdateAppInfo(self, appid,version,lan,description,keywords,marketingUrl,promotionalText,supportUrl,whatsNew): 
        print("UpdateAppInfo GetAppLocalization  appid=",appid)
        applocalization_id = mainUploadAssetApple.GetAppLocalizationId(appid,"IOS",version,lan)
        print("applocalization_id=",applocalization_id)
        url = "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/"+applocalization_id
        header = self.GetApiUrlHead()  
        # print(header)  
        params = {
            "data": {
                "attributes": {   
                    "description":description,
                    "keywords": keywords,
                    "marketingUrl":marketingUrl,
                    "promotionalText": promotionalText,
                    "supportUrl": supportUrl,
                    "whatsNew": whatsNew
                },
                
                    "id": applocalization_id,
                    "type": "appStoreVersionLocalizations"
            }
        }
        # print(params)
        json_str = json.dumps(params) 
        print(json_str)
     
        # mdl_rqt = requests.patch(
        #     url,
        #     json=json_str,
        #     headers=header,
        #     timeout=3000
        # )
        # print(mdl_rqt.content.decode("utf-8"))
        
        attributes = {       
            "description":description,
            "keywords": keywords,
            "marketingUrl":marketingUrl,
            "promotionalText": promotionalText,
            "supportUrl": supportUrl 
        }
        if version !="1.0.0":
            attributes["whatsNew"]=whatsNew
 
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        auth_header = 'Bearer %s' % token
        mainUploadAssetApple.make_http_request(
            "PATCH",
            f"https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{applocalization_id}",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({ 
                "data": {
                "attributes":attributes,
                    "id": applocalization_id,
                    "type": "appStoreVersionLocalizations"
            }
            })
        )    

         

    def CreateNewVersion(self, appid, version, package):
        # bundleid = self.GetBundleIdByPackage(package)
        build = None
        print(" appid=", appid, " version=", version, " package=", package)

        result = self.api.list_bundle_ids()
        # print(result)
        self.SaveData2Json(result,"Bundle_id.json")

        # self.CreateBundleID(package)
        # return
        
        # result = self.api.create_app_version(app_id=appid, version_string=version, platform='IOS',  release_type='AFTER_APPROVAL', copyright='moonma', build_id=build, earliest_release_date=None, uses_idfa=True)
        # result = self.create_app_version(self.connect_api_app_versions, appid, version, 'IOS',  'AFTER_APPROVAL', 'moonma', build, None, True)
        # bundleid = self.GetBundleIdByPackage(package)
        # print(" bundleid=",bundleid)
        # idversion = self.GetAppCurentSubmitVersionId(appid)

        # # en-US zh-Hans
        # # result = self.CreateAppLocalization(idversion,"en-US")
        # localization_id = self.GetAppLocalization(idversion,"zh-Hans")
        # print(" localization_id=",localization_id)
        
        # scset_id = self.GetScreenshotSet(localization_id,"APP_IPHONE_65")
        # print(" scset_id=",scset_id)
        # result = self.CreateScreenshotSet(localization_id,"APP_IPHONE_65")
        #  "id" : "0a6b8b75-4ec8-4957-a39e-b0ceafbe53d1",

        for i in range(5):
            # scid  = self.CreateScreenshot(scset_id,i)
            mainUploadAssetApple.UploadScreenShot(appid, "IOS", version, "zh-Hans", "APP_IPHONE_65", "1.jpg")

        # result = self.ReadScreenshotSet("0a6b8b75-4ec8-4957-a39e-b0ceafbe53d1","APP_IPHONE_65")

        # 

        # print(result)

    def UploadScreenShot(self,appid,version,lan,type,filepath):     
        # for i in range(5): 
        # mainUploadAssetApple.UploadScreenShot(appid, "IOS", version, "zh-Hans", "APP_IPHONE_65", "1.jpg")
        mainUploadAssetApple.UploadScreenShot(appid, "IOS", version, lan, type, filepath)
 
    def DeleteAllScreenShot(self,appid,version,lan,type):      
        mainUploadAssetApple.DeleteAllScreenShot(appid, "IOS", version, lan, type)
 
 
    def ReadAllAppLocalization(self, _id):
        header = self.GetApiUrlHead()  
        url = "https://api.appstoreconnect.apple.com/v1/appStoreVersions/"+_id+"/appStoreVersionLocalizations"
        # print(header) 

        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        ) 
        strret = mdl_rqt.content.decode("utf-8")
        return strret
    
    def GetAppLocalization(self, _id,lan):
        strret = self.ReadAllAppLocalization(_id)
        # print(strret)

        jsonRoot = json.loads(strret)
        for data in jsonRoot["data"]:
            id = data["id"] 
            if lan==data["attributes"]["locale"]:
                return id

        
        return self.CreateAppLocalization(_id,lan)
 


# 本地语言信息等
# Create an App Store Version Localization
# https://developer.apple.com/documentation/appstoreconnectapi/create_an_app_store_version_localization
# en-US zh-Hans en-CA en-AU en-GB
    def CreateAppLocalization(self, _id,lan):
        header = self.GetApiUrlHead()
        # _id = "fe097c65-e7f2-4092-84b7-8f3060837545"
        url = "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations"
        print(header)
        params = {
            "data": {
                "relationships": {
                    "appStoreVersion": {"data": {"id": _id, "type": "appStoreVersions"}}
                },
                "attributes": { 
                    "locale": lan,
                    "description": "Go wild and discover trails, parks and off-the-beaten-track terrain with Forest Explorer. Whether you’re bushwalking in the outback or looking for a quick local hike, Forest Explorer has thousands of trails and destinations from around the globe to explore.",
                    "keywords": "hiking, trails, backcountry, parks, path, terrain, forest",
                    "marketingUrl": "http://www.apple.com/forestexplorer",
                    "promotionalText": "Get Forest Explorer free for a limited time.",
                    "supportUrl": "https://support.apple.com",
                    "whatsNew": "Now includes trails in Europe and South America"
                      
                },
                "type": "appStoreVersionLocalizations"
            }
        }

        mdl_rqt = requests.post(
            url,
            json=params,
            headers=header
            # timeout=30
        )
        strret = mdl_rqt.content.decode("utf-8")
        print(strret)

        jsonRoot = json.loads(strret)
        id = jsonRoot["data"]["id"]
        return  id


    def ReadAllScreenshotSet(self, app_id):
        header = self.GetApiUrlHead() 
        # url = "https://api.appstoreconnect.apple.com/v1/appScreenshotSets/"+app_id
        url = "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/"+app_id+"/relationships/appScreenshotSets"
        # url = "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/"+app_id 
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        )
        strret = mdl_rqt.content.decode("utf-8")
        # print(strret)
        return strret


    def GetScreenshotSet(self, app_id,displayType):
        strret =self.ReadAllScreenshotSet(app_id)
        print("ReadAllScreenshotSet strret=",strret)
        jsonRoot = json.loads(strret)
        # iphone 5.5 ,ipadpro 3, ipadpro 2, iphone 6.5
        idx = 0
        if displayType=="APP_IPHONE_55":
            idx = 0
        if displayType=="APP_IPAD_PRO_3GEN_129":
            idx = 1
        if displayType=="APP_IPAD_PRO_129":
            idx = 2
        if displayType=="APP_IPHONE_65":
            idx = 3
 
        if len(jsonRoot["data"])!=0:
            _id = jsonRoot["data"][idx]["id"]
        else:
            _id = self.CreateScreenshotSet(app_id,displayType)
        return _id


    # https://developer.apple.com/documentation/appstoreconnectapi/create_an_app_screenshot_set
# https://developer.apple.com/documentation/appstoreconnectapi/screenshotdisplaytype
# APP_IPHONE_65
    def CreateScreenshotSet(self, app_id,displayType):
        header = self.GetApiUrlHead()
        # app_id = "631ff5d0-2a4e-4d10-bd56-b43e5c2bd77d"
        url = "https://api.appstoreconnect.apple.com/v1/appScreenshotSets"
        print(header)
        params = {
            "data": {
                "relationships": {
                    "appStoreVersionLocalization": {"data": {"id": app_id, "type": "appStoreVersionLocalizations"}}
                },
                "attributes": { 
                    "screenshotDisplayType": displayType
                },
                "type": "appScreenshotSets"
            }
        }

        mdl_rqt = requests.post(
            url,
            json=params,
            headers=header
            # timeout=30
        )
        print(mdl_rqt.content.decode("utf-8"))

# https://developer.apple.com/documentation/appstoreconnectapi/create_an_app_screenshot
    def CreateScreenshot(self, app_id,index):
        header = self.GetApiUrlHead() 
        url = "https://api.appstoreconnect.apple.com/v1/appScreenshots"
        # print(header)
        # 261238 "1.jpg",
        params = {
            "data": {
                "relationships": {
                    "appScreenshotSet": {"data": {"id": app_id, "type": "appScreenshotSets"}}
                },
                "attributes": { 
                    "fileName":"1.jpg",
                    "fileSize":mainResource.get_FileSize(self.fileScreenshot) 
                },
                "type": "appScreenshots"
            }
        }

        mdl_rqt = requests.post(
            url,
            json=params,
            headers=header
            # timeout=30
        )
        strret = mdl_rqt.content.decode("utf-8")
        print(strret)

        #        "uploadOperations" : [ {
        #         "method" : "PUT",
        #         "url" : "https://store-030.blobstore.apple.com/itms6-assets-massilia-030001/PurpleSource62%2Fv4%2Fc4%2Fc6%2F5f%2Fc4c65fe0-b616-0454-d71b-7771b95f74f1%2FgzsRhfc7iZIvrJoG3mdTlRGfH-Hu1JJBY_Y82m_QlKU_U003d-1587670858469?uploadId=5ae7a610-859a-11ea-adb0-d8c497b45469&Signature=nL9SQyAh4l1tEwoWQhiflX270Zs%3D&AWSAccessKeyId=MKIA4IEXBU1OGIOUHE96&partNumber=1&Expires=1588275658",
        #         "length" : 11097,
        #         "offset" : 0,
        #         "requestHeaders" : [ {
        #             "name" : "Content-Type",
        #             "value" : "image/png"
        #         } ]
        #    } ],
        jsonRoot = json.loads(strret)
        url = jsonRoot["data"]["attributes"]["uploadOperations"][0]["url"]
        length = jsonRoot["data"]["attributes"]["uploadOperations"][0]["length"]
        print(url)
        self.UploadImage(url,length)
        _id = jsonRoot["data"]["id"]
        time.sleep(60)
        self.CommitUploadImage(_id)
        return _id


    def GetUrlHeadUploadImage(self,length,offset=0):
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        header = {
            # 'Content-Type': 'application/json',
            # 'Authorization': 'Bearer %s'%str(token, encoding='utf-8')
            # 'Authorization': strauthor
            'Content-Type': 'image/jpg',
            # 'Content-Length': '%s' % length ,
            'length': '%s' % length ,
            'offset': '%s' % offset ,
            'Authorization': 'Bearer %s' % token
            # 指定JWT
        }
        return header


 
 

# https://developer.apple.com/documentation/appstoreconnectapi/uploading_assets_to_app_store_connect
    def UploadImage(self, url,length):
        header = self.GetUrlHeadUploadImage(length)  
        print("UploadImage header=",header) 
        offset=0
        body = {
            'length': '%s' % length ,
            'offset': '%s' % offset 
        }

        mdl_rqt = requests.put(
            url, 
            headers=header,
            # json=body,
            timeout=3000
        )
        print("UploadImage end = ",mdl_rqt.content.decode("utf-8"))
        # print(mdl_rqt.content.decode("utf-8"))

 
    def CommitUploadImage(self, _id):
        # _id ="111"
        url = "https://api.appstoreconnect.apple.com/v1/appScreenshots/"+_id
        header = self.GetApiUrlHead()  
        # print(header) 

        sourceFileChecksum = mainResource.get_MD5_checksum_file(self.fileScreenshot)
        print(sourceFileChecksum)
        print(url)
        params = {
            "data": {
                "attributes": { 
                    "uploaded": True,
                    "sourceFileChecksum": sourceFileChecksum
                },
                "id": _id,
                "type": "appScreenshots"
            }
        }
        # print(params)
        json_str = json.dumps(params) 
        print(json_str)
     
        mdl_rqt = requests.patch(
            url,
            json=json_str,
            headers=header,
            timeout=3000
        )
        print("CommitUploadImage end ",mdl_rqt.content.decode("utf-8"))

 
    def GetNameByPackage(self,package):
        return package.replace(".","").replace("commoonma","")

# https://developer.apple.com/documentation/appstoreconnectapi/register_a_new_bundle_id
    def CreateBundleID(self,package):
        ret = ""
        header = self.GetApiUrlHead()  
        url = "https://api.appstoreconnect.apple.com/v1/bundleIds" 
        name=self.GetNameByPackage(package)
        # name = "Learn Chinese Word"
        print("self.teamID=",self.teamID)
        print("name=",name)
        # package = 'Y9ZUK2WTEE.com.moonma.poem'
        # name = 'com-moonma-poem'
        params = {'data':{'attributes':{'identifier':package,'name':name,'platform':'IOS','seedId':self.teamID},'type':'bundleIds'}} 
        
        mdl_rqt = requests.post(
            url, 
            headers=header,
            json=params,
            # timeout=30
        ) 

        strret = mdl_rqt.content.decode("utf-8")
        print("CreateBundleID strret=",strret)
        jsonRoot = json.loads(strret)
        if "data" in jsonRoot:
            ret = jsonRoot["data"]["id"] 
        return ret  

    def DeleteBundleID(self,bundleid):
        header = self.GetApiUrlHead()  
        url = "https://api.appstoreconnect.apple.com/v1/bundleIds/"+bundleid 
        mdl_rqt = requests.delete(
            url, 
            headers=header, 
            # timeout=30
        ) 

        strret = mdl_rqt.content.decode("utf-8")
        print("DeleteBundleID strret=",strret)  

    def create_app_version(self, url, app_id, version_string, platform='IOS',  # required fields
                           release_type='MANUAL', copyright=None, build_id=None,
                           earliest_release_date=None, uses_idfa=False):
        header = self.GetApiUrlHead()
        # print(header)
        params = {
            "data": {
                "relationships": {
                    "app": {"data": {"id": app_id, "type": "apps"}}
                },
                "attributes": {
                    "versionString": version_string,
                    "platform": platform,
                    "releaseType": release_type,
                    "earliestReleaseDate": earliest_release_date,
                    "usesIdfa": uses_idfa
                },
                "type": "appStoreVersions"
            }
        }
        if copyright != None:
            params['data']['attributes']['copyright'] = copyright
        # Add build relationship if there is a build ID
        if build_id != None:
            params['data']['relationships']['build'] = {
                "data": {"id": build_id, "type": "builds"}}

        mdl_rqt = requests.post(
            url,
            json=params,
            headers=header
            # timeout=30
        )
        print(mdl_rqt.content.decode("utf-8"))


  ## 查询证书
    def ListAllCertificates(self):
        header = self.GetApiUrlHead()
        url = "https://api.appstoreconnect.apple.com/v1/certificates"
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        )
        
        result = mdl_rqt.content.decode("utf-8")
        json = mdl_rqt.json()
        # print(result)
        self.SaveData2Json(json,"Certificate.json")

    ## 查询bundleid列表接口
    # limit 请求的bundleid个数
    # sort Possible values: id, -id, name, -name, platform, -platform, seedId, -seedId
    def ListAllBundleIds(self,limit=200,sort='id'):
        header = self.GetApiUrlHead()
        url = "https://api.appstoreconnect.apple.com/v1/bundleIds" 
        params = {'limit':limit,'sort':sort}
        mdl_rqt = requests.get(
            url, 
            params=params,
            headers=header
            # timeout=30
        )
        result = mdl_rqt.content.decode("utf-8")
        json = mdl_rqt.json()
        # print("ListAllBundleIds =",result)
        self.SaveData2Json(json,"Bundle_id.json")
        # self.ListBundleIdOfPackage(package)
        return result


    def GetBundleIdOfPackage(self,package):
        # print("ListBundleIdOfPackage start") 
        header = self.GetApiUrlHead()
        # url = "https://api.appstoreconnect.apple.com/v1/bundleIds" 
        url = "https://api.appstoreconnect.apple.com/v1/bundleIds?filter[identifier]="+package 
        limit=200
        sort='id'
        params = {'limit':limit,'sort':sort,}
        mdl_rqt = requests.get(
            url, 
            params=params,
            headers=header
            # timeout=30
        )
        result = mdl_rqt.content.decode("utf-8")
        # json = mdl_rqt.json()
        # print("ListBundleIdOfPackage result=",result) 

        ret =""
        jsonRoot = json.loads(result)
        list = jsonRoot["data"]
        for data in list:
            if data["attributes"]["identifier"] == package:
                ret = data["id"]
                break
        print("ListBundleIdOfPackage ret=",ret) 
        return ret

    def GetAppInfo(self,appid):
        header = self.GetApiUrlHead()
        url = "https://api.appstoreconnect.apple.com/v1/apps/"+appid
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        )
        result = mdl_rqt.content.decode("utf-8")
        json = mdl_rqt.json()
        # print("ListAllBundleIds =",result)
        # self.SaveData2Json(json,"AppInfo_Api.json") 
 
    def DeleteProfile(self,id):
        header = self.GetApiUrlHead()  
        url = "https://api.appstoreconnect.apple.com/v1/profiles/"+id 
        mdl_rqt = requests.delete(
            url, 
            headers=header, 
            # timeout=30
        ) 

        strret = mdl_rqt.content.decode("utf-8")
        print("DeleteProfile strret=",strret) 


    def DeleteAllProfile(self,package):
        bundle_id = self.GetBundleIdByPackage(package)
        header = self.GetApiUrlHead()
        url = "https://api.appstoreconnect.apple.com/v1/bundleIds/"+bundle_id+"/profiles"
        mdl_rqt = requests.get(
            url, 
            headers=header
            # timeout=30
        )
        result = mdl_rqt.content.decode("utf-8")
        json = mdl_rqt.json()
        jsondata = json["data"]
        for data in jsondata:
            id = data["id"]
            self.DeleteProfile(id)


    def GetAppProfile(self,package,appid):

        filename = package+".mobileprovision" 
        savepath = mainResource.GetResourceDataApp()+"/"+filename
        savepath = os.path.normpath(savepath) 
        if os.path.exists(savepath):
            return
            
        # self.DeleteAllProfile(package)

        self.ListAllCertificates()
        self.GetAppInfo(appid)
        bundle_id = self.GetBundleIdByPackage(package)
        print("bundle_id =",bundle_id)

        count = 0
        if len(bundle_id)==0:
            count = 0
        else:
        # self.DeleteBundleID(bundle_id)
        # bundle_id = self.GetBundleIdByPackage(package)

            header = self.GetApiUrlHead()
            url = "https://api.appstoreconnect.apple.com/v1/bundleIds/"+bundle_id+"/profiles"
            mdl_rqt = requests.get(
                url, 
                headers=header
                # timeout=30
            )
            result = mdl_rqt.content.decode("utf-8")
            json = mdl_rqt.json()
            # print("ListAllBundleIds =",result)
            self.SaveData2Json(json,"GetAppProfile.json")
            jsonRoot =json
            jsondata = jsonRoot["data"]
            count = len(jsondata)

        print("GetAppProfile count=",count," package="+package)
        if count:
            dataprofile = jsonRoot["data"][0]["attributes"]["profileContent"]
            
        else:
            # if isCreate:
            dataprofile =self.CreateProfile(package,appid) 
         
        decode_content = self.base64decode(dataprofile)  
        FileUtil.SaveByte2File(decode_content, savepath)


    def base64decode(self,content):
        return base64.b64decode(content)

    # name profile name
    # type IOS_APP_DEVELOPMENT, IOS_APP_STORE, IOS_APP_ADHOC
    # bundle_id 包名的id
    # certificate_id 证书id
#  https://developer.apple.com/documentation/appstoreconnectapi/create_a_profile
    def CreateProfile(self, package,appid):
        # result = self.api.list_bundle_ids()
        # self.SaveData2Json(result,"Bundle_id2.json")

        print("CreateProfile appid=",appid)
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        str_url = "https://api.appstoreconnect.apple.com/v1/profiles"
        header = self.GetApiUrlHead()
        # print(header) 
 
        type = 'IOS_APP_STORE' 
        name=self.GetNameByPackage(package)
        bundle_id = self.GetBundleIdByPackage(package)
        print("CreateProfile bundle_id=",bundle_id)
        cerificate_id = self.CertificateID

        params = {'data':{
                        'attributes':{'name':name,'profileType':type},
                        'relationships':{
                                            'bundleId':{'data':{'id':bundle_id,'type':'bundleIds'}},
                                            'certificates':{'data':[{'id':cerificate_id,'type':'certificates'}]},
                                        },
                        'type':'profiles'
                    }
                }
        # App Store profile must not include devices relationship
        if type != 'IOS_APP_STORE':
            params['data']['relationships']['devices'] = {'data':devices}


        mdl_rqt = requests.post(
            str_url,
            json=params,
            headers=header
            # timeout=30
        )
        # 5. 将get回来的content使用gzip解码
        strret = mdl_rqt.content.decode("utf-8")
        print("CreateProfile strret =",strret)
        json = mdl_rqt.json()
        dataprofile = json["data"]["attributes"]["profileContent"] 
        return dataprofile

 

    def CreateProfile2(self, package,appid):
        # package = mainap
        # devices = api.list_devices(limit=1)
        # print(devices)

        # result = api.register_device('name','udid')
        # print(result)

        # result = api.register_certificate(csr_path='/Users/last/Desktop/CertificateSigningRequest.certSigningRequest')
        # print(result)

        # result = api.delete_certificate('N9P79WJTHK')
        # print(result)

        # result = self.api.list_certificates()
        # # print(result)
        # self.SaveData2Json(result,"Certificate.json")

        # result = api.register_bundle_id(bundle_id='com.hepburn.app',team_id='6DD349HLLU',name='hepburn')
        # print(result)

        # result = api.list_bundle_ids()
        # # print(result)
        # self.SaveData2Json(result,"Bundle_id.json")

        # result = api.list_bundle_ids(sort='-identifier com.moonma.poem')
        # "name": "com-moonma-poem",

        # result = api.get_bundle_id('com.moonma.poem')
        # print(result)

        # result = api.get_bundle_id_profiles('N49MX9AWAX')
        # print(result)

        # result = api.delete_bundle_id('N49MX9AWAX')
        # print(result)

        # result = api.create_app_version(app_id='123456', version_string='1.2.3', platform='IOS',
        #                                 release_type='AFTER_APPROVAL', copyright='2020 My Company', build_id='123',
        #                                 earliest_release_date=None, uses_idfa=False)
        # print(result)

        # result = api.get_app_version_localizations('a1a2a3a4-a1a2-a1a2-a1a2-a1a2a3a4a5a6')
        # print(result)

        bundleid = self.GetBundleIdByPackage(package)
        print("bundleid=",bundleid)
        #   # type IOS_APP_DEVELOPMENT, IOS_APP_STORE, IOS_APP_ADHOC
        result = self.api.create_profile(name=package, bundle_id=bundleid, certificate_id=self.CertificateID, type='IOS_APP_STORE')

        result = self.api.get_bundle_id_profiles(bundleid)
        print(result)
        # self.SaveData2Json(result,"create_profile.json")
        filename = package+".mobileprovision"
        src = self.DIR_HOME+"/"+filename
        src = os.path.normpath(src)
        dst = mainResource.GetResourceDataApp()+"/"+filename
        dst = os.path.normpath(dst)
        FileUtil.CopyFile(src, dst)

        # result = api.delete_profile('4KVXW4LK52')
        # print(result)

        # result = api.list_profiles()
        # print(result)

        # result = api.request_profile('4KVXW4LK52')
        # print(result)

        # result = api.list_apps()
        # print(result)

        # result = api.get_app_versions('123456')
        # print(result)

    def GetAllApp(self, isHD):
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        str_url = "https://api.appstoreconnect.apple.com/v1/apps"
        # str_url = "https://api.appstoreconnect.apple.com/v1/apps/894369706"

        header = self.GetApiUrlHead()
        print(header)

        mdl_rqt = requests.get(
            str_url,
            headers=header,
            timeout=30
        )
        # 5. 将get回来的content使用gzip解码
        print(mdl_rqt.content.decode("utf-8"))

# TestFlight
# List Beta Testers

    def GetAppAllTester(self, isHD):
        token = self.CreateJWTToken(self.API_KEY_ID, self.API_USER_ID)
        str_url = "https://api.appstoreconnect.apple.com/v1/betaTesters" 
        header = self.GetApiUrlHead() 
        mdl_rqt = requests.get(
            str_url,
            headers=header,
            timeout=30
        )
        # 5. 将get回来的content使用gzip解码
        print(mdl_rqt.content.decode("utf-8"))

mainAppConnectApi = AppConnectApi()
