# 导入selenium的浏览器驱动接口


import sys
import os
import json
import sys
import argparse
from apiclient import sample_tools
from oauth2client import client

o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
sys.path.append("../")

import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Common import Source  
from AppStore.AppStoreBase import AppStoreBase
from AppStore.AppConnectApi import mainAppConnectApi
from AppInfo.AppInfo import mainAppInfo
from Project.Resource import mainResource

from Common.File.FileUtil import FileUtil 

from Common.Platform import Platform
# @moon line 1052, in method
  #  raise UnknownFileType(media_filename)
# googleapiclient.errors.UnknownFileType: shapecolor_shapecolor_gp.apk
# https://github.com/googlesamples/android-play-publisher-api/issues/14

# go to regedit.exe
# go to HKEY_LOCAL_MACHINE\Software\Classes
# right click Classes, New Key - call it .apk
# right click on the right hand side, New String - "Content Type", "application/vnd.android.package-archive"

# @moon

class GooglePlayApi:  

    def GetPython(self):
        python = "python"
        if Platform.isMacSystem():
            python = "python3"
        
        return python

    def UpdateAppInfo(self,package,country,title,detail,shortDetail,strHD,lan):
        #argv ="c "+ package
        #argv ="['AppStoreManager.py', 'com.moonma.wordpuzzle']" 
        # package lan title detail shortdetail
        # os.system("python AppStore/Google/update_listings.py "+package+" "+lan+" "+title+" "+detail+" "+shortDetail)
        python = self.GetPython() 

        os.system(python+" AppStore/Google/update_listings.py "+package+" "+country+" "+strHD+" "+lan+" "+mainResource.cmdPath)
        return

        argparser = argparse.ArgumentParser(add_help=False)
        argparser.add_argument('package_name', help='The package name. Example: com.android.sample')


        # Authenticate and construct service.
        service, flags = sample_tools.init(
            argv,
            'androidpublisher',
            'v3',
            __doc__,
            __file__,
            parents=[argparser],
            scope='https://www.googleapis.com/auth/androidpublisher')

        # Process flags and read their values.
        package_name = flags.package_name

        try:
            edit_request = service.edits().insert(body={}, packageName=package_name)
            result = edit_request.execute()
            edit_id = result['id']

            listing_response_us = service.edits().listings().update(
                editId=edit_id, packageName=package_name, language=lan,
                body={'fullDescription': detail,
                    'shortDescription': shortDetail,
                    'title': title}).execute()

            print ('Listing for language %s was updated.'
                % listing_response_us['language'])
 

            commit_request = service.edits().commit(
                editId=edit_id, packageName=package_name).execute()

            print ('Edit "%s" has been committed' % (commit_request['id']))

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run the '
                'application to re-authorize')



    def DeleteAllScreenShot(self,package,version,lan,imageType):
        print("DeleteAllScreenShot")
 
    def UploadOneScreenShot(self,package,image_file,lan,imageType):
        # # package imageFile lan imageType
        python = self.GetPython() 
        os.system(python+" AppStore/Google/screenshot.py "+package+" "+image_file+" "+lan+" "+imageType)
        return

        # Authenticate and construct service.
        argv =package+" "+image_file
        service, flags = sample_tools.init(
            argv,
            'androidpublisher',
            'v3',
            __doc__,
            __file__, parents=[argparser],
            scope='https://www.googleapis.com/auth/androidpublisher')

        # Process flags and read their values.
        package_name = flags.package_name
        image_file = flags.image_file

        try:
            edit_request = service.edits().insert(body={}, packageName=package_name)
            result = edit_request.execute()
            edit_id = result['id']


        # https://developers.google.cn/android-publisher/api-ref/rest/v3/AppImageType?hl=zh-cn
        # upload(packageName, editId, language, imagpheType, media_body=None, media_mime_type=None)
            image_response = service.edits().images().upload(
                editId=edit_id,
                packageName=package_name,
                # language="en-US",
                # imageType="phoneScreenshots",
                language=lan,
                imageType=imageType,
                media_body=image_file).execute()

            # print ('Version code %d has been uploaded' % image_response['versionCode'])

            # track_response = service.edits().tracks().update(
            #     editId=edit_id,
            #     track=TRACK,
            #     packageName=package_name,
            #     body={u'releases': [{
            #         u'name': u'My first API release with release notes',
            #         u'versionCodes': [str([apk_response['versionCode']])],
            #         u'releaseNotes': [
            #             {u'recentChanges': u'Apk recent changes in en-US'},
            #         ],
            #         u'status': u'completed',
            #     }]}).execute()

            # print 'Track %s is set with releases: %s' % (
            #     track_response['track'], str(track_response['releases']))

            commit_request = service.edits().commit(
                editId=edit_id, packageName=package_name).execute()

            # print 'Edit "%s" has been committed' % (commit_request['id'])

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run the '
                'application to re-authorize')



    def UploadApk(self,package,apk_file):
        argv =package+" "+apk_file
        python = self.GetPython()
        os.system(python+" AppStore/Google/upload_apks_with_listing.py "+package+" "+apk_file)
        return
        # Authenticate and construct service.
        service, flags = sample_tools.init(
            argv,
            'androidpublisher',
            'v3',
            __doc__,
            __file__, parents=[argparser],
            scope='https://www.googleapis.com/auth/androidpublisher')

        # Process flags and read their values.
        package_name = flags.package_name
        apk_file = flags.apk_file

        try:
            edit_request = service.edits().insert(body={}, packageName=package_name)
            result = edit_request.execute()
            edit_id = result['id']

            apk_response = service.edits().apks().upload(
                editId=edit_id,
                packageName=package_name,
                media_body=apk_file).execute()

            print ('Version code %d has been uploaded' % apk_response['versionCode'])

            track_response = service.edits().tracks().update(
                editId=edit_id,
                track=TRACK,
                packageName=package_name,
                body={u'releases': [{
                    u'name': u'My first API release with release notes',
                    u'versionCodes': [str([apk_response['versionCode']])],
                    u'releaseNotes': [
                        {u'recentChanges': u'Apk recent changes in en-US'},
                    ],
                    u'status': u'completed',
                }]}).execute()

            print ('Track %s is set with releases: %s' % (track_response['track'], str(track_response['releases'])))

            commit_request = service.edits().commit(
                editId=edit_id, packageName=package_name).execute()

            print ('Edit "%s" has been committed' % (commit_request['id']))

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run the '
                'application to re-authorize')

mainGooglePlayApi = GooglePlayApi()
    
 
