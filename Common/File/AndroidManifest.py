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

from xml.dom.minidom import parse
import xml.dom.minidom 
import codecs


sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
from Common.Platform import Platform

from Common.File.FileUtil import FileUtil    

class AndroidManifest():   
    dom=None
    rootXml=None
    application=None

    def Load(self,filepath): 
        #加载真个文件到内存
        self.dom=xml.dom.minidom.parse(filepath)
        self.rootXml=self.dom.documentElement

        self.application = self.dom.getElementsByTagName('application')[0]
        print("self.application nodeName=",self.application.nodeName)
        
        # root.setAttribute('android:versionCode', versionCode)
        # root.setAttribute('android:versionName', versionName)
 
        #得到包名
        # package=root.getAttribute('package')        




    def GetMainActivity(self):  
        # #得到所有的Activity
        listActivity= self.dom.getElementsByTagName('activity')
        node = None
        for activity in listActivity:
            if activity.toxml().find("android.intent.action.MAIN")>0 and activity.toxml().find("android.intent.category.LAUNCHER")>0:
                node = activity
                break
 
        print("GetMainActivity nodeName=",node.nodeName)
        return node
        


    def AddUsesPermission(self,permission,isProtectionLevel = False):
      # #  <uses-permission android:name="android.permission.INTERNET"/>
        node = self.dom.createElement("uses-permission")
        #这个属性类似map中key,value
        node.setAttribute("android:name", permission)
        if isProtectionLevel:
            node.setAttribute("android:protectionLevel", "signature")
        # 把大节点info_node挂到根节点root_node下面
        self.rootXml.appendChild(node)
    

    def AddActivity(self,name,isMain,theme): 
        nodeActivity = self.dom.createElement("activity")
        
        nodeActivity.setAttribute("android:name", name)
        if len(theme)>0:
            nodeActivity.setAttribute("android:theme", theme)

        if isMain:
            node_intent_filter = self.dom.createElement("activity")
            
            node_action = self.dom.createElement("action")
            node_action.setAttribute("android:name", "android.intent.action.MAIN")
            node_intent_filter.appendChild(node_action)
            

            node_category = self.dom.createElement("category")
            node_category.setAttribute("android:name", "android.intent.category.LAUNCHER")
            node_intent_filter.appendChild(node_category)


            nodeActivity.appendChild(node_intent_filter)


            #       <intent-filter>
            #     <action android:name="android.intent.action.MAIN"/>
            #     <category android:name="android.intent.category.LAUNCHER"/>
            # </intent-filter>
    

        self.application.appendChild(nodeActivity)


    def ConfigSellMyApp(self,package):
        self.application.setAttribute('android:usesCleartextTraffic', "true")

    # <uses-permission android:name="android.permission.INTERNET"/>
    # <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    # <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    # <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
    # <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    # <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    # <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>
    # <uses-permission android:name="android.permission.CHANGE_NETWORK_STATE"/>
    # <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES"/>

    # <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    # <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>

        listPermission =["INTERNET","ACCESS_NETWORK_STATE","ACCESS_WIFI_STATE","READ_PHONE_STATE","ACCESS_COARSE_LOCATION","ACCESS_FINE_LOCATION","REQUEST_INSTALL_PACKAGES","CHANGE_NETWORK_STATE","QUERY_ALL_PACKAGES","READ_EXTERNAL_STORAGE","WRITE_EXTERNAL_STORAGE"]
        for strtmp in listPermission:
            self.AddUsesPermission("android.permission."+strtmp)
 

    # <permission android:name="com.unconditionalgames.waterpuzzle.permission.KW_SDK_BROADCAST" android:protectionLevel="signature"/>
        self.AddUsesPermission(package+".permission."+"KW_SDK_BROADCAST",True)
    # <uses-permission android:name="com.unconditionalgames.waterpuzzle.permission.KW_SDK_BROADCAST"/>
        self.AddUsesPermission(package+".permission."+"KW_SDK_BROADCAST",False)


        

    #  <activity android:name=".AdSplashActivity"  android:theme="@style/UnityThemeSelector">
    #         <intent-filter>
    #             <action android:name="android.intent.action.MAIN"/>
    #             <category android:name="android.intent.category.LAUNCHER"/>
    #         </intent-filter>
    #     </activity>
 
        mainAc = self.GetMainActivity()
        # child = mainAc.getElementsByTagName('intent-filter')[0]
        child = mainAc.childNodes[0]
        # author=dom.getElementsByTagName('author')[0].childNodes[0].data
        if child is not None:
            mainAc.removeChild(child)

        self.AddActivity(".AdSplashActivity",True,"@style/UnityThemeSelector")

 
 

        #  <!-- gdt ad -->
        # <service android:exported="false" android:multiprocess="true" android:name="com.qq.e.comm.DownloadService"/>
        # <activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize" android:multiprocess="true" android:name="com.qq.e.ads.ADActivity"/>
        # <activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize" android:multiprocess="true" android:name="com.qq.e.ads.PortraitADActivity" android:screenOrientation="portrait"/>
        # <activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize" android:multiprocess="true" android:name="com.qq.e.ads.LandscapeADActivity" android:screenOrientation="sensorLandscape"/>
        # <activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize" android:multiprocess="true" android:name="com.qq.e.ads.RewardvideoPortraitADActivity" android:theme="@android:style/Theme.Light.NoTitleBar">
        #     <meta-data android:name="android.notch_support" android:value="true"/>
        # </activity>
        # <activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize" android:multiprocess="true" android:name="com.qq.e.ads.RewardvideoLandscapeADActivity" android:screenOrientation="landscape" android:theme="@android:style/Theme.Light.NoTitleBar">
        #     <meta-data android:name="android.notch_support" android:value="true"/>
        # </activity>
        # <activity android:configChanges="keyboardHidden|orientation|screenSize" android:name="com.kwad.sdk.page.KsAdWebViewActivity" android:screenOrientation="portrait"/>
        # <activity android:configChanges="keyboardHidden|orientation|screenSize" android:name="com.kwad.sdk.page.VideoWebViewActivity" android:screenOrientation="portrait" android:theme="@android:style/Theme.Light.NoTitleBar.Fullscreen"/>
        # <activity android:configChanges="keyboardHidden|orientation|screenSize" android:name="com.kwad.sdk.page.KsFullScreenVideoActivity" android:screenOrientation="portrait" android:theme="@android:style/Theme.Light.NoTitleBar.Fullscreen"/>
        # <activity android:configChanges="keyboardHidden|orientation|screenSize" android:name="com.kwad.sdk.page.KSRewardVideoActivity" android:screenOrientation="portrait" android:theme="@android:style/Theme.Light.NoTitleBar.Fullscreen"/>
        # <provider android:authorities="com.unconditionalgames.waterpuzzle.adFileProvider" android:exported="false" android:grantUriPermissions="true" android:name="com.kwad.sdk.widget.AdSdkFileProvider">
        #     <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/ksad_file_paths"/>
        # </provider>
        # <receiver android:exported="true" android:name="com.ksad.download.DownloadReceiver">
        #     <intent-filter>
        #         <action android:name="download.intent.action.DOWNLOAD_PAUSE"/>
        #     </intent-filter>
        #     <intent-filter>
        #         <action android:name="download.intent.action.DOWNLOAD_RESUME"/>
        #     </intent-filter>
        #     <intent-filter>
        #         <action android:name="download.intent.action.DOWNLOAD_CANCEL"/>
        #     </intent-filter>
        # </receiver>
        # <service android:name="com.kwai.filedownloader.services.FileDownloadService$SharedMainProcessService"/>
        # <service android:name="com.kwai.filedownloader.services.FileDownloadService$SeparateProcessService" android:process=":filedownloader"/>
        # <service android:exported="false" android:name="com.ksad.download.service.DownloadService"/>
        # <service android:enabled="false" android:name="com.squareup.leakcanary.internal.HeapAnalyzerService" android:process=":leakcanary"/>
        # <service android:enabled="false" android:name="com.squareup.leakcanary.DisplayLeakService" android:process=":leakcanary"/>
        # <provider android:authorities="com.squareup.leakcanary.fileprovider.com.unconditionalgames.waterpuzzle" android:exported="false" android:grantUriPermissions="true" android:name="com.squareup.leakcanary.internal.LeakCanaryFileProvider">
        #     <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/leak_canary_file_paths"/>
        # </provider>
        # <activity android:enabled="false" android:icon="@mipmap/app_icon" android:label="@string/app_name" android:name="com.squareup.leakcanary.internal.DisplayLeakActivity" android:process=":leakcanary" android:taskAffinity="com.squareup.leakcanary.com.unconditionalgames.waterpuzzle" >
        #     <intent-filter>
        #         <action android:name="android.intent.action.MAIN"/>
        #         <category android:name="android.intent.category.LAUNCHER"/>
        #     </intent-filter>
        # </activity>
        # <activity android:enabled="false" android:excludeFromRecents="true" android:icon="@mipmap/app_icon" android:label="@string/app_name" android:name="com.squareup.leakcanary.internal.RequestStoragePermissionActivity" android:process=":leakcanary" android:roundIcon="@mipmap/app_icon" android:taskAffinity="com.squareup.leakcanary.com.unconditionalgames.waterpuzzle" />
   
        #   <!-- gdt ad end-->

          

    def SaveXml(self,filepath): 
        # FileUtil.SaveString2File(self.dom.toxml(),filepath)
        # f = open(filepath, "w")
        # writer = codecs.lookup('utf-8')[3](f)
        # self.dom.writexml(writer, newl='', indent='\n', encoding='utf-8')
        # writer.close()
        # f.close()
        fileHandle = open(filepath, 'w')
        # 写入操作，第二个参数为缩进（加在每行结束后），第三个为增量缩进（加在每行开始前并增量）
        self.dom.writexml(fileHandle, '\n', ' ', '', 'UTF-8')
        fileHandle.close()

mainAndroidManifest = AndroidManifest()
