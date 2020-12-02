@echo  unity_build
@set filepath = %~dp0 
 

c:/Python27/python unity_realtime_log.py -unity E:/Unity/2019.2.0f1/Editor/Unity.exe -project F:/sourcecode/unity/product/kidsgame/kidsgameUnity -method BuildPlayer.PerformAndroidBuild
  
@Pause
