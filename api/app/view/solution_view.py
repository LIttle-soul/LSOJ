from django.http import JsonResponse
from django.views.generic import View
from app.RoleMethod.PublicMethod import PublicMethod
from django.core.cache import cache
from app.models import *
from datetime import datetime
from django.utils import timezone

publicMethod = PublicMethod()

class ProblemSubmission(View):
    """
    模块: 题目提交
    接口信息:
        GET:
            token:token认证
            method:POST方法
        POST:
            None
    返回信息：
        GET:
            None
        POST:
            result:提交结果【submitPass】
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            data = JsonResponse({'status': False, 'message': '用户未登录'})
            data.delete_cookie('token')
            return data
        cache.touch(token, 7200)
        problem_id = request.POST.get('problem_id')
        solution_language = request.POST.get('solution_language')
        level_id = request.POST.get('level_id')
        if level_id == 'null':
            level_id = None
        contest_id = request.POST.get('contest_id')
        if contest_id == 'null':
            contest_id = -1
        # code_length = request.POST.get('code_length')
        solution_code = request.POST.get('solution_code')
        solution_ip = publicMethod.get_ip(request)
        # print(problem_id, solution_ip, solution_language, level_id, contest_id, solution_code)
        # run_time = request.POST.get('run_time')
        # run_memory = request.POST.get('run_memory ')
        # run_error = request.POST.get('run_error')
        # run_result = request.POST.get('run_result ')
        if all([problem_id]):  # all() 所有内容不为 0 、‘’、false
            solution = Solution.objects.create(
                problem_id=problem_id,
                user_id=user_id,
                contest_id=contest_id,
                solution_code=solution_code,
                solution_language=solution_language,
                solution_time=timezone.now(),
                solution_ip=solution_ip,
                # code_length=code_length,
                # run_time=run_time,
                # run_memory=run_memory,
                # run_result=run_result,
                # run_error=run_error
            )
            if level_id is not None:
                solution_id = solution.solution_id
                s_result = solution.run_result
                s_result = 1 if s_result == 4 else 2
                lps = LevelProblemSubmit.objects.filter(level_id=level_id, problem_id=problem_id, user_id=user_id).first()
                if not lps.exit():
                    LevelProblemSubmit.objects.create(
                        level_id=level_id,
                        problem_id=problem_id,
                        user_id=user_id,
                        status=s_result,
                        solution_id=solution_id
                    )
                elif lps.status == 2:
                    LevelProblemSubmit.objects.filter(level_id=level_id, problem_id=problem_id, user_id=user_id).update(
                        status=s_result,
                        solution_id=solution_id,
                        submit_time=datetime.now()
                    )
                level_submit = LevelProblemSubmit.objects.filter(level_id=level_id, status=1).count()
                if level_submit == Level.objects.filter(level_id=level_id).first().pass_num:
                    lp = LevelPass.objects.filter(user_id=user_id, level_id=level_id)
                    if not lp.exit():
                        LevelPass.objects.create(
                            level_id=level_id,
                            user_id=user_id,
                        )
            return JsonResponse({'status': True, 'message': '提交成功', 'solution_id': solution.solution_id})
        else:
            return JsonResponse({'status': False, 'message': '消息不全'})

class StatusSubmit(View):
    """
    模块: 查询题目提交状态
    接口信息:
        GET:
            None
        POST:
            None
    返回信息：
        GET:
            None
        POST:
            result:rank_date【状态列表】
    """
    def get(self, request):
        contest_id = request.GET.get('contest_id')
        message = []
        if contest_id is not None:
            solution = Solution.objects.filter(contest_id=contest_id)
            problems = ContestProblem.objects.filter(contest_id=contest_id)
            problem_num = dict()
            for problem in problems:
                problem_num[problem.problem_id] = chr(problem.problem_num + 65)
            for data in solution:
                message.append({
                    'solution_id': data.solution_id,
                    'user_id': data.user_id,
                    'problem_id': data.problem_id,
                    'problem_num': problem_num[data.problem_id],
                    'contest_id': data.contest_id,
                    'run_result': data.run_result,
                    'run_memory': data.run_memory,
                    'run_time': data.run_time,
                    'run_error': data.run_error,
                    'solution_language': data.solution_language,
                    'code_length': data.code_length,
                    'solution_time': data.solution_time,
                    'solution_code': data.solution_code,
                    'solution_ip': data.solution_ip,
                    'run_pass_rate': data.run_pass_rate,
                    'run_all_rate': data.run_all_rate
                })
        else:
            solution = Solution.objects.filter(contest_id='-1')
            for data in solution:
                message.append({
                    'solution_id': data.solution_id,
                    'user_id': data.user_id,
                    'problem_id': data.problem_id,
                    'contest_id': data.contest_id,
                    'run_result': data.run_result,
                    'run_memory': data.run_memory,
                    'run_time': data.run_time,
                    'run_error': data.run_error,
                    'solution_language': data.solution_language,
                    'code_length': data.code_length,
                    'solution_time': data.solution_time,
                    'solution_code': data.solution_code,
                    'solution_ip': data.solution_ip,
                    'run_pass_rate': data.run_pass_rate,
                    'run_all_rate': data.run_all_rate
                })
        return JsonResponse({'status': True, 'message': message})


class OneSolutionStatus(View):
    def get(self, request):
        solution_id = request.GET.get('solution_id')
        solution = Solution.objects.filter(solution_id=solution_id).first()
        if not solution:
            return JsonResponse({'status': False, 'message': '未提交'})
        message = {
            'solution_id': solution.solution_id,
            'user_id': solution.user_id,
            'problem_id': solution.problem_id,
            'contest_id': solution.contest_id,
            'run_result': solution.run_result,
            'run_memory': solution.run_memory,
            'run_time': solution.run_time,
            'run_error': solution.run_error,
            'solution_language': solution.solution_language,
            'code_length': solution.code_length,
            'solution_time': solution.solution_time,
            'solution_code': solution.solution_code,
            'solution_ip': solution.solution_ip,
            'run_pass_rate': solution.run_pass_rate,
            'run_all_rate': solution.run_all_rate
        }
        return JsonResponse({'status': True, 'message': message})
