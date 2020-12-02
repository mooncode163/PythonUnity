@echo  apk_build_taptap
@set filepath = %~dp0 

cd ../../../../../../Common/PythonUnity/ProjectConfig/Script

python ProjectManager.py %~dp0 ApkBuild taptap

@Pause
