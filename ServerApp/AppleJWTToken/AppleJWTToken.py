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

import pytesseract
from PIL import Image

smsCode = ""
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

# http://47.242.56.146:5000/GetSmsCode
@app.route('/GetSmsCode')
def GetSmsCode():
    print(request.url)
    global smsCode
    return smsCode 

# http://47.242.56.146:5000/SetSmsCode?code=123456
@app.route('/SetSmsCode')
def SetSmsCode():
    print(request.url) 
    global smsCode
    smsCode = request.args["code"]
    return smsCode 

# http://mooncore.cn:5000/GetAppleCode
@app.route('/GetAppleCode', methods=['POST', 'GET'])
def GetAppleCode():
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    file_dir = os.path.join(basepath, 'upload')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    

    if request.method == 'POST':
        f = request.files['file']
        # region = request.files['arg']
        # print("GetAppleCode region=",region)
        
        filepath = file_dir+"/"+f.filename

        f.save(filepath)

        oft = 50
        x = 1220
        y = 540
        w = 200
        h = 50

        # listtmp = region.split(",")
        # x = listtmp[0]
        # y = listtmp[1]
        # w = listtmp[2]
        # h = listtmp[3]
        tangle=(x,y,x+w,y+h)
        print("GetAppleCode tangle=",tangle)
        # print(tangle)#(276, 274, 569, 464)
        #打开123.png图片
        img = Image.open(filepath)
        #在123.png图片上 截取验证码图片
        frame = img.crop(tangle)
        #保存
        frame.save(filepath)


        code = pytesseract.image_to_string(Image.open(filepath),lang="eng") 
        print("GetAppleCode code=",code)
        return code

    if request.method == 'GET':
        filepath = file_dir+"/"+"screenshot.png"
        code = pytesseract.image_to_string(Image.open(filepath),lang="eng") 
        print("GetAppleCode code=",code)
        return code

    return 'GetAppleCode'

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