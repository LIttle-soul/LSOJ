from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.core.cache import cache
from app.models import *
from app.RoleMethod.PublicMethod import PublicMethod
publicMethod = PublicMethod()


class CreateClass(View):
    """
    模块: 获取团队信息,创建团队,删除团队
    接口信息:
        GET:
            token：token认证
        POST:
            token：token认证
            team_name: 队伍名称
            team_introduce: 团队介绍
            team_member: 团队人员列表
            team_teacher: 指导老师
            team_school: 团队所属学校
        DELETE:
            token：token认证
            class_id: 团队ID
    返回信息:
        GET:
            status: 验证状态[True|False](boolean)
            message: team消息
        POST:
            status: 验证状态[True|False](boolean)
            message: 提示信息
        DELETE:
            status: 验证状态[True|False](boolean)
            message: 提示信息
    """
    def get(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        team_list = []
        teams = Class.objects.filter(class_type=1)
        for team in teams:
            user_list = []
            users = ClassUser.objects.filter(class_id=team.class_id)
            for user in users:
                user_nick = User.objects.filter(user_id=user.user_id).first()
                if not user_nick:
                    user_nick = user.user_id
                else:
                    user_nick = user_nick.user_nick
                user_list.append({
                    'user_id': user.user_id,
                    'user_nick': user_nick,
                    'user_type': user.user_type,
                    'add_time': user.add_time,
                    'user_status': user.user_status,
                })
            if team.class_college:
                class_college = School.objects.filter(school_id=team.class_college).first().school_name
            else:
                class_college = ''
            team_list.append({
                'class_id': team.class_id,
                'class_name': team.class_name,
                'class_creator': team.class_creator,
                'create_time': team.create_time,
                'class_introduce': team.class_introduce,
                'class_type': team.class_type,
                'class_college': class_college,
                'user_list': user_list,
            })
        teams = Class.objects.filter(class_type=4)
        for team in teams:
            user_list = []
            users = ClassUser.objects.filer(class_id=team.class_id)
            for user in users:
                user_nick = User.objects.filter(user_id=user.user_id).first().user_nick
                if not user_nick:
                    user_nick = user.user_id
                user_list.append({
                    'user_id': user.user_id,
                    'user_nick': user_nick,
                    'user_type': user.user_type,
                    'add_time': user.add_time,
                    'user_status': user.user_status,
                })
            if team.class_college:
                class_college = School.objects.filter(school_id=team.class_college).first().school_name
            else:
                class_college = ''
            team_list.append({
                'class_id': team.class_id,
                'class_name': team.class_name,
                'class_creator': team.class_creator,
                'create_time': team.create_time,
                'class_introduce': team.class_introduce,
                'class_type': team.class_type,
                'class_college': class_college,
                'user_list': user_list
            })
        return JsonResponse({'status': True, 'message': team_list})

    def post(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        team_name = request.POST.get('team_name')
        team_introduce = request.POST.get('team_introduce')
        team_member = request.POST.get('team_member')
        team_teacher = request.POST.get('team_teacher')
        team_school = request.POST.get('team_school')
        if not team_name or not team_member:
            return JsonResponse({'status': False, 'message': '信息不全'})
        team = Class.objects.create(
            class_name=team_name,
            class_creator=user_id,
            create_time=timezone.now(),
            class_introduce=team_introduce,
            class_type=1,
            class_college=team_school
        )
        team_member = team_member.split(',')
        for member in list(team_member):
            if member == '':
                continue
            ClassUser.objects.create(
                class_id=team.class_id,
                user_id=member,
                user_type=0,
                add_time=timezone.now(),
                user_status=1,
            )
        if team_teacher:
            ClassUser.objects.create(
                class_id=team.class_id,
                user_id=team_teacher,
                user_type=1,
                add_time=timezone.now(),
                user_status=1,
            )
        return JsonResponse({'status': True, 'message': '创建成功'})

    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        class_id = request.GET.get('class_id')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        user = User.objects.filter(user_id=user_id).first()
        power = user.user_power
        if not user:
            return JsonResponse({'status': False, 'message': '用户未完善信息'})
        team = Class.objects.filter(class_id=class_id).first()
        if not team:
            return JsonResponse({'status': False, 'message': '这个团队不存在'})
        if team.class_creator != user_id and power > 2:
            return JsonResponse({'status': False, 'message': '你没有权限'})
        team.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})


class JoinClass(View):
    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get('token')













