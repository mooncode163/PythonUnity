from flask import Flask 
from flask import request
import sys
app = Flask(__name__)
sys.path.append("../../") 

import requests
import platform  
import jwt 
import time
import datetime
import os
import json 
import base64
# import PyJWT
# from jwt import PyJWT
# 在 Ubuntu 上使用 Nginx 部署 Flask 应用
# https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu

# Google Play Developer API
# https://developer.android.google.cn/google/play/developer-api.html?hl=zh-cn


# jwt 和pyjwt 同时安装会出现下面的冲突 删除jwt
# 如果uninstall 无法删除就到E:\Python37\Lib\site-packages下面手动删除
# JWT: 'module' object has no attribute 'encode' 
# http://47.242.56.146:5000/AppleJWTToken
# http://127.0.0.1:5000/AppleJWTToken?keyid=com.moonma.caicaile&userid=100270155&KEY_PRIVATE=100270155
@app.route('/AppleJWTToken')
def AppleJWTToken():
    print(request.url)
    keyid = request.args["keyid"]
    userid = request.args["userid"] 
    KEY_PRIVATE = request.args["KEY_PRIVATE"] 
    return CreateJWTToken(keyid, userid,KEY_PRIVATE) 

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

def CreateJWTToken(keyid, userid,KEY_PRIVATE):
    print("keyid=",keyid," userid=",userid," KEY_PRIVATE=",KEY_PRIVATE)
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
    
    result = "result"
    # return result
    result = jwt.encode(payload=payload, key=KEY_PRIVATE,algorithm='ES256', headers=headers).decode('utf8')
    # result = jwt.encode(payload=payload, key=KEY_PRIVATE,algorithm='ES256', headers=headers).decode('utf8')
    # result = PyJWT.encode({'some' : 'payload'}, key= 'secret' , algorithm= 'RS256') 
    # print("CreateJWTToken =",result)

    # dic = {
    # 'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
    # 'iat': datetime.datetime.now(),  #  开始时间
    # 'iss': 'lianzong',  # 签名
    # 'data': {  # 内容，一般存放该用户id和开始时间
    #     'a': 1,
    #     'b': 2,
    # },
    # }

    # s = jwt.encode(dic, 'secret',key=KEY_PRIVATE, algorithm='ES256')  # 加密生成字符串      
    # print(s) 
    # print("，result=",result)
    return result

 
if __name__ == '__main__':
    # key_id = "MVG9NGFVX7"
    # key_private =  GetKEY_PRIVATE(key_id)
    # CreateJWTToken(key_id,"69a6de89-f844-47e3-e053-5b8c7c11a4d1",key_private)
    # app.run()
    app.run(host='0.0.0.0', port=5000)