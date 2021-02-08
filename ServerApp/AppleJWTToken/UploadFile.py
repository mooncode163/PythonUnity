import requests
from urllib3 import encode_multipart_formdata
 

def UploadFile(url,filename, file_path):
	"""
	:param filename：文件的名称
	:param file_path：文件的绝对路径
	"""
	
	with open(file_path, "rb")as f:
    # with open(file_path, mode="r", encoding="utf8") as f : 
		file = {
				"file": (filename, f.read()),# 引号的file是接口的字段，后面的是文件的名称、文件的内容
				"key": "value", # 如果接口中有其他字段也可以加上
					} 
		
		encode_data = encode_multipart_formdata(file)
		
		file_data = encode_data[0] 
		# b'--c0c46a5929c2ce4c935c9cff85bf11d4\r\nContent-Disposition: form-data; name="file"; filename="1.txt"\r\nContent-Type: text/plain\r\n\r\n...........--c0c46a5929c2ce4c935c9cff85bf11d4--\r\n
		
		headers_from_data = {
					"Content-Type": encode_data[1]
					# "Authorization": token
							} 
		# token是登陆后给的值，如果你的接口中头部不需要上传字段，就不用写，只要前面的就可以
		# 'Content-Type': 'multipart/form-data; boundary=c0c46a5929c2ce4c935c9cff85bf11d4'，这里上传文件用的是form-data,不能用json
		
		# response = requests.post(url=url, headers=headers_from_data, data=file_data).json()
		response = requests.post(url=url, headers=headers_from_data, data=file_data)
		return response
		

if __name__=='__main__':
    # 上传图片
	url = 'http://127.0.0.1:8887/upload' 
	UploadFile(url,"2.png","uploadfile.png")

	# print(res)
	 