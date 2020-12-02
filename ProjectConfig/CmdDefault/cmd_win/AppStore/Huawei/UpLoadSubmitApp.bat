
  
@set filepath = %~dp0 

cd ../../../../../../../Common/PythonUnity/ProjectConfig/Script

python AppStoreManager.py %~dp0 UpdateApk huawei
python AppStoreManager.py %~dp0 UpdateVersion huawei


@Pause

 


 
 