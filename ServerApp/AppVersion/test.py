# from pyvirtualdisplay import Display
# pip3 install pyvirtualdisplay

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
# display = Display(visible=0, size=(800, 600))　　# 初始化屏幕 display.start()　　
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options) 

driver.get('http://www.cnblogs.com/x54256/')

print(driver.title)