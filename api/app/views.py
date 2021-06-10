from django.http import JsonResponse
from django.views.generic import View
from django.utils import timezone
from app.utils.PublicMethods import PublicMethod
from app.models import *

publicMethod = PublicMethod()


# --------------------------用户功能----------------------------
class Login(View):
    """
    模块: 用户登录
    接口信息:
        GET:
            None
        POST:
            user_id: 用户学号、工号
            password: 用户密码
            code: 图片验证码
    """
    def get(self, request):
        res = publicMethod.capture(requester=request)
        return JsonResponse(res)

    def post(self, request):
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if publicMethod.check_capture(requester=request, code=code):
            if Password.objects.using('app').filter(user_id=username):
                obj = Password.objects.using('app').get(user_id=username)
                if publicMethod.check_password(password_new=password, password_old=obj.password):
                    token = publicMethod.create_token({'username': obj.user_id}, 30)
                    LoginLog.objects.using('app').create(
                        user_id=username,
                        ip=publicMethod.get_ip(request),
                        time=timezone.now(),
                        login_way='JHCOJ'
                    )
                    massage = {'status': True, 'err': '登陆成功', 'token': token}
                else:
                    massage = {'status': False, 'err': '密码错误'}
            else:
                massage = {'status': False, 'err': '此用户未注册'}
        else:
            massage = {'status': False, 'err': '验证码错误'}
        return JsonResponse(massage)


class Logout(View):
    def get(self, request):
        token = request.GET.get('token')
        if token:
            data = publicMethod.parse_payload(token)
        else:
            data = "error"
        print(data)
        message = {'err': data}
        return JsonResponse(message)

    def post(self, request):
        message = {'err': '注销成功'}
        return JsonResponse(message)


class Register(View):
    """
    模块: 用户注册
    接口信息:
        GET:
            None
        POST:
            user_id: 用户学号、工号
            password: 用户密码
            check_pass: 重复密码
            code: 图片验证码
        """
    def get(self, request):
        res = publicMethod.capture(requester=request)
        return JsonResponse(res)

    def post(self, request):
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        check_pass = request.POST.get('check_pass')
        code = request.POST.get('code')
        if publicMethod.check_capture(request, code):
            if Password.objects.using('app').filter(user_id=username):
                state = {'status': False, 'err': '此用户已注册'}
            else:
                if password == check_pass:
                    Password.objects.using('app').create(user_id=username, password=publicMethod.reg_pass(password))
                    state = {'status': True, 'err': '注册成功'}
                else:
                    state = {'status': False, 'err': '密码输入不一致'}
        else:
            state = {'status': False, 'err': '验证码错误'}
        return JsonResponse(state)


class PerfectInfo(View):
    """
    模块: 用户信息获取，修改，完善
    接口信息:
        GET:
            token: token认证
        POST:
            token: token认证
            name: 用户姓名
            nickname: 用户昵称
            school: 用户所在学校
            sex: 用户性别{‘男’，‘女’}
        """
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': '用户未登录'})
        else:
            user_id = Password.objects.using('app').get(user_id=user_id)
        if User.objects.using('app').filter(user_id=user_id):
            obj = User.objects.using('app').filter(user_id=user_id).values().first()
            messages = {'status': True, 'err': '个人用户信息', 'data': obj}
        else:
            messages = {'status': False, 'err': '请先完善用户信息'}
        return JsonResponse(messages)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': "用户认证失败"})
        real_name = request.POST.get('name')
        nick_name = request.POST.get('nickname')
        school = request.POST.get('school')
        sex = request.POST.get('sex')
        sex = (0 if sex == '男' else 1)
        user_id = Password.objects.using('app').get(user_id=user_id)
        if User.objects.using('app').filter(user_id=user_id):
            obj = User.objects.using('app').get(user_id=user_id)
            if nick_name:
                obj.nick = nick_name
            if school:
                obj.school = school
            obj.ip = publicMethod.get_ip(request)
            obj.reg_time = timezone.now()
            obj.save()
            message = {'status': True, 'err': '信息修改成功'}
        else:
            User.objects.using('app').create(
                user_id=user_id,
                real_name=real_name,
                nick=nick_name,
                ip=publicMethod.get_ip(request),
                access_time=timezone.now(),
                reg_time=timezone.now(),
                school=school,
                sex=sex,
                role_pri=4,
                is_delete=0
            )
            message = {'status': True, 'err': '信息完善成功'}
        return JsonResponse(message)


class PasswordModification(View):
    """
    模块: 密码修改
    接口信息:
        GET:
            None
        POST:
            token: token认证
            old_password: 旧用户密码
            new_password: 新用户密码
            check_password: 重复密码
            code: 图片验证码
        """
    def get(self, request):
        res = publicMethod.capture(requester=request)
        return JsonResponse(res)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        check_password = request.POST.get('check_password')
        code = request.POST.get('code')
        obj = Password.objects.using('app').get(user_id=user_id)
        if publicMethod.check_password(password_new=old_password, password_old=obj.password):
            if new_password == check_password:
                if publicMethod.check_capture(requester=request, code=code):
                    obj.password = publicMethod.reg_pass(new_password)
                    obj.save()
                    message = {'status': True, 'err': '密码修改成功'}
                else:
                    message = {'status': False, 'err': '验证码错误'}
            else:
                message = {'status': False, 'err': '密码输入不一致'}
        else:
            message = {'status': False, 'err': '密码错误'}
        return JsonResponse(message)


class SendEmail(View):
    """
    模块: 邮件发送,认证
    接口信息:
        GET:
            token: token认证
            email: 邮箱（绑定邮箱时使用）
        POST:
            token: token认证
            code: 邮箱验证码
        """
    def get(self, request):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')
        email = request.GET.get('email')
        if not token or not publicMethod.parse_payload(token).get('status'):
            email = User.objects.using('app').get(user_id__user_id=user_id).email
            if not email:
                message = {'status': False, 'err': '邮箱未绑定'}
            else:
                if publicMethod.send_email(user_id, email):
                    message = {'status': True, 'err': '邮件发送成功', 'email': email}
                else:
                    message = {'status': False, 'err': '邮件发送失败', 'email': email}
        else:
            user_id = publicMethod.check_user_login(token)
            if user_id:
                if publicMethod.send_email(user_id, email):
                    message = {'status': True, 'err': '邮件发送成功', 'email': email}
                else:
                    message = {'status': False, 'err': '邮件发送失败', 'email': email}
            else:
                message = {'status': False, 'err': '用户认证失败'}
        return JsonResponse(message)

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        code = request.POST.get('code')
        if not token or not publicMethod.parse_payload(token).get('status'):
            email = User.objects.using('app').get(user_id__user_id=user_id).email
            if publicMethod.check_email_code(email=email, code=code):
                message = {'status': True, 'err': '邮箱验证通过'}
                publicMethod.set_user_email(user_id + email)
            else:
                message = {'status': False, 'err': '邮箱验证失败'}
        else:
            user_id = publicMethod.check_user_login(token)
            if publicMethod.check_email_code(email=email, code=code):
                message = {'status': True, 'err': '邮箱绑定成功'}
                obj = User.objects.using('app').get(user_id__user_id=user_id)
                obj.email = email
                obj.save()
            else:
                message = {'status': False, 'err': '邮箱验证失败'}
        return JsonResponse(message)


class ForgetPassword(View):
    """
    模块: 忘记密码
    接口信息:
        GET:
            None
        POST:
            user_id: 用户账号
            new_password: 新用户密码
            check_password: 重复密码
            code: 图片验证码
        """
    def get(self, request):
        res = publicMethod.capture(requester=request)
        return JsonResponse(res)

    def post(self, request):
        user_id = request.POST.get('user_id')
        new_password = request.POST.get('new_password')
        check_password = request.POST.get('check_password')
        code = request.POST.get('code')
        obj = Password.objects.using('app').get(user_id=user_id)
        if User.objects.using('app').filter(user_id=obj):
            user = User.objects.using('app').get(user_id=obj)
            if publicMethod.check_capture(requester=request, code=code):
                if new_password == check_password:
                    if publicMethod.check_user_email(user_id + user.email):
                        obj.password = publicMethod.reg_pass(new_password)
                        obj.save()
                        message = {'status': True, 'err': '密码重置成功'}
                    else:
                        message = {'status': False, 'err': '请先验证邮箱'}
                else:
                    message = {'status': False, 'err': '密码输入不一致'}
            else:
                message = {'status': False, 'err': '验证码错误'}
        else:
            message = {'status': False, 'err': '此用户信息未完善'}
        return JsonResponse(message)


class GetUserList(View):
    """
    模块: 获取用户信息列表
    接口信息:
        GET:
            None
        POST:
            None
        """
    def get(self, request):
        message = []
        obj = User.objects.using('app').all()
        for user in obj.values():
            message.append(user)
        return JsonResponse({"data": message})

    def post(self, request):
        pass


# ---------------------------问题功能---------------------------
class GetProblemList(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class GetProblemInfo(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class AddProblem(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ChangeProblem(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DeleteProblem(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


# ---------------------------新闻功能---------------------------
class GetNewsList(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class GetNewsInfo(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class AddNews(View):
    def get(self, request):
        pass

    def post(self, request):
        title = request.POST.get('title')
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')
        importance = request.POST.get('importance')
        image = request.POST.get('image')
        user_id = User.objects.using('app').get(user_id=user_id)
        obj = News.objects.using('app').create(
            user_id=user_id,
            title=title,
            content=content,
            time=timezone.now(),
            importance=importance,
            defunct=0,
            image=image
        )
        if obj:
            message = {'err': '创建成功'}
        else:
            message = {'err': '创建失败'}
        return JsonResponse(message)


class ChangeNews(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DeleteNews(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


# ---------------------------竞赛功能---------------------------
class GetContestList(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class GetContestInfo(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class AddContest(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ChangeContest(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DeleteContest(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
