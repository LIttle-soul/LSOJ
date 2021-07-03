from django.http import JsonResponse
from django.views.generic import View
from django.utils import timezone
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.utils.PublicMethods import PublicMethod
from app.models import *
import numpy

publicMethod = PublicMethod()


# --------------------------地址管理----------------------------
class AddProvince(View):
    """
    模块: 省份管理
    接口信息:
        GET:
            None
        POST:
            province: 要添加的省份名称
    返回数据:
        GET:
            所有省份列表
        POST:
            执行操作状态
    """
    def get(self, request):
        obj = Province.objects.using('app').all().values_list('province_name')
        return JsonResponse({'status': True, 'data': list(obj)})

    def post(self, request):
        province = request.POST.get('province')
        obj = Province.objects.using('app').filter(province_name=province)
        if obj.exists():
            message = {'status': False, 'info': '此省份已添加'}
        else:
            Province.objects.using('app').create(
                province_name=province
            )
            message = {'status': True, 'info': '省份添加成功'}
        return JsonResponse(message)


class AddMunicipality(View):
    """
    模块: 城市管理
    接口信息:
        GET:
            province: 要获取城市列表的省份
        POST:
            province: 要添加城市的省份
            municipality: 要添加的城市
    返回数据:
        GET:
            当前省份下的所有城市列表
        POST:
            城市添加状态
    """
    def get(self, request):
        province = request.GET.get('province')
        obj = Province.objects.using('app').filter(province_name=province)
        if obj.exists():
            province_obj = obj.first()
            data = province_obj.municipality_set.all().values_list('municipality_name')
            message = {'status': True, 'info': list(data)}
        else:
            message = {'status': False, 'info': '请先添加此省份'}
        return JsonResponse(message)

    def post(self, request):
        province = request.POST.get('province')
        municipality = request.POST.get('municipality')
        obj1 = Province.objects.using('app').filter(province_name=province)
        if obj1.exists():
            province_obj = obj1.first()
            obj2 = province_obj.municipality_set.filter(municipality_name=municipality)
            if obj2.exists():
                message = {'status': False, 'info': '当前城市已添加'}
            else:
                province_obj.municipality_set.create(municipality_name=municipality)
                message = {'status': True, 'info': '城市添加成功'}
        else:
            message = {'status': False, 'info': '请先添加此省份'}
        return JsonResponse(message)


# --------------------------学校管理----------------------------
class AddSchool(View):
    """
    模块: 学校管理
    接口信息:
        GET:
            province: 学校所在的省份
            municipality: 学校所在的城市
        POST:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学校名称
    返回数据:
        GET:
            当前城市下面的所有学校
        POST:
            添加学校的状态
    """
    def get(self, request):
        province = request.GET.get('province')
        municipality = request.GET.get('municipality')
        obj = Municipality.objects.using('app').filter(
            Q(municipality_province__province_name=province) &
            Q(municipality_name=municipality)
        )
        if obj.exists():
            obj1 = obj.first()
            data = obj1.school_set.all().values('school_name', 'school_describe')
            message = {'status': True, 'info': list(data)}
        else:
            message = {'status': False, 'info': '请先添加相关城市信息'}
        return JsonResponse(message)

    def post(self, request):
        province = request.POST.get('province')
        municipality = request.POST.get('municipality')
        school = request.POST.get('school')
        describe = request.POST.get('describe')
        obj = Municipality.objects.using('app').filter(
            Q(municipality_province__province_name=province) &
            Q(municipality_name=municipality)
        )
        if obj.exists():
            obj1 = obj.first()
            obj2 = obj1.school_set.filter(school_name=school)
            if obj2.exists():
                message = {'status': False, 'info': '此学校已添加'}
            else:
                obj1.school_set.create(school_name=school, school_describe=describe)
                message = {'status': True, 'info': '学校添加成功'}
        else:
            message = {'status': False, 'info': '请先添加相关城市信息'}
        return JsonResponse(message)


class AddCollege(View):
    """
    模块: 学院添加
    接口信息:
        GET:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在的学校
        POST:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在学校
            college: 学院名称
    返回数据:
        GET:
            当前学校下面的所有学院
        POST:
            添加学院的状态
    """
    def get(self, request):
        province = request.GET.get('province')
        municipality = request.GET.get('municipality')
        school = request.GET.get('school')
        obj = School.objects.using('app').filter(
            Q(school_municipality__municipality_province__province_name=province) &
            Q(school_municipality__municipality_name=municipality) &
            Q(school_name=school)
        )
        if obj.exists():
            obj1 = obj.first()
            data = obj1.college_set.all().values_list('college_name')
            message = {'status': True, 'info': list(data)}
        else:
            message = {'status': False, 'info': '请先添加相关城市信息'}
        return JsonResponse(message)

    def post(self, request):
        province = request.POST.get('province')
        municipality = request.POST.get('municipality')
        school = request.POST.get('school')
        college = request.POST.get('college')
        obj = School.objects.using('app').filter(
            Q(school_municipality__municipality_province__province_name=province) &
            Q(school_municipality__municipality_name=municipality) &
            Q(school_name=school)
        )
        if obj.exists():
            obj1 = obj.first()
            obj2 = obj1.college_set.filter(college_name=college)
            if obj2.exists():
                message = {'status': False, 'info': '此学院已添加'}
            else:
                obj1.college_set.create(college_name=college)
                message = {'status': True, 'info': '学院添加成功'}
        else:
            message = {'status': False, 'info': '请先添加相关学校信息'}
        return JsonResponse(message)


class AddClass(View):
    """
    模块: 班级添加
    接口信息:
        GET:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在的学校
            college: 班级所在学院
        POST:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在学校
            college: 班级所在学院
            user_class: 班级名称
    返回数据:
        GET:
            当前学院下面的所有班级
        POST:
            添加班级的状态
    """
    def get(self, request):
        province = request.GET.get('province')
        municipality = request.GET.get('municipality')
        school = request.GET.get('school')
        college = request.GET.get('college')
        obj = College.objects.using('app').filter(
            Q(college_school__school_municipality__municipality_province__province_name=province) &
            Q(college_school__school_municipality__municipality_name=municipality) &
            Q(college_school__school_name=school) &
            Q(college_name=college)
        )
        if obj.exists():
            obj1 = obj.first()
            data = obj1.class_set.all().values_list('class_name')
            message = {'status': True, 'info': list(data)}
        else:
            message = {'status': False, 'info': '请先添加相关学院信息'}
        return JsonResponse(message)

    def post(self, request):
        province = request.POST.get('province')
        municipality = request.POST.get('municipality')
        school = request.POST.get('school')
        college = request.POST.get('college')
        user_class = request.POST.get('user_class')
        obj = College.objects.using('app').filter(
            Q(college_school__school_municipality__municipality_province__province_name=province) &
            Q(college_school__school_municipality__municipality_name=municipality) &
            Q(college_school__school_name=school) &
            Q(college_name=college)
        )
        if obj.exists():
            obj1 = obj.first()
            obj2 = obj1.class_set.filter(class_name=user_class)
            if obj2.exists():
                message = {'status': False, 'info': '此班级已添加'}
            else:
                obj1.class_set.create(college_name=user_class)
                message = {'status': True, 'info': '班级添加成功'}
        else:
            message = {'status': False, 'info': '请先添加相关学院信息'}
        return JsonResponse(message)


class AddStudent(View):
    """
    模块: 学生添加
    接口信息:
        GET:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在的学校
            college: 班级所在学院
            user_class: 学生所在班级
        POST:
            province: 学校所在的省份
            municipality: 学校所在的城市
            school: 学院所在学校
            college: 班级所在学院
            user_class: 学生所在班级
            student: 学生编号
    返回数据:
        GET:
            当前班级下面的所有学生
        POST:
            添加学生的状态
    """
    def get(self, request):
        province = request.GET.get('province')
        municipality = request.GET.get('municipality')
        school = request.GET.get('school')
        college = request.GET.get('college')
        user_class = request.GET.get('user_class')
        obj = Class.objects.using('app').filter(
            Q(class_college__college_school__school_municipality__municipality_province__province_name=province) &
            Q(class_college__college_school__school_municipality__municipality_name=municipality) &
            Q(class_college__college_school__school_name=school) &
            Q(class_college__college_name=college) &
            Q(class_name=user_class)
        )
        if obj.exists():
            obj1 = obj.first()
            data = obj1.user_set.all().values()
            message = {'status': True, 'info': list(data)}
        else:
            message = {'status': False, 'info': '请先添加相关班级信息'}
        return JsonResponse(message)

    def post(self, request):
        province = request.POST.get('province')
        municipality = request.POST.get('municipality')
        school = request.POST.get('school')
        college = request.POST.get('college')
        user_class = request.POST.get('user_class')
        student = request.POST.get('student')
        obj = Class.objects.using('app').filter(
            Q(class_college__college_school__school_municipality__municipality_province__province_name=province) &
            Q(class_college__college_school__school_municipality__municipality_name=municipality) &
            Q(class_college__college_school__school_name=school) &
            Q(class_college__college_name=college) &
            Q(class_name=user_class)
        )
        if obj.exists():
            obj1 = obj.first()
            obj2 = obj1.user_set.filter(user_id__user_id=student)
            if obj2.exists():
                message = {'status': False, 'info': '此学生已添加'}
            else:
                obj1.user_set.add(User.objects.get(user_id__user_id=student))
                message = {'status': True, 'info': '学生添加成功'}
        else:
            message = {'status': False, 'info': '请先添加相关学院信息'}
        return JsonResponse(message)


# --------------------------用户功能----------------------------
# 普通用户
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
    返回数据:
        GET:
            图片验证码内容
        POST:
            用户登录状态和提示信息
    """
    def get(self, request):
        res = publicMethod.capture(requester=request)
        return JsonResponse(res)

    def post(self, request):
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # print(username, password, code)
        if publicMethod.check_capture(requester=request, code=code):
            obj = Password.objects.using('app').filter(user_id=username)
            if obj.exists():
                obj = obj.first()
                if publicMethod.check_password(password_new=password, password_old=obj.password):
                    user_obj = User.objects.using('app').filter(user_id=obj)
                    capacity = user_obj.first().user_power if user_obj.exists() else 4
                    # print(capacity)
                    token = publicMethod.create_token({'username': obj.user_id, 'capacity': capacity}, 120)
                    LoginLog.objects.using('app').create(
                        user_id=obj,
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
    返回数据:
        GET:
            图片验证码内容
        POST:
            用户注册状态和提示信息
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
            obj = Password.objects.using('app').filter(user_id=username)
            if obj.exists():
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
        obj = User.objects.using('app').filter(user_id__user_id=user_id)
        if obj.exists():
            messages = {'status': True, 'err': '个人用户信息', 'data': obj.values().first()}
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
        school_id = request.POST.get('school_id')
        sex = request.POST.get('sex')
        sex = (0 if sex == '男' else 1)
        user = Password.objects.using('app').get(user_id=user_id)
        obj = User.objects.using('app').filter(user_id=user)
        if obj.exists():
            obj = obj.first()
            if nick_name:
                obj.nick = nick_name
            if school_id:
                school_obj = School.objects.filter(school_id=school_id)
                if school_obj.exists():
                    obj.school = school_obj.first()
                else:
                    return JsonResponse({'status': False, 'err': '此学校不存在'})
            obj.ip = publicMethod.get_ip(request)
            obj.reg_time = timezone.now()
            obj.save()
            message = {'status': True, 'err': '信息修改成功'}
        else:
            if school_id:
                school_obj = School.objects.filter(school_id=school_id)
                if school_obj.exists():
                    school_id = school_obj.first()
                else:
                    return JsonResponse({'status': False, 'err': '此学校不存在'})
            User.objects.using('app').create(
                user_id=user,
                real_name=real_name,
                nick=nick_name,
                ip=publicMethod.get_ip(request),
                access_time=timezone.now(),
                reg_time=timezone.now(),
                school=school_id,
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
            user_id: 用户id
            email: 邮箱（绑定邮箱时使用）
        POST:
            token: token认证
            user_id: 用户id
            email: 邮箱
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


#  ------------------------------------------------------------------------------------------------
class GetUserStatus(View):
    """
    模块: 获取用户状态
    接口信息:
        GET:
            user_id: 用户账号
        POST:
            None
    """
    def __init__(self):
        super(GetUserStatus, self).__init__()
        self.year_now = timezone.now().year
        self.month_now = timezone.now().month
        self.day_now = timezone.now().day

    def get(self, request):
        user_id = request.GET.get('user_id')
        year = self.year_now - 1
        month = self.month_now
        day = 1 if self.day_now <= 15 else 15
        solution_list = []
        solved_list = []
        submit_data = []
        solved_data = []
        date_data = []
        user = User.objects.using('app').filter(user_id__user_id=user_id)
        solution = Solution.objects.using('app').filter(user_id=user_id)
        if user.exists():
            user = user.first()
            solved = user.solved
            submit = user.submit
            school = user.school
            rank = User.objects.filter(solved__gt=solved).count() + 1
            if solution.exists():
                stop = False
                while True:
                    begin_time = timezone.now().replace(year, month, day)
                    day += 15
                    if day >= 30:
                        month += 1
                        day = 1
                        if month >= 13:
                            month = 1
                            year += 1
                    end_time = timezone.now().replace(year, month, day)
                    if end_time >= timezone.now():
                        stop = True
                        end_time = timezone.now()
                    submit_data.append(solution.filter(in_date__range=[begin_time, end_time]).count())
                    solved_data.append(solution.filter(Q(result=4) & Q(in_date__range=[begin_time, end_time])).count())
                    date_data.append(end_time)
                    if stop:
                        break
                solution_list = solution.values("result").annotate(number=Count("user_id"))
                solved_list = solution.filter(result=4).values("problem_id").annotate(number=Count('user_id'))
                # print(len(solved_list), len(solution))
                user.solved = len(solved_list)
                user.submit = len(solution)
                user.save()
        else:
            return JsonResponse({'status': False, 'err': '输入用户不存在'})
        return JsonResponse({'user_id': user_id,
                             'solved': solved,
                             'submit': submit,
                             'rank': rank,
                             'solution': list(solution_list),
                             'school': school,
                             'solved_list': list(solved_list),
                             'submit_data': list(submit_data),
                             'solved_data': list(solved_data),
                             'date_data': list(date_data)
                             })

    def post(self, request):
        pass


class GetRankList(View):
    """
    模块: 获取用户排名列表
    接口信息:
        GET:
            None
        POST:
            search: 查询字段
    """
    def get(self, request):
        sort_by = request.GET.get('sort_by')
        end_time = timezone.now()
        if sort_by == 'year':
            begin_time = f'{end_time.year - 1}-{end_time.month}-{end_time.day}'
            obj = publicMethod.get_rank_list_by_time(begin_time)
        elif sort_by == 'month':
            begin_time = f'{end_time.year}-{end_time.month - 1}-{end_time.day}'
            obj = publicMethod.get_rank_list_by_time(begin_time)
        elif sort_by == 'day':
            begin_time = f'{end_time.year}-{end_time.month}-{end_time.day - 1}'
            obj = publicMethod.get_rank_list_by_time(begin_time)
        else:
            obj = User.objects.using('app').all().order_by('-solved').values_list('user_id', 'real_name', 'nick', 'submit', 'solved', 'school', 'sex')
        data2 = list(obj)[:10]
        data2 = numpy.array(data2)
        data2 = data2.T
        return JsonResponse({"data": list(obj), "data2": data2.tolist()})

    def post(self, request):
        search = request.POST.get('search')
        obj = User.objects.using('app').filter(
            Q(user_id__user_id__contains=search) |
            Q(real_name__contains=search) |
            Q(nick__contains=search) |
            Q(school__contains=search)
        ).values('user_id', 'real_name', 'nick', 'submit', 'solved', 'school', 'sex')
        return JsonResponse({'data': list(obj)})


# 教师管理员功能
class GetUserList(View):
    """
    模块: 获取用户信息列表
    接口信息:
        GET:
            None
        POST:
            search: 查询字段
    """
    def get(self, request):
        message = []
        obj = User.objects.using('app').all()
        for user in obj.values():
            message.append(user)
        return JsonResponse({"data": message})

    def post(self, request):
        message = []
        search = request.POST.get('search')
        obj = User.objects.using('app').filter(
            Q(user_id__user_id__contains=search) |
            Q(real_name__contains=search) |
            Q(nick__contains=search) |
            Q(school__contains=search)
        )
        for user in obj.values():
            message.append(user)
        return JsonResponse({'data': message})


# 管理员权限部分
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
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.POST.get('user')
        role_pri = request.POST.get('role_pri')
        capacity = publicMethod.get_user_capacity(token)
        if capacity in [0, 1]:
            obj = User.objects.using('app').filter(user_id__user_id=user_id)
            if obj.exists():
                obj = obj.first()
                obj.role_pri = role_pri
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
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.POST.get('user')
        password = request.POST.get('password')
        capacity = publicMethod.get_user_capacity(token)
        if capacity in [0, 1]:
            obj = Password.objects.using('app').filter(user_id=user_id)
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


# ---------------------------问题功能---------------------------
class GetProblemList(View):
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        obj = Problems.objects.using('app').all().values('problem_id', 'title', 'difficulty', 'type', 'accepted', 'submit')
        data = {'status': True, 'data': list(obj)}
        return JsonResponse(data)

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
