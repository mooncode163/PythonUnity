@echo  apk_build_gp
@set filepath = %~dp0 

cd ../../../../../../Common/PythonUnity/ProjectConfig/Script

python ProjectManager.py %~dp0 ApkBuild gp

@Pause