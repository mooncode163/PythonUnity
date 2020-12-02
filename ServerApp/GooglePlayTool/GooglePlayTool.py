from flask import Flask 
from flask import request
import sys
app = Flask(__name__)
sys.path.append("../../") 
from Common.Common import Common
from ProjectConfig.Script.AppStore.GooglePlayApi import mainGooglePlayApi
from ProjectConfig.Script.AppStore.AppStoreGoogleInternal import mainAppStoreGoogleInternal
from ProjectConfig.Script.Project.Resource import mainResource

# 在 Ubuntu 上使用 Nginx 部署 Flask 应用
# https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu

# Google Play Developer API
# https://developer.android.google.cn/google/play/developer-api.html?hl=zh-cn


# http://127.0.0.1:5000/GooglePlayDeveloperAPI/CreateApp?package=com.moonma.caicaile&name=100270155
@app.route('/GooglePlayDeveloperAPI/CreateApp')
def CreateApp():
    print(request.url)
    # package = request.args["package"]
    # # name = request.args["name"]
    # mainAppStoreGoogleInternal.apptype = request.args["apptype"]
    # mainAppStoreGoogleInternal.appkey = request.args["appkey"] 
    mainResource.SetCmdPath(request.args["path"])
    mainAppStoreGoogleInternal.Run("createapp",False)
    return "CreateApp"

@app.route('/GooglePlayDeveloperAPI/UploadScreenShot')
def UploadScreenShot():
    print(request.url)
    # package = request.args["package"]
    # name = request.args["name"]
    # mainAppStoreGoogleInternal.apptype = request.args["apptype"]
    # mainAppStoreGoogleInternal.appkey = request.args["appkey"]
    mainResource.SetCmdPath(request.args["path"])
    mainAppStoreGoogleInternal.Run("screenshot",False)
    return "UploadScreenShot"

@app.route('/GooglePlayDeveloperAPI/UpdateAppInfo')
def UpdateAppInfo():
    print(request.url)
    # package = request.args["package"]
    # name = request.args["name"]
    # mainAppStoreGoogleInternal.apptype = request.args["apptype"]
    # mainAppStoreGoogleInternal.appkey = request.args["appkey"]
    mainResource.SetCmdPath(request.args["path"])
    mainAppStoreGoogleInternal.Run("UpdateAppInfo",False)
    return "UpdateAppInfo"

@app.route('/GooglePlayDeveloperAPI/UpdateApk')
def UpdateApk():
    print(request.url)
    # package = request.args["package"]
    # name = request.args["name"]
    # mainAppStoreGoogleInternal.apptype = request.args["apptype"]
    # mainAppStoreGoogleInternal.appkey = request.args["appkey"]
    mainResource.SetCmdPath(request.args["path"])
    mainAppStoreGoogleInternal.Run("UpdateApk",False)
    return "UpdateApk"

 
if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=8080)