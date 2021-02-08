#encoding:utf-8
#!/usr/bin/env python
# from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort,redirect,url_for
 
import time
import os
# from strUtil import Pic_str
import base64

import pytesseract

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
 
# @app.route('/upload_test')
@app.route('/upload_test', methods=['POST', 'GET'])
def upload_test():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_dir = os.path.join(basepath, 'upload')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        f.save(file_dir+"/"+f.filename)

        return redirect(url_for('upload'))

    return 'up.html'
 
 
# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        # fname = secure_filename(f.filename)
        # print (fname)
        print(f.filename)
        # ext = fname.rsplit('.', 1)[1]
        # new_filename = Pic_str().create_uuid() + '.' + ext
        new_filename = "save"
        f.save(os.path.join(file_dir, new_filename))
 
        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})
 
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        arg = request.files['arg']
        print("upload arg=",arg)
        
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_dir = os.path.join(basepath, 'upload')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        f.save(file_dir+"/"+f.filename)

        return redirect(url_for('upload'))

    return 'hello'



# http://mooncore.cn:5000/GetAppleCode
@app.route('/GetAppleCode', methods=['POST', 'GET'])
def GetAppleCode():
    if request.method == 'POST':
        print("GetAppleCode POST start")
        f = request.files['file']
        # region = request.files['arg']
        # print("GetAppleCode region=",region)
        
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_dir = os.path.join(basepath, 'upload')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        filepath = file_dir+"/"+f.filename
        f.save(filepath)

        # listtmp = region.split(",")
        # x = listtmp[0]
        # y = listtmp[1]
        # w = listtmp[2]
        # h = listtmp[3]
        # tangle=(x,y,x+w,y+h)
        # print("GetAppleCode tangle=",tangle)
        # # print(tangle)#(276, 274, 569, 464)
        # #打开123.png图片
        # img = Image.open(filepath)
        # #在123.png图片上 截取验证码图片
        # frame = img.crop(tangle)
        # #保存
        # frame.save(filepath)

        try:
            code = pytesseract.image_to_string(Image.open(filepath),lang="eng") 
        except:
            test=False

        print("GetAppleCode code=",code)
        return code

    return 'GetAppleCode'

# 上传文件
@app.route('/uploadfile', methods=['POST'], strict_slashes=False)
def uploadfile():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']
    if f and allowed_file(f.filename):
        # fname = secure_filename(f.filename)
        # print (fname)
        print(f.filename)
        # ext = fname.rsplit('.', 1)[1]
        # new_filename = Pic_str().create_uuid() + '.' + ext
        new_filename = "save"
        f.save(os.path.join(file_dir, new_filename))
 
        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)
        pass
    
    
# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass
 
 
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8887)
