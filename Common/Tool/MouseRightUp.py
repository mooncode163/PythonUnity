import pyautogui 
 

import os
import time

from pynput import mouse

import pynput, time

# 鼠标右键坏了 将鼠标中间按键按下模拟鼠标右键
def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    print(button)
    # Button.middle left right
    if button==pynput.mouse.Button.middle:
        pyautogui.rightClick()
        return True
    return True
 

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
with pynput.mouse.Listener(
        # on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
        
    listener.join()


# pyautogui.rightClick()
