import base64
import hashlib
import string
from asyncio import exceptions
import datetime
import random
import jwt
from django_redis import get_redis_connection
from django.db import connection
from django.http import FileResponse
from app.config import config
from django.http import JsonResponse, request

redis = get_redis_connection()
JWT_SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


class PublicMethod:
    def __init__(self):
        super(PublicMethod, self).__init__()
        self.password = b'jhcoj_mxs'
        self.code_str = string.ascii_letters + string.digits

    def reg_pass(self, password):
        md5 = hashlib.md5(self.password)
        md5.update(password.encode(encoding='utf-8'))
        return md5.hexdigest()

    def check_password(self, password_new, password_old):
        if self.reg_pass(password_new) == password_old:
            # print(self.reg_pass(password_new), password_old)
            return True
        else:
            return False

    # 获取用户ip
    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        # print(ip)
        return ip

    def gen_code(self, len):
        return ''.join(random.sample(self.code_str, len))

    # 验证验证码是否正确
    def check_capture(self, request, code):
        ip = self.get_ip(request)
        get_code = redis.get(ip)
        if not get_code:
            return False
        if str(code).upper() == str(get_code.decode("utf-8", "ignore")).upper():
            return True
        else:
            return False

    # 后台生成验证码
    def capture(self, request):
        code = self.gen_code(len=4)  ##取5个长度为4的随机序
        # 将验证码存储在redis中
        ip = self.get_ip(request)
        res = redis.setex(ip, 60, code)
        code = {"capture": code}
        return code

    # 生成token
    def create_token(self, payload, timeout=3):

        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
        result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
        return result

    # 对token进行和发行校验并获取payload
    def parse_payload(self, token):

        result = {'status': False, 'data': None, 'error': None}
        try:
            verified_payload = jwt.decode(token, JWT_SALT, True)
            result['status'] = True
            result['data'] = verified_payload
        except exceptions.ExpiredSignatureError:
            result['error'] = 'token已失效'
        except jwt.DecodeError:
            result['error'] = 'token认证失败'
        except jwt.InvalidTokenError:
            result['error'] = '非法的token'
        return result
