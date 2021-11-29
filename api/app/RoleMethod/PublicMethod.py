import base64
import hashlib
import string
from django.utils import timezone
import datetime
import time
import random
import jwt
from django.core.mail import send_mail
from django.db import connection
from django.core.cache import cache


class PublicMethod:
    def __init__(self):
        super(PublicMethod, self).__init__()
        self.JWT_SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='
        self.password = b'jhcoj_mxs'
        self.code_str = string.ascii_letters + string.digits
        self.ip = ""
        self.iss = "JHCOJ"

    # 生成密码
    def reg_pass(self, password):
        md5 = hashlib.md5(self.password)
        md5.update(password.encode(encoding='utf-8'))
        return md5.hexdigest()

    # 密码检查
    def check_password(self, password_new, password_old):
        if self.reg_pass(password_new) == password_old:
            # print(self.reg_pass(password_new), password_old)
            return True
        else:
            return False

    # 密码检查（旧用户注册密码验证）
    @staticmethod
    def check_password2(password_new, password_old):
        svg = base64.b64decode(bytes(password_old, 'utf-8'))
        svg = svg.decode('utf-8', 'ignore')
        salt = str(svg)[-4:]
        # print(svg)
        pas = password_new + salt
        pas = pas.encode('utf-8')
        code = hashlib.sha1(pas).digest()
        code = code.decode('utf-8', 'ignore')

        if code + salt == svg:
            return True
        else:
            return False

    # 获取用户ip
    def get_ip(self, requester):
        x_forwarded_for = requester.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            self.ip = requester.META.get('REMOTE_ADDR')  # 这里获得代理ip
        # print(ip)
        return self.ip

    def get_code(self, length):
        return ''.join(random.sample(self.code_str, length))

    # 生成后台验证码
    def capture(self, requester):
        code = self.get_code(length=4)  # 取5个长度为4的随机序
        # 将验证码存储在redis中
        ip = self.get_ip(requester)
        cache.set(ip, 60, code)
        code = {"capture": code}
        return code

    # 验证后台验证码是否正确
    def check_capture(self, requester, code):
        ip = self.get_ip(requester)
        get_code = cache.get(ip)
        if not get_code:
            return False
        if str(code).upper() == str(get_code.decode("utf-8", "ignore")).upper():
            return True
        else:
            return False

    # 生成邮箱验证码
    def email_code(self, email):
        code = self.get_code(length=6)
        cache.set(email, code, 3000)
        return code

    # 验证邮箱验证码是否正确
    def check_email_code(self, email, code):
        get_code = cache.get(email)
        if not get_code:
            return False
        if str(code).upper() == str(get_code).upper():
            return True
        else:
            return False

    # 发送邮件
    def send_email(self, user, email):
        get_code = self.email_code(email)
        cache.set(email, get_code, 600)
        res = send_mail(
            '52AC平台',
            f'{user}你好，感谢你使用金华职业技术学院的OJ平台，你本次的验证码是：{get_code}，请在10分钟内完成验证。',
            f'3488508834@qq.com',
            [f'{email}']
        )
        return res

    # 验证邮箱验证通过的邮箱
    def check_user_email(self, email, email_code):
        code = cache.get(email)
        if code == email_code:
            return True
        else:
            return False

    # 生成token
    def create_token(self, data, timeout=3):
        payload = {
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(minutes=timeout),
            "iss": self.iss,
            "data": data
        }
        result = jwt.encode(payload=payload, key=self.JWT_SALT, algorithm="HS256")
        return result

    # 对token进行和发行校验并获取payload
    def parse_payload(self, token):
        result = {
            'status': False,
            'remind': False,
            'time': timezone.now(),
            'data': None,
            'error': None,
            'new_token': None
        }
        try:
            verified_payload = jwt.decode(token, key=self.JWT_SALT, algorithms="HS256")
            result['status'] = True
            result['data'] = verified_payload
            if verified_payload['exp'] - int(time.time()) < 600:
                result['remind'] = True
                result['new_token'] = self.create_token(verified_payload['data'], 120)
        except jwt.ExpiredSignatureError:
            result['error'] = 'token已失效'
        except jwt.DecodeError:
            result['error'] = 'token认证失败'
        except jwt.InvalidTokenError:
            result['error'] = '非法的token'
        return result

    # 通过token获取用户信息
    def check_user_login(self, token):
        user_id = None
        if token:
            data = self.parse_payload(token)
            if data['status']:
                # user_id = data['data']['data']['username']
                user_id = data.get('data').get('data').get('user_id')
            else:
                user_id = None
        return user_id

    # 通过token获取用户昵称
    def get_user_nick(self, token):
        user_id = None
        if token:
            data = self.parse_payload(token)
            if data['status']:
                # user_id = data['data']['data']['username']
                user_id = data.get('data').get('data').get('user_nick')
            else:
                user_id = None
        return user_id

    # 通过token获取用户身份
    def get_user_capacity(self, token):
        capacity = 4
        if token:
            data = self.parse_payload(token)
            if data['status']:
                capacity = data.get('data').get('data').get('capacity')
        return capacity

    # 查询用户做题排名情况，传参为起始时间
    def get_rank_list_by_time(self, timer):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT USER.user_id, USER.user_name, USER.user_nick, t.submit, s.solved, USER.user_sex, w.success success FROM USER INNER JOIN ( SELECT COUNT( DISTINCT problem_id ) solved, user_id FROM solution WHERE solution_time > '{timer}' AND run_result = 4 GROUP BY user_id ORDER BY solved DESC ) s ON USER.user_id = s.user_id INNER JOIN ( SELECT count( solution_id ) success, user_id FROM solution WHERE solution_time > '{timer}' AND run_result = 4 GROUP BY user_id ORDER BY success DESC ) w ON USER.user_id = w.user_id INNER JOIN ( SELECT COUNT( problem_id ) submit, user_id FROM solution WHERE solution_time > '{timer}' GROUP BY user_id ORDER BY submit DESC ) t ON USER.user_id = t.user_id ORDER BY s.solved DESC, t.submit;")
            solution_data = cursor.fetchall()
        return_data = list(solution_data)
        return return_data

    # 查询用户做题排名情况，全部的排名
    def get_all_rank_list(self):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT USER.user_id user_id, USER.user_name user_name, USER.user_nick user_nick, t.submit submit, s.solved solved, USER.user_sex user_sex, w.success success FROM USER INNER JOIN ( SELECT count( DISTINCT problem_id ) solved, user_id FROM solution WHERE run_result = 4 GROUP BY user_id ORDER BY solved DESC ) s ON USER.user_id = s.user_id INNER JOIN ( SELECT count( solution_id ) success, user_id FROM solution WHERE run_result = 4 GROUP BY user_id ORDER BY success DESC ) w ON USER.user_id = w.user_id INNER JOIN ( SELECT COUNT( problem_id ) submit, user_id FROM solution GROUP BY user_id ORDER BY submit DESC ) t ON USER.user_id = t.user_id ORDER BY s.solved DESC,t.submit;")
            date = cursor.fetchall()
        return list(date)
