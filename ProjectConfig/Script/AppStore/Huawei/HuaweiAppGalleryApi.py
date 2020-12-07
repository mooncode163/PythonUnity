# 导入selenium的浏览器驱动接口


import sys
import os
import json
import sys
import argparse 
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
sys.path.append("../")
sys.path.append("../../")

import time 
from Common.File.FileUtil import FileUtil
# from AppInfo.AppInfo import mainAppInfo
# from AppStore.AppStoreAcount import mainAppStoreAcount
from Common import Source

class HuaweiAppGalleryApi:  
    # ClientId = "469947311665972416"
    # ClientSecret = "7701769ABE85209F58C1736D3FD95C8B9B7225F6EDC1415482D1EB142C8ED201"
    accessToken = ""
    listScreeenshot = []
    # https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-References/obtain_token

    # def __init__(self): 
    #     name = mainAppInfo.GetAppStoreAcount(isHD,Source.HUAWEI)
    #     self.ClientId = mainAppStoreAcount.GetClientId(Source.HUAWEI,name)
    #     self.ClientSecret = mainAppStoreAcount.GetClientSecret(Source.HUAWEI,name) 

    def GetToken(self):
        if len(self.accessToken)>0:
            return self.accessToken

        url = "https://connect-api.cloud.huawei.com/api/oauth2/v1/token"
        header = {
            'Content-Type': 'application/json' 
            # 'Authorization': 'Bearer %s'%str(token, encoding='utf-8')
            # 'Authorization': strauthor
            # 'Authorization': 'Bearer %s' % token
            # 指定JWT
        }
        
        params = { 
            'grant_type':'client_credentials',  
            'client_id':self.ClientId, 
            "client_secret":self.ClientSecret
            # 'Authorization': 'Bearer %s'%str(token, encoding='utf-8')
            # 'Authorization': strauthor
            # 'Authorization': 'Bearer %s' % token
            # 指定JWT
        }

        mdl_rqt = requests.post(
            url,
            json=params,
            headers=header
            # timeout=30
        )
  
        strret = mdl_rqt.content.decode("utf-8") 
        # access_token
        print(strret)
        jsonRoot = json.loads(strret)
        result = jsonRoot["access_token"]
        print(result)
        self.accessToken = result
        return result
 

# https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-References/agcapi-app-info_update_v2
    def UpdateAppBaseInfo(self,appId,defaultLang,privacyPolicy):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-info?appId="+appId
   
        # {"HW":"3+"}
        dictitem =  dict(HW='3+')
        print("UpdateAppBaseInfo dictitem=",dictitem)

        params = { 
            'defaultLang':defaultLang,  
            'contentRate':json.dumps(dictitem),  
            'privacyPolicy':privacyPolicy 
            
            
        }

        mdl_rqt = requests.put(
            url,
            json=params,
            headers=self.GetUrlHead() 
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)

        self.SubmitAppTime(appId)
        # self.SubmitApp(appId)
        

    def UpdateAppInfo(self,appId,country,title,detail,shortDetail,what_is_new):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-language-info?appId="+appId
        header = {
            'Content-Type': 'application/json', 
            'client_id':self.ClientId, 
            'Authorization': 'Bearer %s' % self.GetToken()
        }
        
        params = { 
            'lang':country,  
            'appName':title, 
            "appDesc":detail,
            'briefInfo':shortDetail, 
            'newFeatures':what_is_new
            
            
        }

        mdl_rqt = requests.put(
            url,
            json=params,
            headers=header 
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)

    # def DeleteAllScreenShot(self,package,version,lan,imageType):
    #     print("DeleteAllScreenShot")
 
    def StartScreenShot(self):  
        self.listScreeenshot = []

    def DeleteLanuage(self,appId,lan):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-language-info?appId="+appId+"&lang="+lan
        mdl_rqt = requests.delete(
            url,  
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        # {"ret":{"code":204144641,"msg":"[AppGalleryConnectPublishService]input fileUrls format error, sign is empty"}}
        return strret



    def UploadOneScreenShot(self,appId,image_file,isHd):
        jsonfiledata = self.UploadFile(appId,image_file)
        self.listScreeenshot.append(jsonfiledata)
        # self.CommitImage(appId,fileDestUrl)

    def CommitScreenShot(self,appId,isHd,country): 
        self.CommitImage(appId,isHd,country)

    def UploadImageIcon(self,appId,image_file,lan):
        jsonfiledata = self.UploadFile(appId,image_file)
        self.CommitImageIcon(appId,jsonfiledata,lan)

    def CommitImageIcon(self,appId,jsondata,lan):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-file-info?appId="+appId 
        # https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-Guides/agcapi-reference-langtype
        # print("self.listScreeenshot[0]=",self.listScreeenshot[0])
        fileDestUrl = jsondata['fileDestUlr']
        imageResolution = jsondata['imageResolution']
        imageResolutionSingature = jsondata['imageResolutionSingature']
        size = jsondata['size']
        print("size=",size)
        
        params = {  
            'lang':lan,
            # en-US zh-CN
            'imgShowType':'0',
            'fileType':'0',
            'files':
            [
                {
                    'size':size,
                    'imageResolution':imageResolution,
                    'imageResolutionSingature':imageResolutionSingature,
                    'fileDestUrl':fileDestUrl
                } 
            ] 
        }


        mdl_rqt = requests.put(
            url, 
            json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        # {"ret":{"code":204144641,"msg":"[AppGalleryConnectPublishService]input fileUrls format error, sign is empty"}}
        return strret


    def UploadImageCopyRight(self,appId,image_file):
        jsonfiledata = self.UploadFile(appId,image_file)
        self.CommitImageCopyRight(appId,jsonfiledata)

    def CommitImageCopyRight(self,appId,jsondata):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-file-info?appId="+appId 
        # https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-Guides/agcapi-reference-langtype
        # print("self.listScreeenshot[0]=",self.listScreeenshot[0])
        fileDestUrl = jsondata['fileDestUlr']
        imageResolution = jsondata['imageResolution']
        imageResolutionSingature = jsondata['imageResolutionSingature']
        size = jsondata['size']
        print("size=",size)
        
        params = {  
            # 'lang':lan,
            # en-US zh-CN
            'imgShowType':'0',
            'fileType':'6',
            'files':
            [
                {
                    'size':size,
                    'imageResolution':imageResolution,
                    'imageResolutionSingature':imageResolutionSingature,
                    'fileDestUrl':fileDestUrl
                } 
            ] 
        }


        mdl_rqt = requests.put(
            url, 
            json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        # {"ret":{"code":204144641,"msg":"[AppGalleryConnectPublishService]input fileUrls format error, sign is empty"}}
        return strret

# https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-References/agcapi-app-file-info_v2
    def CommitImage(self,appId,isHd,country):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-file-info?appId="+appId 
        # https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-Guides/agcapi-reference-langtype
        # print("self.listScreeenshot[0]=",self.listScreeenshot[0])

        fileDestUrl = self.listScreeenshot[0]['fileDestUlr']
        imageResolution = self.listScreeenshot[0]['imageResolution']
        imageResolutionSingature = self.listScreeenshot[0]['imageResolutionSingature']

        # jsonfiles = dict ()
        jsonfiles = [] 
        for jsondata in self.listScreeenshot:
            dictitem = dict (imageResolution=jsondata['imageResolution'],imageResolutionSingature= jsondata['imageResolutionSingature'],fileDestUrl= jsondata['fileDestUlr'], size= jsondata['size'])
            # print("dictitem=",dictitem)
            jsonfiles.append(dictitem)

        # print("jsonfiles=",jsonfiles) 

        imgType = '0'
        if isHd==True:
            imgType = '1'


        params = {  
            'lang':country,
            # en-US zh-CN
            'imgShowType':imgType,
            'fileType':'2',
            'files':jsonfiles
            # [
            #     {
            #         'size':self.listScreeenshot[0]['size'],
            #         'imageResolution':self.listScreeenshot[0]['imageResolution'],
            #         'imageResolutionSingature':self.listScreeenshot[0]['imageResolutionSingature'],
            #         'fileDestUrl':self.listScreeenshot[0]['fileDestUlr'] 
            #     }
            #     ,
            #      {
            #          'size':self.listScreeenshot[1]['size'],
            #         'imageResolution':self.listScreeenshot[1]['imageResolution'],
            #         'imageResolutionSingature':self.listScreeenshot[1]['imageResolutionSingature'],
            #         'fileDestUrl':self.listScreeenshot[1]['fileDestUlr'] 
            #     },
            #        {
            #         'size':self.listScreeenshot[2]['size'],
            #         'imageResolution':self.listScreeenshot[2]['imageResolution'],
            #         'imageResolutionSingature':self.listScreeenshot[2]['imageResolutionSingature'],
            #         'fileDestUrl':self.listScreeenshot[2]['fileDestUlr'] 
            #     }
            # ]
            #  'files':{
            #      'fileDestUrl':self.listScreeenshot[0]
            #  }
        }


        mdl_rqt = requests.put(
            url, 
            json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        return strret

    def GetUrlHead(self):
        header = {
            'Content-Type': 'application/json', 
            'client_id':self.ClientId, 
            'Authorization': 'Bearer %s' % self.GetToken()
        }
        return header


# https://developer.huawei.com/consumer/cn/doc/development/AppGallery-connect-References/agcapi-upload-url_v2
#  suffix apk/rpk/pdf/jpg/jpeg/png/bmp/mp4/mov/aab
    def GetUploadUrl(self,appId,suffix):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/upload-url?appId="+appId+"&suffix="+suffix
        print(url)
        mdl_rqt = requests.get(
            url, 
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        return strret


    def UploadFile(self,appId,filepath):
        print("UploadFile filepath="+filepath)
        suffix = FileUtil.GetFileExt(filepath)
        strurl = self.GetUploadUrl(appId,suffix)
        jsonRoot = json.loads(strurl)
        uploadUrl = jsonRoot["uploadUrl"]
        authCode = jsonRoot["authCode"]  
        files = {'file': open(filepath, 'rb')} 
        params = { 
            'authCode':authCode,  
            # 'file':files,  
            'fileCount':1
        }
        fileName = FileUtil.GetPathNameWithExt(filepath)
        m = MultipartEncoder(
            fields={
            'authCode':authCode, 
            'fileCount':'1', 
            'parseType':'1', 
            'file': (fileName, open(filepath, 'rb'), 'multipart/form-data')
            # 'file': open(filepath, 'rb')
             }
        ) 
        print("m.content_type="+m.content_type)
        header = {
            'Content-Type':  m.content_type, 
            # 'Content-Type':  'multipart/form-data', 
            # 'accept':'application/json', 
            'client_id':self.ClientId, 
            'Authorization': 'Bearer %s' % self.GetToken()
        }

        mdl_rqt = requests.post(
            uploadUrl,
            # json=paramges,
            data=m,
            # files=files, 
            headers=header 
        ) 
        strret = mdl_rqt.content.decode("utf-8") 
        print(strret)
         
        jsonRoot = json.loads(strret)
        UploadFileRsp = jsonRoot["result"]["UploadFileRsp"]
        fileDestUrl = UploadFileRsp["fileInfoList"][0]["fileDestUlr"]
        print("fileDestUrl="+fileDestUrl)
        return UploadFileRsp["fileInfoList"][0]


    def SaveData2Json(self, data, savepath):
        json_str = json.dumps(data, ensure_ascii=False,
                              indent=4, sort_keys=True)
        FileUtil.SaveString2File(json_str, savepath)

    def GetVersion(self,appId,isInAppleStore=False): 
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-info?appId="+appId    
        mdl_rqt = requests.get(
            url,  
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        # print(strret)
        jsonRoot = json.loads(strret)
        jsonAppInfo = jsonRoot["appInfo"]
        key = "versionNumber"
        version = "1.0.0"
        if isInAppleStore:
            releaseState =jsonAppInfo["releaseState"]
        else:
            releaseState = 0

        print(" releaseState =",releaseState)

        if releaseState == 0:
            # 0 已上架
            if  (key  in  jsonAppInfo) :
                version = jsonAppInfo[key] 

        return version

    def GetAppInfo(self,appId): 
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-info?appId="+appId    
        mdl_rqt = requests.get(
            url,  
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        # print(strret)
        return strret

    def CommitApk(self,appId,jsondata,filepath):
        fileDestUrl = jsondata['fileDestUlr']
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-file-info?appId="+appId 
        fileName = FileUtil.GetPathNameWithExt(filepath)

        
        print(" fileName =",fileName)
        params = {  
            'fileType':'5',
            'files':
            [
            {
                # 'size':'79518677',
                'fileName':fileName,
                'fileDestUrl':fileDestUrl
            }
            ]
           
        }
        mdl_rqt = requests.put(
            url, 
            json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        return strret

    def SubmitApp(self,appId): 
        # self.SubmitAppTime(appId)
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-submit?appId="+appId   
        params = {  
            'fileType':'5' 
           
        }
        mdl_rqt = requests.post(
            url, 
            # json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        return strret

    def SubmitAppTime(self,appId): 
       
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/on-shelf-time?appId="+appId   
        params = {  
            'changeType':'2',
            'releaseTime':'2016-10-26T08:20:53.131252',
            'releaseType':'1'
        }
        mdl_rqt = requests.put(
            url, 
            json=params,
            headers=self.GetUrlHead()
        ) 
        strret = mdl_rqt.content.decode("utf-8")  
        print(strret)
        return strret




    def UploadApk(self,appId,apk_file):
        url = "https://connect-api.cloud.huawei.com/api/publish/v2/app-language-info?appId="+appId
        jsonfiledata = self.UploadFile(appId,apk_file)
        self.CommitApk(appId,jsonfiledata,apk_file)
        

mainHuaweiAppGalleryApi = HuaweiAppGalleryApi()
    
 
