@echo  build_huawei
@set filepath = %~dp0 
@echo off
filepath = %~dp0  
cd ../
echo.| call CopyResource.bat
cd %~dp0
echo.| call UnityBuildAndroid.bat
cd ../
echo.| call UpdateAppInfoAuto.bat
cd %~dp0
echo.| call ApkBuildGP.bat
@Pause
