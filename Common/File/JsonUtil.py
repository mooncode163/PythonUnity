#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import json

from . import FileUtil

class JsonUtil():  
    @staticmethod  
    def SaveString2File(str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8',"ignore")
        f.write(b)
        f.close()

    @staticmethod  
    def SaveJson(filePath,dataRoot):   
        # 保存json 
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True).encode('utf8',"ignore")
        json_str = json.dumps(dataRoot,ensure_ascii=False,indent=4,sort_keys = True)
        JsonUtil.SaveString2File(json_str,filePath)
        # json.dumps(dataRoot, f, ensure_ascii=False,indent=4,sort_keys = True)

    @staticmethod  
    def IsContainKey(data, key):
        if  (key  in  data) :
            return True
        
        return False
 