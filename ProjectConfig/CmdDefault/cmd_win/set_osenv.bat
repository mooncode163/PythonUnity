@echo  unity_build
@set filepath = %~dp0 

cd ../../../../../Common/PythonUnity/ProjectConfig/Script

python set_osenv.py %~dp0
  
@Pause
