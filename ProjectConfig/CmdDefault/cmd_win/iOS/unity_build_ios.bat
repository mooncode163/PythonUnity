@echo  unity_build
@set filepath = %~dp0 

cd ../../../../../../Common/PythonUnity/ProjectConfig/Script

python unity_build.py %~dp0 ios
  
@Pause
