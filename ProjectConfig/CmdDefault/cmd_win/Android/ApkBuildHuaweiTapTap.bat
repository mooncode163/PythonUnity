@echo  apk_build_huawei
@set filepath = %~dp0 

cd ../../../../../../Common/PythonUnity/ProjectConfig/Script
python ProjectManager.py %~dp0 ApkBuild taptap
python ProjectManager.py %~dp0 ApkBuild huawei

@Pause
