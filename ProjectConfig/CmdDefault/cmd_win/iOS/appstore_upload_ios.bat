
  
@set filepath = %~dp0 

cd ../../../../../../Common/PythonUnity/ProjectConfig/Script 
python appstore_upload_ios.py %~dp0
# http://help.apple.com/itc/appsspec/#/itc6e4198248
# /Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/itms/bin/iTMSTransporter -m upload -u chyfemail163@163.com -p ayww-hcnh-uaau-lsgh -f ./appstore/ios/app.itmsp -v eXtreme
python update_appstore.py $filepath delete_screenshot

@Pause

 


 
 
 