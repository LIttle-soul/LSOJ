from django.views.generic import View
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Q
from app.models import *
import time
import uuid


class GetTeamList(View):
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        mode = request.GET.get('mode')
        print(page, total, text, mode)
        team = Team.objects.all()
        if mode == 'join':
            team_user = TeamUser.objects.filter(team_user=user_id).values_list('team_id')
            team_user = [item[0] for item in team_user]
            team = team.filter(team_id__in=team_user)
        elif mode == 'create':
            team = team.filter(team_creator=user_id)
        if text:
            team = team.filter(Q(team_nick__contains=text) | Q(team_id__contains=text) | Q(team_creator__contains=text) | Q(school_name__contains=text))
        team_num = team.count()
        if total != '0':
            team = team[(int(page) - 1) * int(total): int(page) * int(total)]
        team_user_all = TeamUser.objects.all()
        user_all = User.objects.all()
        team_list = []
        for item in team:
            users = team_user_all.filter(team_id=item.team_id)
            user_list = []
            for user in users:
                it = user_all.filter(user_id=user.team_user).first()
                user_list.append({
                    'user_id': user.team_user,
                    'user_nick': it.user_nick,
                    'user_name': it.user_name,
                    'join_time': user.join_time,
                })
            team_list.append({
                'team_id': item.team_id,
                'team_nick': item.team_nick,
                'team_introduce': item.team_introduce,
                'team_creator': item.team_creator,
                'team_teacher': item.team_teacher,
                'team_school': item.team_school,
                'school_name': item.school_name,
                'registration_time': item.registration_time,
                'invitation_code': item.invitation_code if cache.get(f"team_{item.team_id}") == item.invitation_code else '',
                'user_list': user_list,
            })
        return JsonResponse({'status': True, 'message': team_list, 'total': team_num})

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        team_nick = request.POST.get('team_nick')
        team_introduce = request.POST.get('team_introduce')
        team_school = request.POST.get('team_school')
        team_teacher = request.POST.get('team_teacher')
        if team_school:
            team_school = team_school.split(',')[-1]
            school = School.objects.filter(school_id=team_school).first()
            school_name = school.school_name
        else:
            school_name = ''
        team = Team.objects.create(
            team_nick=team_nick,
            team_introduce=team_introduce,
            team_creator=user_id,
            team_teacher=team_teacher,
            team_school=team_school,
            school_name=school_name,
            registration_time=timezone.now(),
            invitation_code='',
        )
        TeamUser.objects.create(
            team_id=team.team_id,
            team_user=user_id,
            join_time=timezone.now(),
        )
        return JsonResponse({'status': True, 'message': '创建成功'})

    def put(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        team_id = request.GET.get('team_id')
        team_nick = request.GET.get('team_nick')
        team_introduce = request.GET.get('team_introduce')
        team_creator = request.GET.get('team_creator')
        team_school = request.GET.get('team_school')

        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '用户未完善信息'})
        if not team_id:
            return JsonResponse({'status': False, 'message': '没有团队'})
        team = Team.objects.filter(team_id=team_id).first()
        if user_id != team.team_creator and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '无权限'})
        team.team_nick = team_nick
        team.team_introduce = team_introduce
        team.team_creator = team_creator
        team.team_school = team_school
        school = School.objects.filter(school_id=team_school).first()
        team.school_name = school.school_name
        team.save()
        return JsonResponse({'status': True, 'message': '修改成功!'})

    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        team_id = request.GET.get('team_id')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '用户未完善信息'})
        team = Team.objects.filter(team_id=team_id).first()
        if not team:
            return JsonResponse({'status': False, 'message': '团队不存在'})
        if user_id != team.team_creator and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '无权限'})
        TeamUser.objects.filter(team_id=team_id).delete()
        team.delete()
        return JsonResponse({'status': True, 'message': '团队已删除'})


class CreateCode(View):
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        team_id = request.GET.get('team_id')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        team = Team.objects.filter(team_id=team_id).first()
        if not team:
            return JsonResponse({'status': False, 'message': '团队不存在'})
        if team.team_creator != user_id:
            return JsonResponse({'status': False, 'message': '无权限'})
        code = str(uuid.uuid1())
        team.invitation_code = code[0:8]
        cache.set(f"team_{team_id}", team.invitation_code, 259200)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() + 259200)))
        team.code_time = int(time.time()) + 259200
        team.save()
        return JsonResponse({'status': True, 'message': {'code': team.invitation_code, 'time': end_time}})


class JoinTeam(View):
    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        code = request.POST.get('code')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        team = Team.objects.filter(invitation_code=code, code_time__gte=int(time.time())).first()
        if not team:
            return JsonResponse({'status': False, 'message': '邀请码不正确'})
        else:
            team_user = TeamUser.objects.filter(team_id=team.team_id, team_user=user_id).first()
            if team_user:
                return JsonResponse({'status': False, 'message': '已加入该团队!'})
            TeamUser.objects.create(
                team_id=team.team_id,
                team_user=user_id,
                join_time=timezone.now(),
            )
            return JsonResponse({'status': True, 'message': '加入成功'})


    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        team_id = request.GET.get('team_id')
        delete_user = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '用户未完善信息'})
        if not delete_user:
            delete_user = user_id
        team = Team.objects.filter(team_id=team_id).first()
        if user_id == delete_user or team.team_creator == user_id or user.user_power in [0, 1]:
            team_user = TeamUser.objects.filter(team_id=team_id, team_user=delete_user).first()
            team_user.delete()
        else:
            return JsonResponse({'status': False, 'message': '无权限'})
        user_num = TeamUser.objects.filter(team_id=team_id).count()
        if user_num == 0:
            team.delete()
        elif team.team_creator == delete_user:
            team.team_creator = TeamUser.objects.filter(team_id=team_id).first().team_user
            team.save()
        return JsonResponse({'status': True, 'message': '删除完成'})


