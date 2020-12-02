@echo  build_all_android
@set filepath = %~dp0 
@echo off
echo.| call ../CopyResource.bat
echo.| call UnityBuildAndroid.bat
echo. | call ../UpdateAppInfoAuto.bat
echo.| call ApkBuildAll.bat
@Pause


