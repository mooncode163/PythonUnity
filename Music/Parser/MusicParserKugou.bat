@echo  apk_build_huawei
@set filepath = %~dp0 
cd ../../
python Music/Parser/MusicParserKugou.py %~dp0 

@Pause
