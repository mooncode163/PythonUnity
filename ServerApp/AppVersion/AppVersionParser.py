  
from flask import request
import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
sys.path.append("../../") 

from AppInfo import AppInfo
from DBApp import DBApp
from DBApp import mainDBApp

from AppVersionHuawei import mainAppVersionHuawei

class AppVersionParser():  
 
    def GetJson(self,version):
        strJson = "{}"
        dataRoot = json.loads(strJson)
        dataRoot["version"]=version
        json_str = json.dumps(dataRoot,ensure_ascii=False,indent=4,sort_keys = True)
        return json_str

    def GetVersion(self,cur_version,package,appid): 
        # print(request.url)
        # appinfo = AppInfo()
        # appinfo.appid= "100270155"
        # appinfo.package= "com.moonma.caicaile"
        # appinfo.version= "2.1.0"

        db = DBApp()
        db.OpenDB("DBApp.db") 
        
        version = db.GetVersionByPackage(package)
        print(" dbversion = ",version)
        if version<cur_version:
            version = mainAppVersionHuawei.ParseVersion(appid)
            appinfo = AppInfo()
            appinfo.appid= appid
            appinfo.package= package
            appinfo.version= version

            if db.IsItemExist(appinfo.package)==True: 
                db.UpdateItem(appinfo)
            else:
                # AddItem
                db.AddItem(appinfo)
            

        return self.GetJson(version)

        # return "1.0.0"

mainAppVersionParser = AppVersionParser() 
 
    