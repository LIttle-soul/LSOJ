from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.utils import timezone
from app.RoleMethod.PublicMethod import PublicMethod
from app.serialize.serializer_user import *
import base64

publicMethod = PublicMethod()


class Login(View):
    """
    模块: 用户登录
    接口信息:
        POST:
            user_id: 用户学号、工号
            password: 用户密码
    返回信息:
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
            token: 登陆成功时的token
    """
    def post(self, request):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        obj = Password.objects.filter(user_id=user_id)
        if obj.exists():
            obj = obj.first()
            if publicMethod.check_password(password_new=password, password_old=obj.password):
                LoginLog.objects.create(
                    user_id=user_id,
                    login_ip=publicMethod.get_ip(request),
                    login_time=timezone.now(),
                    login_way='JHCOJ'
                )
                user = User.objects.filter(user_id=user_id).first()
                if user and user.user_status == 0:
                    return JsonResponse({'status': False, 'message': '你被封号了！想再登入请联系管理员或老师！'})
                token = uuid.uuid4().hex
                cache.set(token, user_id, 7200)  # 将token存入缓存有效期120分钟
                message = {'status': True, 'message': '登录成功', 'token': token}
            else:
                message = {'status': False, 'message': '密码错误'}
        else:
            message = {'status': False, 'message': '此账号未注册'}
        return JsonResponse(message)


class Register(View):
    """
    模块: 用户注册
    接口信息:
        POST:
            user_id: 用户学号、工号
            password: 用户密码
            check_password: 重复密码
    返回信息:
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
    """
    def post(self, request):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        check_password = request.POST.get('check_password')
        obj = Password.objects.filter(user_id=user_id)
        if obj.exists():
            message = {'status': False, 'message': '此用户已注册'}
        else:
            if password == check_password:
                Password.objects.create(
                    user_id=user_id,
                    password=publicMethod.reg_pass(password),
                    registration_time=timezone.now()
                )
                token = uuid.uuid4().hex
                cache.set(token, user_id, 1200)
                message = {'status': True, 'message': '注册成功', 'token': token}
            else:
                message = {'status': False, 'message': '密码输入不一致'}
        return JsonResponse(message)


class ForgetPassword(View):
    """
    模块: 忘记密码
    接口信息:
        POST:
            user_id: 用户账号
            new_password: 新用户密码
            check_password: 重复密码
            email_code: 邮箱验证码
    返回信息:
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
    """
    def post(self, request):
        user_id = request.POST.get('user_id')
        new_password = request.POST.get('new_password')
        check_password = request.POST.get('check_password')
        email_code = request.POST.get('email_code')
        obj = Password.objects.filter(user_id=user_id)
        user_obj = User.objects.filter(user_id=user_id)
        if user_obj.exists() and obj.exists():
            user = user_obj.first()
            if new_password == check_password:
                new_password = publicMethod.reg_pass(new_password)
                password = obj.first()
                if password.password != new_password:
                    if user.user_email:
                        if publicMethod.check_user_email(user.user_email, email_code):
                            password.password = new_password
                            password.save()
                            message = {'status': True, 'message': '密码修改成功'}
                        else:
                            message = {'status': False, 'message': '邮箱验证失败，请确认是否输入正确'}
                    else:
                        message = {'status': False, 'message': '未绑定邮箱，请联系老师或管理员修改'}
                else:
                    message = {'status': False, 'message': '新密码不能和原密码相同'}
            else:
                message = {'status': False, 'message': '密码输入不一致'}
        else:
            message = {'status': False, 'message': '此用户信息未完善'}
        return JsonResponse(message)


class SendEmail(View):
    """
    模块: 邮件发送,认证
    接口信息:
        GET:
            token: token认证（绑定邮箱时使用）
            user_id: 用户账号（找回密码时使用）
            email: 邮箱（绑定邮箱时使用）
        POST:
            token: token认证（绑定邮箱时使用）
            email: 邮箱（绑定邮箱时使用）
            email_code: 邮箱验证码
    返回信息:
        GET:
            status: 邮件发送状态
            message: 提示信息
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        email = request.GET.get('email')
        if not user_id:
            user_id = request.GET.get('user_id')
            obj = User.objects.filter(user_id=user_id)
            if not obj.exists():
                return JsonResponse({'status': False, 'message': '此用户未完善任何信息！！'})
            email = obj.first().user_email
            if not email:
                message = {'status': False, 'message': '邮箱未绑定'}
            else:
                if publicMethod.send_email(user_id, email):
                    message = {'status': True, 'message': '邮件发送成功', 'email': email}
                else:
                    message = {'status': False, 'message': '邮件发送失败', 'email': email}
        else:
            if publicMethod.send_email(user_id, email):
                message = {'status': True, 'message': '邮件发送成功', 'email': email}
            else:
                message = {'status': False, 'message': '邮件发送失败', 'email': email}
        return JsonResponse(message)

    def post(self, request):
        token = request.COOKIES.get('token')
        email = request.POST.get('email')
        email_code = request.POST.get('code')
        user_id = cache.get(token)
        print(email, email_code)
        if publicMethod.check_email_code(email, email_code):
            message = {'status': True, 'message': '邮箱绑定成功'}
            obj = User.objects.get(user_id=user_id)
            obj.user_email = email
            obj.save()
        else:
            message = {'status': False, 'message': '邮箱验证失败'}
        return JsonResponse(message)


class PerfectInfo(View):
    """
    模块: 用户信息获取，修改，完善
    接口信息:
        GET:
            token: token认证
        POST:
            token: token认证
            user_name: 用户姓名
            user_nick: 用户昵称
            user_introduce: 用户介绍
            user_telephone: 用户电话
            user_birthday: 用户生日
            user_school: 用户所在学校编号
            user_class: 用户所在班级编号
            user_address: 用户所在地区编号
            user_sex: 用户性别{‘男’，‘女’}
    返回信息:
        GET:
            status: 数据请求状态
            message: 提示信息
            data: 用户个人的信息包
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            data = JsonResponse({'status': False, 'message': '用户未登录'})
            data.delete_cookie('token')
            return data
        cache.touch(token, 7200)
        obj = User.objects.filter(user_id=user_id)
        if obj.exists():
            user = obj.first()
            if user.user_address is None:
                address_name = ''
            else:
                address_num = len(user.user_address.split(','))
                user_address = user.user_address.split(',')[-1]
                if address_num == 1 and user.user_address:
                    address = Province.objects.filter(province_id=user_address).first()
                    address_name = address.province_name
                elif address_num == 2:
                    address = Municipality.objects.filter(municipality_id=user_address).first()
                    address_name = address.municipality_name
                elif address_num == 3:
                    address = District.objects.filter(district_id=user_address).first()
                    address_name = address.district_name
                elif address_num == 4:
                    address = Township.objects.filter(township_id=user_address).first()
                    address_name = address.township_name
                elif address_num == 5:
                    address = Village.objects.filter(village_id=user_address).first()
                    address_name = address.village_name
                else:
                    address_name = ''
            user_school = user.user_school.split(',')[-1]
            school = School.objects.filter(school_id=user_school).first()
            if school:
                school_name = school.school_name
            else:
                school_name = ''
            data = {
                'student_id': user.student_id,
                'user_address': None if user.user_address is None or user.user_address == '' else {
                    'address_id': user.user_address,
                    'address_name': address_name,
                },
                'user_birthday': user.user_birthday,
                'user_email': user.user_email,
                'user_id': user.user_id,
                'user_introduce': user.user_introduce,
                'user_name': user.user_name,
                'user_nick': user.user_nick,
                'user_power': user.user_power,
                'user_school': None if user.user_school is None else {
                    'school_id': user.user_school,
                    'school_name': school_name,
                },
                'user_score': user.user_score,
                'user_sex': user.user_sex,
                'user_telephone': user.user_telephone,
                'registration_time': Password.objects.filter(user_id=user_id).first().registration_time,
                'user_icon': user.user_icon
            }
            message = {'status': True, 'message': '个人用户信息', 'data': data}
        else:
            message = {'status': True, 'message': '请先完善用户信息'}
        return JsonResponse(message)

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        print(token, user_id)
        if not user_id:
            return JsonResponse({'status': False, 'message': "登录已失效"})
        user_name = request.POST.get('user_name')
        user_nick = request.POST.get('user_nick')
        user_introduce = request.POST.get('user_introduce')
        user_telephone = request.POST.get('user_telephone')
        user_sex = request.POST.get('user_sex')
        user_birthday = request.POST.get('user_birthday')
        user_school = request.POST.get('user_school')
        user_address = request.POST.get('user_address')
        print(user_name, user_nick, user_introduce, user_telephone, user_sex, user_birthday, user_school, user_address)
        obj = User.objects.filter(user_id=user_id)
        if obj.exists():
            obj = obj.first()
            obj.user_nick = user_nick
            obj.user_name = user_name
            obj.user_sex = user_sex
            obj.user_introduce = user_introduce
            obj.user_telephone = user_telephone
            obj.user_birthday = user_birthday
            obj.user_school = user_school
            obj.user_address = user_address
            obj.save()
            message = {'status': True, 'message': '信息修改成功'}
        else:
            User.objects.create(
                user_id=user_id,
                user_name=user_name,
                user_nick=user_nick,
                user_introduce=user_introduce,
                user_power=4,
                user_score=0,
                user_birthday=user_birthday,
                user_sex=user_sex,
                user_telephone=user_telephone,
                user_school=user_school,
                user_address=user_address,
            )
            message = {'status': True, 'message': '信息完善成功'}
        return JsonResponse(message)


class GetUserList(View):
    """
    模块: 获取用户信息列表,修改用户信息,删除用户
    接口信息:
        GET:
            None
        PUT:
            token: token认证
            put_user: 修改用户id
            user_status: 用户状态
            user_password: 用户密码
        DELETE:
            token: token认证
            delete_user: 要删除的用户
    返回信息:
        GET:
            status: 数据请求状态
            message: 所有的用户列表
        PUT:
            status: 数据请求状态
            message: 提示信息
        DELETE:
            status: 数据请求状态
            message: 提示信息
    """
    def get(self, request):
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        user_id = request.GET.get('user_id')
        user = User.objects.all()
        if not user_id:
            if text:
                user = user.filter(Q(user_id__contains=text) | Q(user_nick__contains=text) | Q(user_name__contains=text))
        else:
            user = user.filter(user_id=user_id)
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在'})
        user_num = user.count()
        if total != '0':
            user = user[(int(page) - 1) * int(total): int(page) * int(total)]
        message = []
        for data in user:
            school_name = ''
            if data.user_school:
                user_school = data.user_school.split(',')[-1]
                school_name = School.objects.filter(school_id=user_school).first().school_name
            message.append({
                'user_id': data.user_id,
                'student_id': data.student_id,
                'user_name': data.user_name,
                'user_nick': data.user_nick,
                'user_power': data.user_power,
                'user_score': data.user_score,
                'user_sex': data.user_sex,
                'user_telephone': data.user_telephone,
                'user_email': data.user_email,
                'user_birthday': data.user_birthday,
                'school': {
                    'school_id': data.user_school,
                    'school_name': school_name
                },
                'user_status': data.user_status,
                'user_registration_time': Password.objects.filter(user_id=data.user_id).first().registration_time
            })
        return JsonResponse({'status': True, 'message': message, 'total': user_num})

    def put(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse(({'status': False, 'message': '未登录'}))
        capacity = User.objects.filter(user_id=user_id).first().user_power
        put_user = request.GET.get('user_id')
        user_power = request.GET.get('user_power')
        user_status = request.GET.get('user_status')
        user_password = request.GET.get('user_password')
        print(put_user, user_power, user_status, user_password)
        user = User.objects.filter(user_id=put_user).first()
        if not user:
            return JsonResponse({'status': False, 'message': '此用户不存在'})
        if capacity > 2 or (capacity != 0 and user.user_power <= capacity) or (user_power is not None and capacity != 0 and int(user_power) <= capacity):
            return JsonResponse({'status': False, 'message': '权限不足'})
        if user_power:
            user.user_power = user_power
        if user_status:
            if user_status in ['false', 'FALSE']:
                user_status = False
            elif user_status in ['true', 'TRUE']:
                user_status = True
            user.user_status = user_status
        if user_password:
            password = Password.objects.filter(user_id=put_user).first()
            password.password = publicMethod.reg_pass(user_password)
            password.save()
        user.save()
        return JsonResponse({'status': True, 'message': '修改成功'})

    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        print(user_id)
        if not user_id:
            return JsonResponse(({'status': False, 'message': '未登录'}))
        me = User.objects.filter(user_id=user_id).first()
        if not me:
            return JsonResponse({'status': False, 'message': '未完善信息'})
        capacity = me.user_power
        delete_user = request.GET.get('user_id')
        print(user_id, delete_user)
        user = User.objects.filter(user_id=delete_user).first()
        if not user:
            return JsonResponse({'status': False, 'message': '此用户不存在'})
        if capacity > 1 or (capacity != 0 and user.user_power <= capacity):
            return JsonResponse({'status': False, 'message': '权限不足'})
        Password.objects.filter(user_id=delete_user).delete()
        user.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})


class GetUserStatus(View):
    """
    模块: 获取所有用户提交列表
    接口信息:
        GET:
            token: token认证
    返回信息:
        GET:
            status: 数据请求状态
            message: 所有的用户提交列表
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = request.GET.get('user_id')
        if user_id is None:
            user_id = cache.get(token)
        if user_id is None:
            return JsonResponse({'status': False, 'message': '未登录'})
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '信息没有完善'})
        school = School.objects.filter(school_id=user.user_school)
        if school.exists():
            school_name = school.first().school_name
        else:
            school_name = None
        message = {
            'solution': Solution.objects.filter(user_id=user_id, run_result=4).values('problem_id').distinct().count(),
            'submit': Solution.objects.filter(user_id=user_id).count(),
            'accepted': Solution.objects.filter(user_id=user_id, run_result=4).count(),
            'presentation_error': Solution.objects.filter(user_id=user_id, run_result=5).count(),
            'time_limit_exceeded': Solution.objects.filter(user_id=user_id, run_result=6).count(),
            'memory_limit_exceeded': Solution.objects.filter(user_id=user_id, run_result=7).count(),
            'wrong_answer': Solution.objects.filter(user_id=user_id, run_result=8).count(),
            'runtime_error': Solution.objects.filter(user_id=user_id, run_result=9).count(),
            'output_limit_exceeded': Solution.objects.filter(user_id=user_id, run_result=10).count(),
            'compile_error': Solution.objects.filter(user_id=user_id, run_result=11).count(),
            'school': school_name
        }
        return JsonResponse({'status': True, 'message': message})


class UserStatus(View):
    """
    模块: 获取身份状态
    接口信息:
        GET:
            token: token认证
            user_id: 别人的用户ID
    返回信息:
        GET:
            status: 数据请求状态
            message: 用户身份状态
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = request.GET.get('user_id')
        if not user_id:
            user_id = cache.get(token)
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '用户不存在'})
        solutions = Solution.objects.filter(user_id=user_id)
        problem_list = {}
        stats_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for solution in solutions:
            stats_list[solution.run_result] += 1
            stats_list[13] += 1
            if solution.run_result == 4:
                if solution.problem_id not in problem_list.keys():
                    problem_list[solution.problem_id] = 1
                else:
                    problem_list[solution.problem_id] = problem_list[solution.problem_id] + 1
        school = School.objects.filter(school_id=user.user_school).first()
        if not school:
            school_name = user.user_school
        else:
            school_name = school.school_name
        message = {
            'user_id': user_id,
            'user_nick': user.user_nick,
            'user_solved': stats_list[5],
            'user_submit': stats_list[13],
            'user_accurate': len(problem_list),
            'format_error': stats_list[4],
            'wrong_answer': stats_list[6],
            'time_over': stats_list[7],
            'memory_over': stats_list[8],
            'output_over': stats_list[9],
            'runtime_error': stats_list[10],
            'compile_error': stats_list[11],
            'user_school': school_name,
            'solved_data': problem_list,
        }
        return JsonResponse({'status': True, 'message': message})


class GetRankList(View):
    """
    模块: 获取用户排名列表
    接口信息:
        GET:
            sort_by: 查询时间段[None|year|month|day](String)
    返回信息:
        GET:
            message: 用户排名列表
    """
    def getTime(self, sort_by):
        end_time = timezone.now()
        days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        year = end_time.year
        month = end_time.month
        day = end_time.day
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            days[2] = 29
        if sort_by == 'year':
            begin_time = f'{year - 1}-{month}-{day}'
        elif sort_by == 'month':
            if month == 1:
                month = 13
                year = year - 1
            begin_time = f'{year}-{month - 1}-{day}'
        elif sort_by == 'week':
            if day <= 6:
                day = days[month - 1] + day
                month = month - 1
            begin_time = f'{year}-{month}-{day - 6}'
        else:
            begin_time = f'{year}-{month}-{day} 00:00:00'
        return begin_time

    def get(self, request):
        page = request.GET.get("page")
        total = request.GET.get("total")
        sort_by = request.GET.get('sort_by')
        text = request.GET.get("text")
        print(page, total)
        if sort_by:
            obj = publicMethod.get_rank_list_by_time(self.getTime(sort_by))
        else:
            obj = publicMethod.get_all_rank_list()
        message = []
        rank = 1
        for i in obj:
            if text and text not in i[0] and text not in i[2]:
                continue
            message.append({
                'rank': rank,
                'user_id': i[0],
                'user_name': i[1],
                'user_nick': i[2],
                'submit': i[3],
                'solved': i[4],
                'school_name': i[5],
                'user_sex': i[6],
            })
            rank = rank + 1
        user_num = len(obj)
        if total == '0':
            message = message[int(page) - 1:]
        else:
            message = message[(int(page) - 1) * int(total): int(page) * int(total)]
        return JsonResponse({'status': True, "message": message, 'total': user_num})


class MyContest(View):
    """
    模块: 获取用户参加的竞赛
    接口信息:
        GET:
            token: token认证
    返回信息:
        GET:
            message: 用户参加竞赛的列表
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登入'})
        contest_list = ContestUser.objects.filter(contest_user=user_id).values_list('contest_id')
        return JsonResponse({'status': True, 'message': [item[0] for item in contest_list]})


class GetUserIcon(View):
    """
    模块: 用户头像获取,上传头像
    接口信息:
        GET:
            None
        POST:
            token: token认证
            icon: 头像文件
    返回信息:
        GET:
            默认头像
        POST:
            None
    """
    def get(self, request):
        # token = request.COOKIES.get('token')
        # user_id = cache.get(token)
        image = open("files/icon.jpg", "rb").read()
        # print(token)
        # if not user_id:
        #     data = HttpResponse(image, content_type="image/png")
        #     data.delete_cookie('token')
        #     return data
        # cache.touch(token, 7200)
        # obj = User.objects.filter(user_id=user_id)
        # if obj.exists():
        #     obj = obj.first()
        #     icon = obj.user_icon
        #     if icon:
        #         icon = open(icon.path, "rb").read()
        #         # print(icon.path, type(icon.path))
        #         return HttpResponse(icon, content_type="image/png")
        #     else:
        #         return HttpResponse(image, content_type="image/png")
        # else:
        return HttpResponse(image, content_type="image/png")

    def post(self, request):
        token = request.COOKIES.get('token')
        icon = request.FILES.get('file')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        obj = User.objects.filter(user_id=user_id)
        if obj.exists():
            obj = obj.first()
            icon = icon.read()
            obj.user_icon = str(base64.b64encode(icon), encoding='utf-8')
            obj.save()
            message = {'status': True, 'message': '头像上传成功'}
        else:
            message = {'status': False, 'message': '请先完善用户信息'}
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
    返回信息:
        GET:
            后台生成的验证码
        POST:
            status: 请求状态[True|False](boolean)
            err: 提示信息
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
        obj = Password.objects.get(user_id=user_id)
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


class CheckTwoPasswords(View):
    """
    模块: 密码验证
    接口信息:
        GET:
            None
        POST:
            user_id: 用户账号
            password: 用户密码
    返回信息:
        GET:
            None
        POST:
            status: 验证状态[True|False](boolean)
            err: 提示信息
    """
    def get(self, request):
        pass

    def post(self, request):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        obj = Password.objects.filter(user_id=user_id)
        if obj.exists():
            obj = obj.first()
            if publicMethod.check_password(password_new=password, password_old=obj.password) or publicMethod.check_password2(password_new=password, password_old=obj.password):
                message = {'status': True, 'err': '验证通过'}
            else:
                message = {'status': False, 'err': '密码错误'}
        else:
            message = {'status': False, 'err': '用户验证失败'}
        return JsonResponse(message)


class GetUserTokenInfo(View):
    """
    模块: 获取用户权限信息
    接口信息:
        GET:
            token: 用户token
        POST:
            None
    返回数据:
        GET:
            用户token所包含信息
        POST:
            None
    """
    def get(self, request):
        token = request.GET.get('token')
        data = publicMethod.parse_payload(token)
        return JsonResponse(data)

    def post(self, request):
        pass


class ChangeUserCapacity(View):
    """
    模块: 修改用户权限
    接口信息:
        GET:
            None
        POST:
            token: 当前登录用户的token
            user: 要修改的用户id
            role_pri: 要修改的用户权限
    返回信息:
        GET:
            None
        POST:
            status: 数据操作状态
            err: 提示信息
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.POST.get('user')
        role_pri = request.POST.get('role_pri')
        capacity = publicMethod.get_user_capacity(token)
        if capacity in [0, 1]:
            obj = User.objects.filter(user_id=user_id)
            if obj.exists():
                obj = obj.first()
                obj.user_power = role_pri
                obj.save()
                message = {'status': True, 'err': '权限修改成功'}
            else:
                message = {'status': False, 'err': '未找到此用户'}
        else:
            message = {'status': False, 'err': '你未拥有此权限'}
        return JsonResponse(message)


class ResettingUserPassword(View):
    """
    模块: 重置用户密码
    接口信息:
        GET:
            None
        POST:
            token: 当前登录用户token
            user: 要修改的用户账号
            password: 修改后的密码
    返回信息:
        GET:
            None
        POST:
            status: 数据操作状态
            err: 提示信息
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.POST.get('user')
        password = request.POST.get('password')
        capacity = publicMethod.get_user_capacity(token)
        if capacity in [0, 1]:
            obj = Password.objects.filter(user_id=user_id)
            if obj.exists():
                obj = obj.first()
                obj.password = publicMethod.reg_pass(password)
                obj.save()
                message = {'status': True, 'err': '密码修改成功'}
            else:
                message = {'status': False, 'err': '未找到此用户'}
        else:
            message = {'status': False, 'err': '你未拥有此权限'}
        return JsonResponse(message)


class createTestToken(View):
    def get(self, request):
        time = int(request.GET.get('time'))
        power = int(request.GET.get('power'))
        user_id = request.GET.get('user_id', 'test')
        if time > 0:
            token = publicMethod.create_token({
                'user_id': user_id,
                'capacity': power,
                'user_name': 'test',
                'user_nick': 'test'
            }, time)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'token': ''})

    def post(self, request):
        return JsonResponse({'token': ''})
        pass


class CountMessage(View):
    def get(self, request):
        end_time = timezone.now()
        year = end_time.year
        month = end_time.month
        day = end_time.day
        begin_time = f'{year}-{month}-{day} 00:00:00'
        solution_total = Solution.objects.all().count()
        solution_today = Solution.objects.filter(Q(solution_time__gt=begin_time)).count()
        problem_total = Problem.objects.all().count()
        user_total = User.objects.all().count()
        message = {
            'solution_total': solution_total,
            'solution_today': solution_today,
            'problem_total': problem_total,
            'user_total': user_total,
        }
        return JsonResponse({'status': True, 'message': message})


class ExtendTokenTime(View):
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)

        if not user_id:
            return JsonResponse({'status': False})
        else:
            cache.touch(token, 7200)
            return JsonResponse({'status': True})
