@echo  apk_build_gp
@set filepath = %~dp0 

cd ../script
python build_all_games.py %~dp0 ios
  
@Pause
