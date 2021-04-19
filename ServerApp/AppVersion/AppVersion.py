from flask import Flask
from AppVersionParser import mainAppVersionParser 
from AppVersionTapTap import mainAppVersionTapTap 

from flask import request
app = Flask(__name__)

# 在 Ubuntu 上使用 Nginx 部署 Flask 应用
# https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu
# sudo apt-get install python-setuptools
# sudo easy_install pip
# pip3 install virtualenv
# pip3 install flask
# pip3 install selenium


# ubuntu16.04上安装及使用selenium、chrome、chromedriver
# https://blog.csdn.net/shuchuan0409/article/details/101615221

# 在Ubuntu上安装Chrome浏览器和ChromeDriver
# https://www.cnblogs.com/z-x-y/p/9024622.html

# http://127.0.0.1:8080/
# http://47.242.56.146:8080/
@app.route('/')
def hello_world():
    return 'Hello World!'

# http://47.242.56.146:8080/AppVersion_huawei?cur_version=1.2.0&package=com.moonma.hanziyuan&appid=100278849
# http://mooncore.cn:8080/AppVersion_huawei?cur_version=1.2.0&package=com.moonma.caicaile&appid=100270155
# http://127.0.0.1:5000/AppVersion_huawei?cur_version=1.2.0&package=com.moonma.caicaile&appid=100270155
@app.route('/AppVersion_huawei')
def GetAppVersionHuawei():
    print(request.url)
    cur_version = request.args["cur_version"]
    package = request.args["package"]
    appid = request.args["appid"]
    print(cur_version)
    print(package)
    # return "2.0.0"
    return mainAppVersionParser.GetVersion(cur_version,package,appid)


# http://0.0.0.0:8080/AppVersion_taptap?cur_version=1.2.0&package=com.moonma.hanziyuan&appid=46445
@app.route('/AppVersion_taptap')
def GetAppVersionTapTap():
    print(request.url) 
    cur_version = request.args["cur_version"]
    package = request.args["package"]
    appid = request.args["appid"] 
    print(appid)
    # return "2.0.0"
    return mainAppVersionTapTap.GetVersion(cur_version,package,appid)

# http://mooncore.cn:8080/AppVersion?package=com.moonma.caicaile
@app.route('/AppVersion')
def GetAppVersion():
    print(request.url) 
    package = request.args["package"] 
    print(package)
    # return "2.0.0"
    return mainAppVersionParser.GetVersionByPackage(package)

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=8080)