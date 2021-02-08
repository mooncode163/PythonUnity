import pytesseract
from PIL import Image
# https://www.cnblogs.com/BackingStar/p/11254120.html

# ubunut的话
# sudo add-apt-repository ppa:alex-p/tesseract-ocr
# sudo apt-get update 
# sudo apt-get install tesseract-ocr 

# pip3 install pillow
# pip3 install pytesseract  


if __name__ == '__main__':

    try: 
        text = pytesseract.image_to_string(Image.open("ImageNumber.png"),lang="eng")
        print(text)
    except Exception as e:  
        print("ImageNumber eror=",e)

