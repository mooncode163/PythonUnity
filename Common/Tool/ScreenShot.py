import pyautogui 
 
# img = pyautogui.screenshot(region=[0,0,100,100]) # x,y,w,h
im = pyautogui.screenshot('screenshot.png',region=(0,0, 300, 400))
# img.save('screenshot.png') 