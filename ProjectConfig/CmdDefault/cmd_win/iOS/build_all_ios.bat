@echo  build_all_android
@set filepath = %~dp0 
@echo off
echo.| call ../copy_resource.bat
echo.| call unity_build_ios.bat
@Pause


