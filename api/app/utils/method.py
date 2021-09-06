import hashlib
import string
import random
from django.core.cache import cache
from django.core.mail import send_mail


class Method:
    def __init__(self):
        super(Method, self).__init__()
        self.password = b'LiSoul'
        self.code_str = string.ascii_letters + string.digits
        self.ip = ""
        self.iss = "LiSoul"

    # 生成密码
    def reg_pass(self, password):
        md5 = hashlib.md5(self.password)
        md5.update(password.encode(encoding='utf-8'))
        return md5.hexdigest()

    # 密码检查
    def check_password(self, password_new, password_old):
        print(self.reg_pass(password_new), password_old)
        return bool(
            self.reg_pass(password_new) == password_old
        )

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
        cache.set(ip, code, 600)
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
        if str(code).upper() == str(get_code.decode("utf-8", "ignore")).upper():
            return True
        else:
            return False

    # 发送邮件
    def send_email(self, user, email):
        get_code = self.email_code(email)
        res = send_mail(
            '52AC平台',
            f'{user}你好，感谢你使用金华职业技术学院的OJ平台，你本次的验证码是：{get_code}',
            f'3488508834@qq.com',
            [f'{email}']
        )
        return res

    # 设置邮箱验证时通过的邮箱
    def set_user_email(self, email):
        # print(email)
        cache.set(email, 'pass', 600)

    # 验证邮箱验证通过的邮箱
    def check_user_email(self, email):
        # print(email)
        code = cache.get(email)
        # print(code)
        if code == b'pass':
            return True
        else:
            return False

