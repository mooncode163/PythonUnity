import jwt
import datetime

dic = {
    'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
    'iat': datetime.datetime.now(),  #  开始时间
    'iss': 'lianzong',  # 签名
    'data': {  # 内容，一般存放该用户id和开始时间
        'a': 1,
        'b': 2,
    },
}
 # 加密生成字符串
s = jwt.encode(dic, 'secret', algorithm='HS256') 
print(s)
# s = jwt.JWT.decode(s, 'secret', issuer='lianzong', algorithms=['HS256'])  # 解密，校验签名
# print(s)
# print(type(s))