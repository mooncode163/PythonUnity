#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time
import datetime
import sys

sys.path.append('./common')
import common
import source

# 获取脚本文件的当前路径

 


# http://help.apple.com/itc/appsspec/#/itc6e4198248
# 主函数的实现
if __name__ == "__main__":

    
    count = len(sys.argv)
    for i in range(1,count):
        print ("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i]
    
    # common.SetCmdPath(cmdPath) 
    isUploadIPA = False
    isExportIPA = False
    if count > 1:
        argv1 = sys.argv[1]
        if argv1 == "upload_ipa":
            isUploadIPA = True 

        if argv1 == "export_ipa":
            isExportIPA = True 

            
    #  -u chyfemail163@163.com -p ayww-hcnh-uaau-lsgh
    # xcodebuild -list
    RootDir = common.GetRootProjectIos()
    target = "Unity-iPhone"
    xcode_project = common.GetRootDirXcode()+ "/Unity-iPhone.xcodeproj"
    archive_file = RootDir+"/app.xcarchive"
    # 不带后缀.ipa
    ipa_file = RootDir+"/app_inmobi/"+target
    exportOptionPlist_file = RootDir+"/ExportOptions.plist"
    
    

    if isUploadIPA == True:
        strCmd = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool --upload-app -f "+ipa_file+"/"+target+".ipa"+" -t ios -u "+source.APPSTORE_USER+" -p "+source.APPSTORE_PASSWORD
        os.system(strCmd)
    else:
        # build target.app
        # strCmd = "xcodebuild -project " + xcode_project + " -target " + "Unity-iPhone"
        # os.system(strCmd)

        

        # archive
        if isExportIPA==False:
            flag = os.path.exists(archive_file)
            if flag:
                shutil.rmtree(archive_file)

            flag = os.path.exists(ipa_file)
            if flag:
                shutil.rmtree(ipa_file)
                
            strCmd = "xcodebuild -allowProvisioningUpdates -project " + xcode_project + " -scheme " + target+" -configuration Release clean archive"+" -archivePath "+archive_file
            os.system(strCmd)

        # 导出ipa
        strCmd = "xcodebuild -allowProvisioningUpdates -exportArchive " +" -archivePath "+archive_file+" -exportPath "+ipa_file+" -exportOptionsPlist "+exportOptionPlist_file
        os.system(strCmd)

    
    print ("ipa_build sucess")
