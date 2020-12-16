 
import sys 
sys.path.append("../../") 

import requests
import platform  
import jwt 
import time
import datetime
import os
import json 
import base64 

import requests  

 

# http://127.0.0.1:5000/AppleJWTToken?keyid=com.moonma.caicaile&userid=100270155&KEY_PRIVATE=100270155
 
def GetUrl(url): 
    r = requests.get(url)
    return r.content.decode('utf-8',"ignore")

def GetFileString(filePath): 
    f = open(filePath, 'rb')
    strFile = f.read().decode('utf-8',"ignore")
    f.close()
    return strFile

def GetKEY_PRIVATE(API_KEY_ID):
    dir = os.getcwd()
    filepath = dir+"/AuthKey_"+API_KEY_ID+".p8"
    filepath = os.path.normpath(filepath)
    # print(filepath)
    KEY_PRIVATE = GetFileString(filepath)
    return KEY_PRIVATE
 
 
if __name__ == '__main__':
    key_id = "MVG9NGFVX7"
    user_id = "69a6de89-f844-47e3-e053-5b8c7c11a4d1"
    key_private =  GetKEY_PRIVATE(key_id)
    url = "http://47.242.56.146:5000/AppleJWTToken?keyid="+key_id+"&userid="+user_id+"&KEY_PRIVATE="+key_private
    print("url=",url)
    result = GetUrl(url)
    print("result=",result)
     