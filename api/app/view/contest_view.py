from django.db import connection
from django.db.models import Q
from django.forms import model_to_dict
from django.views.generic import View
from app.models import *
from django.core.cache import cache
from django.http import JsonResponse
from app.RoleMethod.PublicMethod import PublicMethod
from django.utils import timezone
from datetime import datetime
import pytz
utc = pytz.UTC
publicMethod = PublicMethod()


# 竞赛列表
class ContestList(View):
    """
        模块: 竞赛作业列表
        接口信息:
        GET:
            page: 页数
        POST:
            None
    """
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        page = request.GET.get('page')
        total = request.GET.get('total')
        status = request.GET.get('status')
        text = request.GET.get('text')
        contest_id = request.GET.get('contest_id')
        time = request.GET.get('time')
        me = request.GET.get('me')
        print(page, total, status, text, me)
        if not contest_id:
            contest = Contest.objects.all().order_by('-contest_id')
            if me:
                if not user_id:
                    return JsonResponse({'status': False, 'message': '未登入'})
                contests = ContestUser.objects.filter(contest_user=user_id).values_list("contest_id")
                contests_temp = [item[0] for item in contests]
                print(contests_temp)
                contest = contest.filter(contest_id__in=contests_temp)
            if time:
                contest = contest.filter(end_time__gte=timezone.now())
            if text:
                contest = contest.filter(Q(contest_id__contains=text) | Q(contest_title__contains=text) | Q(contest_creator__contains=text))
            if status:
                contest = contest.filter(contest_province=status)
            contest_num = contest.count()
            if total != '0':
                contest = contest[(int(page) - 1) * int(total): int(page) * int(total)]
            contest_data = []
            for data in contest:
                users = ContestUser.objects.filter(contest_id=data.contest_id)
                user_list = []
                for user in users:
                    user_list.append({
                        'user_id': user.contest_user,
                        'contest_id': user.contest_id,
                        'contest_class': user.contest_class,
                        'contest_account': user.contest_account
                    })
                contest_data.append({
                    'contest_id': data.contest_id,
                    'contest_title': data.contest_title,
                    'contest_introduce': data.contest_introduce,
                    'contest_province': data.contest_province,
                    'contest_language': [] if data.contest_language is None else [int(item) for item in data.contest_language.split(',')],
                    'contest_creator': data.contest_creator,
                    'start_time': data.start_time,
                    'end_time': data.end_time,
                    'contest_password': data.contest_password,
                    'contest_defunct': data.contest_defunct,
                    'problem_list': [],
                    'user_list': user_list
                })
        else:
            contest = Contest.objects.filter(contest_id=contest_id).first()
            users = ContestUser.objects.filter(contest_id=contest_id)
            user_list = []
            for user in users:
                user_list.append({
                    'user_id': user.contest_user,
                    'contest_id': user.contest_id,
                    'contest_class': user.contest_class,
                    'contest_account': user.contest_account
                })
            contest_data = {
                'contest_id': contest.contest_id,
                'contest_title': contest.contest_title,
                'contest_introduce': contest.contest_introduce,
                'contest_province': contest.contest_province,
                'contest_language': [] if contest.contest_language is None else [int(item) for item in
                                                                              contest.contest_language.split(',')],
                'contest_creator': contest.contest_creator,
                'start_time': contest.start_time,
                'end_time': contest.end_time,
                'contest_password': contest.contest_password,
                'contest_defunct': contest.contest_defunct,
                'problem_list': [],
                'user_list': user_list
            }
            contest_num = 0
        return JsonResponse({'status': True, 'message': contest_data, 'total': contest_num})

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_title = request.POST.get('contest_title')  # 比赛名称
        start_time = request.POST.get('start_time')  # 开始时间
        end_time = request.POST.get('end_time')  # 结束时间
        if start_time > end_time:
            return JsonResponse({'status': False, 'message': '结束时间不能比开始时间小'})
        problems_id = request.POST.get('problem_id')  # 问题编号
        contest_introduce = request.POST.get('contest_introduce')  # 竞赛描述
        contest_language = request.POST.get('contest_language')  # 编程语言类型
        contest_province = request.POST.get('contest_province')  # 竞赛类型
        contest_password = request.POST.get('contest_password')  # 密码
        contest_status = request.POST.get('contest_status')
        if contest_password is None:
            contest_password = '0000'
        if not (contest_title and start_time and end_time and problems_id and contest_introduce and contest_province and contest_language):
            return JsonResponse({'status': False, 'massage': '信息不完善'})
        contest = Contest.objects.create(
            contest_title=contest_title,
            start_time=start_time,
            end_time=end_time,
            contest_introduce=contest_introduce,
            contest_province=contest_province,
            contest_language=contest_language,
            contest_password=contest_password,
            contest_creator=user_id,
            contest_defunct=contest_status == "true"
        )
        problem_num = 0
        problems_id = problems_id.split(',')
        for problem_id in problems_id:
            ContestProblem.objects.create(
                contest_id=contest.contest_id,
                problem_id=problem_id,
                problem_num=problem_num
            )
            problem_num = problem_num + 1
        return JsonResponse({'status': True, 'message': '添加成功'})

    def put(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_id = request.GET.get('contest_id')
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '竞赛不存在'})
        contest_title = request.GET.get('contest_title')
        if contest_title is not None:
            contest.contest_title = contest_title
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        if start_time is not None:
            if contest.start_time < timezone.now() and contest.start_time != start_time:
                return JsonResponse({'status': False, 'message': '比赛开始不能修改开始时间'})
            contest.start_time = start_time
        if end_time is not None:
            contest.end_time = end_time
        if contest.start_time > contest.end_time:
            return JsonResponse({'status': False, 'message': '结束时间不能比开始时间小'})
        contest_introduce = request.GET.get('contest_introduce')
        if contest_introduce is not None:
            contest.contest_introduce = contest_introduce
        contest_province = request.GET.get('contest_province')
        if contest_province is not None:
            contest.contest_province = contest_province
        contest_status = request.GET.get('contest_status')
        if contest_status is not None:
            contest.contest_defunct = contest_status == 'true'
        contest_password = request.GET.get('contest_password')
        if contest_password is not None:
            contest.contest_password = contest_password
        contest_language = request.GET.get('contest_language')  # 编程语言类型
        if contest_language is not None:
            contest.contest_language = contest_language
        contest.save()
        return JsonResponse({'status': True, 'message': '修改成功'})

    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_id = request.GET.get('contest_id')
        print(contest_id)
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '竞赛不存在'})
        ContestProblem.objects.filter(contest_id=contest_id).delete()
        ContestUser.objects.filter(contest_id=contest_id).delete()
        Solution.objects.filter(contest_id=contest_id).delete()
        contest.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})


class ContestProblemList(View):
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        contest_id = request.GET.get('contest_id')
        problems = ContestProblem.objects.filter(contest_id=contest_id).order_by('problem_num')
        problem_num = problems.count()
        if text:
            problems = problems.filter(Q(problem_id__contains=text) | Q(problem_title__contains=text))
        if total != '0':
            problems = problems[(int(page) - 1) * int(total): int(page) * int(total)]
        problem_list = []
        for problem in problems:
            question = Problem.objects.filter(problem_id=problem.problem_id).first()
            if not question:
                continue
            if user_id:
                problem_ture = Solution.objects.filter(contest_id=contest_id, problem_id=problem.problem_id,
                                                       user_id=user_id, run_result=4).first()
                problem_false = Solution.objects.filter(contest_id=contest_id, problem_id=problem.problem_id,
                                                        user_id=user_id).first()
                if problem_ture:
                    result = '1'
                elif problem_false:
                    result = '-1'
                else:
                    result = '0'
            else:
                result = '0'
            creator_name = ''
            if question.problem_creator:
                user = User.objects.filter(user_id=question.problem_creator).first()
                if user:
                    creator_name = user.user_name
            problem_list.append({
                'problem_num': chr(problem.problem_num + 65),
                'problem_id': problem.problem_id,
                'problem_title': question.problem_title,
                'problem_description': question.problem_description,
                'problem_spj': question.problem_spj,
                'creation_time': question.creation_time,
                'time_limit': question.time_limit,
                'memory_limit': question.memory_limit,
                'problem_difficult': question.problem_difficult,
                'problem_creator': question.problem_creator,
                'creator_name': creator_name.split(','),
                'problem_status': question.problem_status,
                'problem_submit': Solution.objects.filter(contest_id=contest_id, problem_id=problem.problem_id).count(),
                'problem_accepted': Solution.objects.filter(contest_id=contest_id, problem_id=problem.problem_id, run_result=4).count(),
                'pass_status': result
            })
        return JsonResponse({'status': True, 'message': problem_list, 'total': problem_num})

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_id = request.POST.get('contest_id')
        problem_id = request.POST.get('problem_id')
        print(contest_id, problem_id)
        problem = Problem.objects.filter(problem_id=problem_id).first()
        if not problem:
            return JsonResponse({'status': False, 'message': '没有这个问题'})
        ContestProblem.objects.create(
            contest_id=contest_id,
            problem_id=problem_id,
            problem_num=ContestProblem.objects.filter(contest_id=contest_id).count(),
        )
        return JsonResponse({'status': True, 'message': '添加成功'})

    def put(self, request):
        token = request.COOKIES.get('token')
        contest_id = request.GET.get('contest_id')
        problem_list = request.GET.get('problem_list')
        problem_list = problem_list.split(',')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '这个竞赛不存在'})
        problems = ContestProblem.objects.filter(contest_id=contest_id)
        num = 0
        for problem_id in problem_list:
            if problem_id == '':
                break
            problem = problems.filter(problem_id=problem_id).first()
            if not problem:
                continue
            problem.problem_num = num
            problem.save()
            num += 1
        return JsonResponse({'status': True, 'message': '修改成功'})


    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': "用户认证失败"})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_id = request.GET.get('contest_id')
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '这个竞赛不存在'})
        if timezone.now() > contest.start_time:
            return JsonResponse({'status': False, 'message': '这个竞赛已经开始了！'})
        problem_id = request.GET.get('problem_id')
        problems = ContestProblem.objects.filter(contest_id=contest_id)
        problem_num = problems.filter(problem_id=problem_id).first()
        if not problem_num:
            return JsonResponse({'status': False, 'message': '问题不存在'})
        problem_num = problem_num.problem_num
        for problem in problems:
            if problem.problem_id == problem_id:
                problem.delete()
                continue
            if problem.problem_num > problem_num:
                problem.problem_num -= 1
                problem.save()
        Solution.objects.filter(contest_id=contest_id, problem_id=problem_id).delete()
        the_problem = ContestProblem.objects.filter(contest_id=contest_id, problem_id=problem_id).first()
        the_problem.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})


class ContestRanks(View):
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        if contest_id is None:
            return JsonResponse({'status': False, 'message': '竞赛ID不存在！'})
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '竞赛不存在'})
        solution_all = Solution.objects.filter(contest_id=contest_id)
        problem_list = ContestProblem.objects.filter(contest_id=contest_id)
        if contest.contest_province == 0:
            user_list = list(solution_all.values_list('user_id'))
        else:
            user_list = list(ContestUser.objects.filter(contest_id=contest_id).values_list('contest_user'))
        for user in user_list:
            obj = ContestRank.objects.filter(contest_id=contest_id, contest_user=user[0]).first()
            if not obj:
                obj = ContestRank.objects.create(
                    contest_id=contest_id,
                    contest_user=user[0],
                )
            contest_put = ''
            contest_score = ''
            contest_time = 0
            pass_num = 0
            for problem in problem_list:
                pass_time = 0
                put_num = 0
                solutions = solution_all.filter(contest_id=contest_id, user_id=user[0], problem_id=problem.problem_id).order_by('solution_time')
                for solutions in solutions:
                    if solutions.solution_time > contest.end_time:
                        break
                    if solutions.run_result == 4:
                        pass_time = int(solutions.solution_time.timestamp() * 1000 - contest.start_time.timestamp() * 1000 + put_num * 1200000)
                        pass_num = pass_num + 1
                        contest_time = contest_time + pass_time
                        break
                    else:
                        put_num = put_num + 1
                contest_score = contest_score + str(pass_time) + ','
                contest_put = contest_put + str(put_num) + ','
            obj.contest_time = contest_time
            obj.contest_sum = pass_num
            obj.contest_score = contest_score
            obj.contest_put = contest_put
            obj.save()
        return JsonResponse({'status': True, 'message': '添加成功'})


class RankList(View):

    def getTime(self, the_time):
        the_time = "{:02d}:{:02d}:{:02d}".format(int(the_time/3600), int((the_time-int((the_time/3600))*3600)/60), int(the_time % 60))
        return the_time

    def get(self, request):
        page = request.GET.get('page')
        total = request.GET.get('total')
        contest_id = request.GET.get('contest_id')
        contest_rank = ContestRank.objects.filter(contest_id=contest_id).order_by('-contest_sum', 'contest_time')
        rank_num = contest_rank.count()
        if total != '0':
            contest_rank = contest_rank[(int(page) - 1) * int(total): int(page) * int(total)]
        rank_list = []
        for rank in contest_rank:
            score_list = dict()
            score = rank.contest_score.split(',')
            put = rank.contest_put.split(',')
            num = 65
            for it in score:
                if not it:
                    break
                score_list[chr(num)] = {'time': self.getTime(int(it) / 1000), 'num': put[num-65]}
                num = num + 1
            user = User.objects.filter(user_id=rank.contest_user).first()
            if not user:
                contest_user = rank.contest_user
            else:
                contest_user = user.user_nick
            rank_list.append({
                'contest_id': rank.contest_id,
                'contest_user': rank.contest_user,
                'user_nick': contest_user,
                'contest_sum': rank.contest_sum,
                'contest_time': self.getTime(int(rank.contest_time) / 1000),
                'contest_score': score_list,
            })
        return JsonResponse({'status': True, 'message': rank_list, 'total': rank_num})


class ContestStats(View):
    def get(self, request):
        page = request.GET.get('page')
        total = request.GET.get('total')
        contest_id = request.GET.get('contest_id')
        contest_problem = ContestProblem.objects.filter(contest_id=contest_id).order_by('problem_num')
        solutions = Solution.objects.filter(contest_id=contest_id)
        num = contest_problem.count()
        problem_list = dict()
        i = 0
        for problem in contest_problem:
            problem_list[problem.problem_id] = i
            i += 1
        stats_list = []
        for i in range(num):
            stats_list.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for solution in solutions:
            stats_list[problem_list[solution.problem_id]][solution.run_result] += 1
            stats_list[problem_list[solution.problem_id]][13] += 1
        message = []
        for i in range(num):
            message.append({
                'problem_num': chr(65+i),
                'ac': stats_list[i][4],
                'pe': stats_list[i][5],
                'wa': stats_list[i][6],
                'tle': stats_list[i][7],
                'mle': stats_list[i][8],
                'ole': stats_list[i][9],
                're': stats_list[i][10],
                'ce': stats_list[i][11],
                'tr': stats_list[i][12],
                'total': stats_list[i][13]
            })
        status_num = len(message)
        if total != '0':
            message = message[(int(page) - 1) * int(total): int(page) * int(total)]
        return JsonResponse({'status': True, 'message': message, 'total': status_num})


class ContestUserList(View):
    def get(self, request):
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        contest_id = request.GET.get('contest_id')
        contest = Contest.objects.filter(contest_id=contest_id)
        if not contest:
            return JsonResponse({'status': False, 'message': '不存在这个竞赛'})
        contest_user = ContestUser.objects.filter(contest_id=contest_id)
        if text:
            contest_user = contest_user.filter(Q(contest_user__contains=text))
        user_num = contest_user.count()
        if total != '0':
            contest_user = contest_user[(int(page) - 1) * int(total): int(page) * int(total)]
        user_list = []
        for users in contest_user:
            user = User.objects.filter(user_id=users.contest_user).first()
            if not user:
                continue
            school_name = ''
            if user.user_school:
                user_school = user.user_school.split(',')[-1]
                school_name = School.objects.filter(school_id=user_school).first().school_name
            user_list.append({
                'contest_id': users.contest_id,
                'contest_user': users.contest_user,
                'user_name': user.user_name,
                'user_school': school_name,
                'student_id': user.student_id,
                'contest_class': users.contest_class,
                'contest_account': users.contest_account,
                'contest_grades': users.contest_grades,
                'contest_auditing': users.contest_auditing,
                'apply_time': users.apply_time,
            })
        return JsonResponse({'status': True, 'message': user_list, 'total': user_num})

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登入'})
        identity = User.objects.filter(user_id=user_id).first().user_power
        if identity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        contest_id = request.POST.get('contest_id')
        user_list = request.POST.get('user_list')
        user_list = user_list.split(',')
        print(user_list)
        for user_id in user_list:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                continue
            user = ContestUser.objects.filter(contest_id=contest_id, contest_user=user_id).first()
            if user:
                continue
            ContestUser.objects.create(
                contest_id=contest_id,
                contest_user=user_id,
                contest_auditing=True,
                apply_time=timezone.now()
            )
        return JsonResponse({'status': True, 'message': '添加成功'})

    def put(self, request):
        contest_id = request.GET.get('contest_id')
        user_id = request.GET.get('user_id')
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '没有这个竞赛'})
        obj = ContestUser.objects.filter(contest_id=contest_id, contest_user=user_id).first()
        if not obj:
            return JsonResponse({'status': False, 'message': '未报名'})
        obj.contest_auditing = True
        obj.save()
        return JsonResponse({'status': True, 'message': '修改成功'})

    def delete(self, request):
        user_id = request.GET.get('user_id')
        contest_id = request.GET.get('contest_id')
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '没有这个竞赛'})
        user = ContestUser.objects.filter(contest_id=contest_id, contest_user=user_id).first()
        if not user:
            return JsonResponse({'status': False, 'message': '这个没有参加这个竞赛'})
        user.delete()
        obj = ContestRank.objects.filter(contest_id=contest_id, contest_user=user_id).first()
        if obj:
            obj.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})


# 将数据库查询的Object数据转为json类型数据方法
def changeToJson(data):
    json_list = []
    for i in data:
        json_dict = model_to_dict(i)
        json_list.append(json_dict)
    return json_list
# 竞赛题目
# class contestProblemList(View):
#     """
#             模块: 竞赛题目
#             接口信息:
#             GET:
#                 token：token认证
#                 contest_id：竞赛id
#             POST:
#                 token：token认证
#                 contest_id：竞赛id
#                 password: 竞赛密码
#         """
#     def get(self, request):
#         token = request.GET.get('token')
#         contest_id = request.GET.get('contest_id')
#         user_id = publicMethod.check_user_login(token)
#         identity = publicMethod.get_user_capacity(token)
#         if contest_id == '':
#             return JsonResponse({'err': '请求失败，contest_id为空'})
#         contest_province = Contest.objects.filter(contest_id=contest_id).values('contest_province').first()
#         contest_province = contest_province['contest_province']
#         contest = Contest.objects.filter(contest_id=contest_id).all()
#         contest = changeToJson(contest)
#         endtime = Contest.objects.filter(contest_id=contest_id).values('end_time').first()
#         endtime = endtime['end_time']
#         endtime = datetime.datetime.strftime(endtime, '%Y-%m-%d %H:%M:%S')
#         starttime= Contest.objects.filter(contest_id=contest_id).values('start_time').first()
#         starttime = starttime['start_time']
#         starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')
#         if contest_province == 0:
#             problem_data = []
#             problems = ContestProblem.objects.filter(contest_id=contest_id).order_by('problem_num').values('problem_id')
#             for problem in problems:
#                 problem = problem['problem_id']
#                 num = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values('problem_num').first()
#                 num = num['problem_num']
#                 title_number = chr(int(num) + 65)
#                 title = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values('problem_title').first()
#                 submit = 0
#                 solved = 0
#                 result = Solution.objects.filter(problem_id=problem, contest_id=contest_id).values('run_result')
#                 for data in result:
#                     if data['run_result'] == 4:
#                         solved += 1
#                         submit += 1
#                     else:
#                         submit += 1
#                 problem_data.append(
#                     {
#                         'problem_id': problem,
#                         'contest_id': contest_id,
#                         'contest_title': contest[0]['contest_title'],
#                         'type': contest[0]['contest_province'],
#                         'contest_creator': contest[0]['contest_creator'],
#                         'starttime': starttime,
#                         'endtime': endtime,
#                         'title_number': title_number,
#                         'problem_title': title['problem_title'],
#                         'solved': solved,
#                         'submit': submit
#                     }
#                 )
#             return JsonResponse({'status': 'Ture', 'problem_data': problem_data})
#         else:
#             if not user_id:
#                 return JsonResponse({'status': False, 'err': "用户认证失败"})
#             if identity not in [0, 1] and user_id != contest[0]['contest_creator']:
#                 problem_data = []
#                 problem_data.append(
#                     {
#                         'contest_id': contest_id,
#                         'contest_title': contest[0]['contest_title'],
#                         'type': contest[0]['contest_province'],
#                         'contest_creator': contest[0]['contest_creator'],
#                         'starttime': starttime,
#                         'endtime': endtime,
#                     }
#                 )
#                 return JsonResponse({'status': 'Ture', 'problem_data': problem_data})
#             else:
#                 problem_data = []
#                 problems = ContestProblem.objects.filter(contest_id=contest_id).order_by('problem_num').values(
#                     'problem_id')
#                 for problem in problems:
#                     problem = problem['problem_id']
#                     num = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values(
#                         'problem_num').first()
#                     num = num['problem_num']
#                     title_number = chr(int(num) + 65)
#                     title = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values(
#                         'problem_title').first()
#                     submit = 0
#                     solved = 0
#                     result = Solution.objects.filter(problem_id=problem, contest_id=contest_id).values('run_result')
#                     for data in result:
#                         if data['run_result'] == 4:
#                             solved += 1
#                             submit += 1
#                         else:
#                             submit += 1
#                     problem_data.append(
#                         {
#                             'problem_id': problem,
#                             'contest_id': contest_id,
#                             'contest_title': contest[0]['contest_title'],
#                             'type': contest[0]['contest_province'],
#                             'contest_creator': contest[0]['contest_creator'],
#                             'starttime': starttime,
#                             'endtime': endtime,
#                             'title_number': title_number,
#                             'problem_title': title['problem_title'],
#                             'solved': solved,
#                             'submit': submit
#                         }
#                     )
#                 return JsonResponse({'status': 'Ture', 'problem_data': problem_data})
#     def post(self, request):
#         token = request.POST.get('token')
#         contest_id = request.POST.get('contest_id')
#         password = request.POST.get('password')
#         user_id = publicMethod.check_user_login(token)
#         if contest_id == '':
#             return JsonResponse({'err': '请求失败，contest_id为空'})
#         if not user_id:
#             return JsonResponse({'status': False, 'err': "用户认证失败"})
#         contest = Contest.objects.filter(contest_id=contest_id).all()
#         contest = changeToJson(contest)
#         if str(password) != contest[0]['contest_password']:
#             return JsonResponse({'status': 'False', 'err': 'Password incorrect'})
#         endtime = Contest.objects.filter(contest_id=contest_id).values('end_time').first()
#         endtime = endtime['end_time']
#         endtime = datetime.datetime.strftime(endtime, '%Y-%m-%d %H:%M:%S')
#         starttime = Contest.objects.filter(contest_id=contest_id).values('start_time').first()
#         starttime = starttime['start_time']
#         starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')
#         problem_data = []
#         problems = ContestProblem.objects.filter(contest_id=contest_id).order_by('problem_num').values('problem_id')
#         for problem in problems:
#             problem = problem['problem_id']
#             num = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values('problem_num').first()
#             num = num['problem_num']
#             title_number = chr(int(num) + 65)
#             title = ContestProblem.objects.filter(problem_id=problem, contest_id=contest_id).values(
#                 'problem_title').first()
#             submit = 0
#             solved = 0
#             result = Solution.objects.filter(problem_id=problem, contest_id=contest_id).values('run_result')
#             for data in result:
#                 if data['run_result'] == 4:
#                     solved += 1
#                     submit += 1
#                 else:
#                     submit += 1
#             problem_data.append(
#                 {
#                     'contest_id': contest_id,
#                     'contest_title': contest[0]['contest_title'],
#                     'type': contest[0]['contest_province'],
#                     'contest_creator': contest[0]['contest_creator'],
#                     'starttime': starttime,
#                     'endtime': endtime,
#                     'title_number': title_number,
#                     'problem_title': title['problem_title'],
#                     'solved': solved,
#                     'submit': submit
#                 }
#             )
#         return JsonResponse({'status': 'Ture', 'problem_data': problem_data})

# 竞赛状态
class contestStatus(View):
    """
        模块: 竞赛状态
        接口信息:
        GET:
            contest_id：竞赛id
            page:页数
    """
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        if contest_id is None:
            return JsonResponse({'status': False, 'message': '请求失败，contest_id为空'})
        status_data = []
        solution = Solution.objects.filter(contest_id=contest_id).order_by('-solution_id')
        for data in solution:
            num = ContestProblem.objects.filter(problem_id=data.problem_id).values('problem_num').first()
            status_data.append({
                'solution_id': data.solution_id,
                'user_id': data.user_id,
                'problem_id': data.problem_id,
                'problem_num': num,
                'run_result': data.run_result,
                'run_error': data.run_error,
                'run_memory': data.run_memory,
                'run_time': data.run_time,
                'solution_language': data.solution_language,
                'code_length': data.code_length,
                'solution_time': data.solution_time,
                'solution_ip': data.solution_ip,
            })
        return JsonResponse({'status': True, 'message': status_data})


# 竞赛排名
class ContestRankList(View):
    """
        模块: 竞赛作业排名
        接口信息:
        GET:
            contest_id：竞赛id
    """
    # 整数改为时间
    def timeChange(self, time):
        time = str(time)
        if len(time) == 2:
            time = time
        elif len(time) == 1:
            time = '0' + time
        return time
    # 把相隔时间转化为时分秒
    def timedeltaChange(self, time):
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds += time.microseconds / 1e6
        hours = time.days * 24 + hours
        time = "{}:{}:{}".format(hours, self.timeChange(minutes), self.timeChange(int(seconds)))
        return time
    # 竞赛中问题写错的次数
    def getContestSubmitFalseCount(self, contest_id, user_id, num):
        errcount = Solution.objects.filter(contest_id=contest_id, user_id=user_id, problem_id=num).exclude(run_result=4).count()
        return errcount
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        if contest_id is None:
            return JsonResponse({'status': False, 'message': '请求失败，contest_id为空'})
        starttime = Contest.objects.filter(contest_id=contest_id).values('start_time').first()
        starttime = starttime['start_time']
        users = ContestUser.objects.filter(contest_id=contest_id).values('contest_user')
        users = [item['contest_user'] for item in users]
        nums = ContestProblem.objects.filter(contest_id=contest_id).values('problem_num')
        nums = [item['problem_num'] for item in nums]
        num_first_time = []
        for num in nums:
            problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
            problem_first_right_time = Solution.objects.filter(contest_id=contest_id, problem_id=problem_id['problem_id'], run_result=4).order_by('solution_time').values(
                'solution_time').first()
            if problem_first_right_time:
                problem_first_right_time = problem_first_right_time['solution_time']
                problem_first_right_time =problem_first_right_time - starttime
                problem_first_right_time = self.timedeltaChange(problem_first_right_time)
            else:
                problem_first_right_time = '00:00:00'
            num_first_time.append(problem_first_right_time)
        contest_class = ContestUser.objects.filter(contest_user=users[0]).values('contest_class').first()
        if contest_class['contest_class'] == None:
            contestRank = []  # 竞赛排序
            total_time = []  # 总时间
            for user in users:
                now = datetime.datetime.now()
                sumtime = now - now
                nick = User.objects.filter(user_id=user).values('user_nick').first()
                nick = nick['user_nick']
                sumsolved = 0  # 总解题数
                contestNum = []
                contesttime = []
                errcount = []
                sumerrcount = 0
                for num in nums:
                    problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
                    user_first_time = Solution.objects.filter(contest_id=contest_id, user_id=user, problem_id=problem_id['problem_id'], run_result=4).order_by(
                        'solution_time').values('solution_time').first()
                    errcount_data = self.getContestSubmitFalseCount(contest_id, user, problem_id['problem_id'])
                    sumerrcount = int(errcount_data) + sumerrcount
                    errcount.append(errcount_data)
                    if user_first_time:
                        user_first_time = user_first_time['solution_time']
                        user_first_time = user_first_time - starttime
                        sumsolved = sumsolved + 1
                        rstime = self.timedeltaChange(user_first_time)
                    else:
                        timenow = datetime.datetime.now()
                        user_first_time = timenow - timenow
                        rstime = self.timedeltaChange(user_first_time)
                    num = chr(int(num) + 65)
                    contestNum.append(num)
                    contesttime.append(rstime)
                    sumtime = sumtime + user_first_time
                sumtime = self.timedeltaChange(sumtime)
                contestRank.append(
                    {
                        'user_id': user,
                        'nick': nick,
                        'sumsolved': sumsolved,
                        'contestNum': contestNum,
                        'contesttime': contesttime,
                        'sumtime': sumtime,
                        'errcount': errcount,
                        'sumerrcount': sumerrcount,
                    }
                )
            contestRank = sorted(contestRank, key=lambda x: (-x["sumsolved"], x['sumtime'], -x['sumerrcount']))
            rs = [contestRank, num_first_time]
            return JsonResponse(rs, safe=False)
        else:
            contestRank = []  # 竞赛排序
            total_time = []  # 总时间
            for user in users:
                contest_class = ContestUser.objects.filter(contest_user=users[0]).values('contest_class').first()
                user_ids = ClassUser.objects.filter(class_id=contest_class['contest_class']).values('user_id')
                user_ids = [item['user_id'] for item in user_ids]
                real_names = []
                for data in user_ids:
                    real_name = User.objects.filter(user_id=data).values('real_name').first()
                    real_name = real_name['real_name']
                    real_names.append(real_name)
                sumsolved = 0  # 总解题数
                contestNum = []
                contesttime = []
                errcount = []
                sumerrcount = 0
                for num in nums:
                    problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
                    user_first_time = Solution.objects.filter(contest_id=contest_id, user_id=user,
                                                              problem_id=problem_id['problem_id'],
                                                              run_result=4).order_by(
                        'solution_time').values('solution_time').first()
                    errcount_data = self.getContestSubmitFalseCount(contest_id, user, problem_id['problem_id'])
                    sumerrcount = int(errcount_data) + sumerrcount
                    errcount.append(errcount_data)
                    if user_first_time:
                        user_first_time = user_first_time['solution_time']
                        user_first_time = user_first_time - starttime
                        sumsolved = sumsolved + 1
                        rstime = self.timedeltaChange(user_first_time)
                    else:
                        timenow = datetime.datetime.now()
                        user_first_time = timenow - timenow
                        rstime = self.timedeltaChange(user_first_time)
                    num = chr(int(num) + 65)
                    contestNum.append(num)
                    contesttime.append(rstime)
                    sumtime = sumtime + user_first_time
                sumtime = self.timedeltaChange(sumtime)
                contestRank.append(
                    {
                        'user_id': user,
                        'nick': real_names,
                        'sumsolved': sumsolved,
                        'contestNum': contestNum,
                        'contesttime': contesttime,
                        'sumtime': sumtime,
                        'errcount': errcount,
                        'sumerrcount': sumerrcount,
                    }
                )
            contestRank = sorted(contestRank, key=lambda x: (-x["sumsolved"], x['sumtime'], -x['sumerrcount']))
            rs = [contestRank, num_first_time]
            return JsonResponse(rs, safe=False)
# 竞赛oj排名
class contestRankList_oj(View):
    """
        模块: 竞赛作业排名
        接口信息:
        GET:
            contest_id：竞赛id
    """
    # 整数改为时间
    def timeChange(self, time):
        time = str(time)
        if len(time) == 2:
            time = time
        elif len(time) == 1:
            time = '0' + time
        return time
    # 把相隔时间转化为时分秒
    def timedeltaChange(self, time):
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds += time.microseconds / 1e6
        hours = time.days * 24 + hours
        time = "{}:{}:{}".format(hours, self.timeChange(minutes), self.timeChange(int(seconds)))
        return time
    # 竞赛中问题写错的次数
    def getContestSubmitFalseCount(self, contest_id, user_id, num):
        errcount = Solution.objects.filter(contest_id=contest_id, user_id=user_id, problem_id=num).exclude(run_result=4).count()
        return errcount
    def get(self, request):
        contest_id = request.GET.get('contest_id', '')
        if contest_id == '':
            return JsonResponse({'err': '请求失败，contest_id为空'})
        starttime = Contest.objects.filter(contest_id=contest_id).values('start_time').first()
        starttime = starttime['start_time']
        users = ContestUser.objects.filter(contest_id=contest_id).values('contest_user')
        users = [item['contest_user'] for item in users]
        nums = ContestProblem.objects.filter(contest_id=contest_id).values('problem_num')
        nums = [item['problem_num'] for item in nums]
        num_first_time = []
        for num in nums:
            problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
            problem_first_right_time = Solution.objects.filter(contest_id=contest_id, problem_id=problem_id['problem_id'], run_result=4).order_by('solution_time').values(
                'solution_time').first()
            if problem_first_right_time:
                problem_first_right_time = problem_first_right_time['solution_time']
                problem_first_right_time =problem_first_right_time - starttime
                problem_first_right_time = self.timedeltaChange(problem_first_right_time)
            else:
                problem_first_right_time = '00:00:00'
            num_first_time.append(problem_first_right_time)
        contest_class = ContestUser.objects.filter(contest_user=users[0]).values('contest_class').first()
        if contest_class['contest_class'] == None:
            contestRank = []  # 竞赛排序
            total_time = []  # 总时间
            for user in users:
                now = datetime.datetime.now()
                sumtime = now - now
                nick = User.objects.filter(user_id=user).values('user_nick').first()
                nick = nick['user_nick']
                sumsolved = 0  # 总解题数
                contestNum = []
                contesttime = []
                errcount = []
                sumerrcount = 0
                for num in nums:
                    problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
                    user_first_time = Solution.objects.filter(contest_id=contest_id, user_id=user, problem_id=problem_id['problem_id'], run_result=4).order_by(
                        'solution_time').values('solution_time').first()
                    errcount_data = self.getContestSubmitFalseCount(contest_id, user, problem_id['problem_id'])
                    sumerrcount = int(errcount_data) + sumerrcount
                    errcount.append(errcount_data)
                    if user_first_time:
                        user_first_time = user_first_time['solution_time']
                        user_first_time = user_first_time - starttime
                        sumsolved = sumsolved + 1
                        rstime = self.timedeltaChange(user_first_time)
                    else:
                        timenow = datetime.datetime.now()
                        user_first_time = timenow - timenow
                        rstime = self.timedeltaChange(user_first_time)
                    num = chr(int(num) + 65)
                    contestNum.append(num)
                    contesttime.append(rstime)
                    sumtime = sumtime + user_first_time
                sumtime = self.timedeltaChange(sumtime)
                contestRank.append(
                    {
                        'user_id': user,
                        'nick': nick,
                        'sumsolved': sumsolved,
                        'score': sumsolved*100,
                        'contestNum': contestNum,
                        'contesttime': contesttime,
                        'sumtime': sumtime,
                        'errcount': errcount,
                        'sumerrcount': sumerrcount,
                    }
                )
            contestRank = sorted(contestRank, key=lambda x: (-x["sumsolved"], x['sumtime'], -x['sumerrcount']))
            rs = [contestRank, num_first_time]
            return JsonResponse(rs, safe=False)
        else:
            contestRank = []  # 竞赛排序
            total_time = []  # 总时间
            for user in users:
                now = datetime.datetime.now()
                sumtime = now - now
                contest_class = ContestUser.objects.filter(contest_user=users[0]).values('contest_class').first()
                user_ids = ClassUser.objects.filter(class_id=contest_class['contest_class']).values('user_id')
                user_ids = [item['user_id'] for item in user_ids]
                real_names = []
                for data in user_ids:
                    real_name = User.objects.filter(user_id=data).values('real_name').first()
                    real_name = real_name['real_name']
                    real_names.append(real_name)
                sumsolved = 0  # 总解题数
                contestNum = []
                contesttime = []
                errcount = []
                sumerrcount = 0
                for num in nums:
                    problem_id = ContestProblem.objects.filter(problem_num=num).values('problem_id').first()
                    user_first_time = Solution.objects.filter(contest_id=contest_id, user_id=user,
                                                              problem_id=problem_id['problem_id'],
                                                              run_result=4).order_by(
                        'solution_time').values('solution_time').first()
                    errcount_data = self.getContestSubmitFalseCount(contest_id, user, problem_id['problem_id'])
                    sumerrcount = int(errcount_data) + sumerrcount
                    errcount.append(errcount_data)
                    if user_first_time:
                        user_first_time = user_first_time['solution_time']
                        user_first_time = user_first_time - starttime
                        sumsolved = sumsolved + 1
                        rstime = self.timedeltaChange(user_first_time)
                    else:
                        timenow = datetime.datetime.now()
                        user_first_time = timenow - timenow
                        rstime = self.timedeltaChange(user_first_time)
                    num = chr(int(num) + 65)
                    contestNum.append(num)
                    contesttime.append(rstime)
                    sumtime = sumtime + user_first_time
                sumtime = self.timedeltaChange(sumtime)
                contestRank.append(
                    {
                        'user_id': user,
                        'nick': real_names,
                        'sumsolved': sumsolved,
                        'score': sumsolved * 100,
                        'contestNum': contestNum,
                        'contesttime': contesttime,
                        'sumtime': sumtime,
                        'errcount': errcount,
                        'sumerrcount': sumerrcount,
                    }
                )
            contestRank = sorted(contestRank, key=lambda x: (-x["sumsolved"], x['sumtime'], -x['sumerrcount']))
            rs = [contestRank, num_first_time]
            return JsonResponse(rs, safe=False)
# 竞赛统计
class contestStatistics(View):
    """
        模块: 竞赛统计
        接口信息:
        GET:
            contest_id：竞赛id
       """
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        if contest_id is None:
            return JsonResponse({'status': False, 'message': '请求失败，contest_id为空'})
        nums = ContestProblem.objects.filter(contest_id=contest_id).values('problem_num')
        nums = [item['problem_num'] for item in nums]
        problem_data = []
        for num in nums:
            problem_id = ContestProblem.objects.filter(contest_id=contest_id, problem_num=num).values('problem_id').first()
            problem_id = problem_id['problem_id']
            statistics = [0, 0, 0, 0, 0, 0, 0, 0]
            problem_all = Solution.objects.filter(contest_id=contest_id, problem_id=problem_id).all()
            total = Solution.objects.filter(contest_id=contest_id, problem_id=problem_id).all().count()
            for data in problem_all:
                statistics[data.run_result - 4] += 1
            num = chr(int(num) + 65)
            problem_data.append(
                {
                    'problem_id': problem_id,
                    'num': num,
                    'statistics': statistics,
                    'TR': 'TR',
                    'total': total
                }
            )
        return JsonResponse(problem_data, safe=False)
# 管理员竞赛页面
class Admincontest(View):
    """
        模块: 管理员竞赛页面
        接口信息:
        GET:
            token：token认证
            page：页数
    """
    def judgeContest(self, contest_id):
        time = datetime.datetime.now()
        time = time.replace(tzinfo=utc)
        starttime = Contest.objects.filter(contest_id=contest_id).values('start_time').first()
        starttime = starttime['start_time']
        endtime = Contest.objects.filter(contest_id=contest_id).values('end_time').first()
        endtime = endtime['end_time']
        if time <= endtime and time >= starttime:
            return True
        else:
            return False
    def get(self, request):
        token = request.GET.get('token')
        page = int(request.GET.get('page', 1))
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        contest = Contest.objects.filter().all().order_by('-contest_id')[(page - 1) * 50: page * 50]
        contest_data = []
        for data in contest:
            contest_id = data.contest_id
            starttime = Contest.objects.filter(contest_id=contest_id).values('start_time').first()
            starttime = starttime['start_time']
            starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')
            endtime = Contest.objects.filter(contest_id=contest_id).values('end_time').first()
            endtime = endtime['end_time']
            endtime = datetime.datetime.strftime(endtime, '%Y-%m-%d %H:%M:%S')
            if self.judgeContest(contest_id):
                err = '@进行中'
            else:
                err = '@已结束'
            contest_data.append(
                {
                    'contest_id': contest_id,
                    'title': data.contest_title,
                    'province': data.contest_province,
                    'starttime': starttime,
                    'end_time': endtime,
                    'status': err,
                    'creator': data.contest_creator
                }
            )
        return JsonResponse({'status': 'Ture', 'contest': contest_data})


# 修改竞赛
class changeContest(View):
    """
        模块: 修改竞赛
        接口信息:
        GET:
            token：token认证
            contest_id：竞赛id
        POST:
            token：token认证
            title: 标题
            start_time：开始时间
            end_time：结束时间
            problem：问题编号
            description：描述
            language：编程语言类型
            province：类型
            password：密码
            class_name：班级名称
            users：竞赛用户
    """
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        if not contest_id:
            return JsonResponse({'err': '请求失败，contest_id为空'})
        creator = Contest.objects.filter(contest_id=contest_id).values('creator')
        if identity not in [0, 1] and user_id != creator[0]['creator']:
            return JsonResponse({'err': 'No permission'})
        contest = Contest.objects.filter(contest_id=contest_id).all()
        contest = changeToJson(contest)
        return JsonResponse(contest, safe=False)
    def post(self, request):
        token = request.POST.get('token')
        contest_id = request.POST.get('contest_id')
        title = request.POST.get('contest_title')  # 比赛名称
        start_time = request.POST.get('start_time')  # 开始时间
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = request.POST.get('end_time')  # 结束时间
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        problem = request.POST.get('problem')  # 问题编号
        description = request.POST.get('contest_introduce')  # 竞赛描述
        language = request.POST.get('contest_language')  # 编程语言类型
        province = request.POST.get('contest_province')  # 竞赛类型
        password = request.POST.get('contest_password')  # 密码
        class_name = request.POST.get('class_name')  # 班级名称
        users = request.POST.get('user_id')  # 竞赛用户
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        if not contest_id:
            return JsonResponse({'err': '请求失败，contest_id为空'})
        creator = Contest.objects.filter(contest_id=contest_id).values('contest_creator').first()
        if identity not in [0, 1] and user_id != creator['creator']:
            return JsonResponse({'err': 'No permission'})
        # if not (title and start_time and end_time and problem and description and province and language and users and class_name):
        #     return JsonResponse({'massage': '未作任何修改'})
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if title:
            contest.contest_title = title
        if start_time:
            contest.start_time = start_time
        if end_time:
            contest.end_time = end_time
        if description:
            contest.contest_introduce = description
        if province:
            contest.contest_province = province
        if password:
            contest.contest_password = password
        if language:
            contest.contest_language = language
        contest.save()
        if class_name:
            ContestUser.objects.filter(contest_id=contest.contest_id).delete()
            class_id = Class.objects.filter(class_name=class_name).values('class_id').first()
            user_ids = ClassUser.objects.filter(class_id=class_id['class_id']).values('user_id')
            user_ids = [item['user_id'] for item in user_ids]
            for data in user_ids:
                ContestUser.objects.create(
                    contest_id=contest.contest_id,
                    contest_user=data,
                    contest_class=class_id['class_id']
                )
        if users:
            ContestUser.objects.filter(contest_id=contest.contest_id).delete()
            users = users.split('\n')
            for datas in users:
                ContestUser.objects.create(
                    contest_id=contest.contest_id,
                    contest_user=datas,
                )
        if problem:
            problem = problem.split('，')
            ContestProblem.objects.filter(contest_id=contest.contest_id).delete()
            status = 0  # 判断问题是否在关卡中
            num = 0
            for problem_id in problem:
                level_problems = LevelProblem.objects.all()
                for level_problem in level_problems:
                    if problem_id == str(level_problem.problem_id):
                        status = 1
                if status == 1:
                    return JsonResponse({'status': 'false', 'message': '您所添加的问题在关卡中已存在'})
                ContestProblem.objects.create(
                    problem_id=problem_id,
                    contest_id=contest.contest_id,
                    problem_num=num
                )
                num += 1
        massage = {'status': 'ture', 'message': '修改成功'}
        return JsonResponse(massage, safe=False)

# 删除竞赛
class deleteContest(View):
    """
        模块: 删除竞赛
        接口信息:
        GET:
            None
        POST:
            contest_id：竞赛id
            token：token认证
    """
    def get(self, request):
        massage = {'err': 'Wrong request method'}
        return JsonResponse(massage, safe=False)
    def post(self, request):
        token = request.POST.get('token')
        contest_id = request.POST.get('contest_id')
        if not contest_id:
            return JsonResponse({'err': '请求失败，contest_id为空'})
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        creator = Contest.objects.filter(contest_id=contest_id).values('contest_creator').first()
        if identity not in [0, 1] and user_id != creator['creator']:
            return JsonResponse({'err': 'No permission'})
        ContestUser.objects.filter(contest_id=contest_id).delete()
        ContestProblem.objects.filter(contest_id=contest_id).delete()
        Contest.objects.filter(contest_id=contest_id).delete()
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if contest:
            massage = {'err': 'Deletion failed'}
        else:
            massage = {'err': 'Successfully deleted'}
        return JsonResponse(massage, safe=False)

#最近竞赛
class getLateContest(View):
    """
            模块: 消息广播 获取最近竞赛列表
            接口信息:
            GET:
                返回正在比赛中的竞赛列表
            POST:
                传参：contest_id,token
                返回该竞赛的所有参赛成员信息
        """

    def get(self,request):
        keyword = request.GET.get('keyword','')
        token = request.GET.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error']})
        contestList=[]
        if keyword=='' or keyword==None:
            data = Contest.objects.filter(end_time__gte=datetime.datetime.now().date(),contest_defunct='0')
            for d in data:
                contestList.append({
                    'contest_id':d.contest_id,
                    'title':d.contest_title
                })
        else:
            keynum = 0
            if keyword.isdigit():
                keynum = int(keyword)
            data = Contest.objects.filter(Q(contest_title__contains=keyword)|Q(contest_id__exact=keynum)).filter(contest_defunct='0')
            for d in data:
                contestList.append({
                    'contest_id':d.contest_id,
                    'title':d.contest_title
                })
        return JsonResponse({'status': True, 'err': "success",'data':contestList})

    def post(self,request):
        contest_id = int(request.POST.get('contest_id',0))
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'],"data":[]})
        if contest_id ==0:
            return JsonResponse({'status': False, 'err': "contest_id not existence","data":[]})
        ClassUsers=[]
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT contest_user.contest_user,user.user_name,user.user_nick from contest_user LEFT JOIN user on contest_user.contest_user = user.user_id WHERE contest_user.contest_id = %s",
                    [contest_id])
            classUsers = cursor.fetchall()
            classUsers = list(classUsers)
        except:
            return JsonResponse({'status': False, 'err': "Database connection failed","data":[]})


        data=[]
        for classUser in classUsers:
            data.append({
                "user_id":classUser[0],
                "user_name":classUser[1],
                "user_nick":classUser[2]
            })
        return JsonResponse({'status': True, 'err': "success","data":data})