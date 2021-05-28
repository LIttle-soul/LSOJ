from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.utils import timezone
from app.utils.PublicMethods import PublicMethod
from app.models import *


publicMethod = PublicMethod()


# --------------------------用户功能----------------------------
class Login(View):
    def get(self, request):
        res = publicMethod.capture(request=request)
        return JsonResponse(res)

    def post(self, request):
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if publicMethod.check_capture(request=request, code=code):
            if Password.objects.filter(user_id=username):
                obj = Password.objects.get(user_id=username)
                if publicMethod.check_password(password_new=password, password_old=obj.password):
                    token = publicMethod.create_token({'username': obj.user_id})
                    massage = {'err': '登陆成功', 'token': token}
                else:
                    massage = {'err': '密码错误'}
            else:
                massage = {'err': '此用户未注册'}
        else:
            massage = {'err': '验证码错误'}
        return JsonResponse(massage)


class Logout(View):
    def get(self, request):
        status = request.session.get('is_login')
        if not status:
            message = {'err': '请先登录'}
        else:
            message = {'err': '登陆成功'}
        return JsonResponse(message)

    def post(self, request):
        message = {'err': '注销成功'}
        return JsonResponse(message)


class Register(View):
    def get(self, request):
        res = publicMethod.capture(request=request)
        return JsonResponse(res)

    def post(self, request):
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        check_pass = request.POST.get('checkPass')
        code = request.POST.get('code')
        if publicMethod.check_capture(request, code):
            if Password.objects.filter(user_id=username):
                state = {'err': '此用户已注册'}
            else:
                if password == check_pass:
                    Password.objects.create(user_id=username, password=publicMethod.reg_pass(password))
                    state = {'err': '注册成功'}
                else:
                    state = {'err': '密码输入不一致'}
        else:
            state = {'err': '验证码错误'}
        return JsonResponse(state)


class PerfectInfo(View):
    def get(self, request):
        pass

    def post(self, request):
        user_id = request.POST.get('user_id')
        real_name = request.POST.get('name')
        nick_name = request.POST.get('nickname')
        email = request.POST.get('email')
        school = request.POST.get('school')
        sex = request.POST.get('sex')
        sex = (0 if sex == '男' else 1)
        user_id = Password.objects.get(user_id=user_id)
        if User.objects.filter(user_id=user_id):
            obj = User.objects.get(user_id=user_id)
            if obj.email != email and User.objects.filter(email=email):
                message = {'err': '此邮箱已注册'}
            else:
                obj.real_name = real_name
                obj.nick = nick_name
                obj.email = email
                obj.ip = publicMethod.get_ip(request)
                obj.reg_time = timezone.now()
                obj.school = school
                obj.sex = sex
                obj.save()
                message = {'err': '信息修改成功'}
        else:
            if User.objects.filter(email=email):
                message = {'err': '此邮箱已注册'}
            else:
                User.objects.create(
                    user_id=user_id,
                    real_name=real_name,
                    nick=nick_name,
                    email=email,
                    ip=publicMethod.get_ip(request),
                    access_time=timezone.now(),
                    reg_time=timezone.now(),
                    school=school,
                    sex=sex,
                    role_pri=4,
                    is_delete=0
                )
                message = {'err': '信息完善成功'}
        return JsonResponse(message)


class PasswordModification(View):
    def get(self, request):
        pass

    def post(self, request):
        user_id = request.POST.get('user_id')
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        check_password = request.POST.get('checkPassword')
        obj = Password.objects.get(user_id=user_id)
        if publicMethod.check_password(password_new=old_password, password_old=obj.password):
            if new_password == check_password:
                obj.password = publicMethod.reg_pass(new_password)
                obj.save()
                message = {'err': '密码修改成功'}
            else:
                message = {'err': '密码输入不一致'}
        else:
            message = {'err': '密码错误'}
        return JsonResponse(message)


class ForgetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class GetUserList(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class GetUserInfo(View):
    def get(self, request):
        pass

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
        user_id = User.objects.get(user_id=user_id)
        obj = News.objects.create(
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
