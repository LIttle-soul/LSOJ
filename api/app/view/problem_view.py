from django.http import JsonResponse
from django.views.generic import View
from app.RoleMethod.PublicMethod import PublicMethod
from app.models import *
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime
from app.config import config
from django.db.models import Q
import os

publicMethod = PublicMethod()


class GetProblemList(View):
    """
    模块: 获取题目列表
    接口信息:
        GET:
            token: token认证
    返回信息：
        GET:
            message: 数据库内所有的题目信息
    """

    def get(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        page = request.GET.get("page")
        total = request.GET.get("total")
        key = request.GET.get("key")
        text = request.GET.get("text")
        problems = Problem.objects.all()
        solution = Solution.objects.all()
        print(page, total, key, text, user_id)
        if key:
            if key == 'search':
                problems = problems.filter(Q(problem_id__contains=text) | Q(problem_title__contains=text) | Q(
                    problem_tag__contains=text) | Q(problem_course__contains=text))
            elif key == 'id':
                problems = problems.filter(problem_id=text)
            elif key == 'difficult':
                problems = problems.filter(problem_difficult=text)
            else:
                return JsonResponse({'status': False, 'message': 'key值出错'})
        problem_num = problems.count()
        if total == '0':
            problems = problems[int(page) - 1:]
        else:
            problems = problems[(int(page) - 1) * int(total): int(page) * int(total)]
        problem_list = []
        for problem in problems:
            if user_id:
                problem_ture = solution.filter(contest_id='-1', problem_id=problem.problem_id,
                                                       user_id=user_id, run_result=4).first()
                problem_false = solution.filter(contest_id='-1', problem_id=problem.problem_id,
                                                        user_id=user_id).first()
                if problem_ture:
                    result = 1
                elif problem_false:
                    result = -1
                else:
                    result = 0
            else:
                result = 0
            problem_list.append({
                'problem_id': problem.problem_id,
                'problem_title': problem.problem_title,
                'problem_description': problem.problem_description,
                'problem_spj': problem.problem_spj,
                'problem_course': problem.problem_course,
                'creation_time': problem.creation_time,
                'time_limit': problem.time_limit,
                'memory_limit': problem.memory_limit,
                'problem_tag': problem.problem_tag,
                'problem_difficult': problem.problem_difficult,
                'problem_solved': problem.problem_solved,
                'problem_submit': problem.problem_submit,
                'problem_creator': problem.problem_creator,
                'problem_status': problem.problem_status,
                'pass_status': result,
            })

        return JsonResponse({'status': True, 'message': problem_list, 'total': problem_num})


# class GetProblemInfo(View):
#     """
#     模块: 获取题目信息（暂存）
#     接口信息:
#         GET:
#             problem_id:问题id
#         POST:
#             None
#     返回信息：
#         GET:
#             None
#         POST:
#            rank：题目信息
#     """
#     def get(self, request):
#         problem_id = request.GET.get('problem_id')
#         problems = Problem.objects.filter(problem_id=problem_id).all()
#         rank_data = []
#         for data in problems:
#             submit = Solution.objects.filter(problem_id=data.problem_id).count()
#             accepted = Solution.objects.filter(problem_id=data.problem_id, run_result=True).count()
#             rank_data.append(
#                 {
#                     'problem_id': data.problem_id,
#                     'problem_title': data.problem_title,
#                     'problem_description': data.problem_description,
#                     'problem_course': data.problem_course,
#                     'problem_tag': data.problem_tag,
#                     'time_limit': data.time_limit,
#                     'memory_limit': data.memory_limit,
#                     'problem_difficult': data.problem_difficult,
#                     'problem_submit': submit,
#                     'problem_accepted': accepted,
#                 }
#             )
#         return JsonResponse({'status': True, 'message': rank_data})
#
#     def post(self, request):
#         pass


class GetProblemTag(View):
    def get(self, request):
        problems = Problem.objects.all()
        tags = problems.values_list('problem_tag').distinct()
        courses = problems.values_list('problem_course').distinct()
        tags_list = []
        courses_list = []
        for tag in tags:
            if not tag[0]:
                continue
            item = tag[0].split(',')
            for it in item:
                if it != '':
                    tags_list.append(it)
        for course in courses:
            if not course[0]:
                continue
            item = course[0].split(',')
            for it in item:
                if it != '':
                    courses_list.append(it)
        return JsonResponse({'status': True, 'tag': list(set(tags_list)), 'course': list(set(courses_list))})


class AddProblem(View):
    """
    模块: 题目添加
    接口信息:
        GET:
            token:token认证
            method:Post方法
        post:
            None
    返回信息：
        GET:
            None
        post:
            result:添加结果【'addPass': problem_id, 'message': 'true'】/【'addError': 'lose something'】
    """

    def get(self, request):
        pass

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        print(token, user_id)
        if not user_id:
            return JsonResponse({'status': False, 'message': '用户未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        if capacity != 0 and capacity != 1:
            return JsonResponse({'status': False, 'message': '没有权限'})
        problem_id = request.POST.get('problem_id')
        problem = Problem.objects.filter(problem_id=problem_id)
        if problem.exists():
            return JsonResponse({'status': False, 'message': '这个问题ID已使用'})
        problem_title = request.POST.get('problem_title')
        problem_description = request.POST.get('problem_description')
        problem_spj = request.POST.get('problem_spj')
        if problem_spj in ['false', 'FALSE']:
            problem_spj = False
        elif problem_spj in ['true', 'TRUE']:
            problem_spj = True
        problem_course = request.POST.get('problem_course')
        time_limit = request.POST.get('time_limit')
        memory_limit = request.POST.get('memory_limit')
        problem_tag = request.POST.get('problem_tag')
        problem_difficult = request.POST.get('problem_difficult')
        if all([problem_title, problem_description]):
            Problem.objects.create(
                problem_id=problem_id,
                problem_title=problem_title,
                problem_description=problem_description,
                problem_spj=problem_spj,
                problem_course=problem_course,
                creation_time=timezone.now,
                time_limit=time_limit,
                memory_limit=memory_limit,
                problem_tag=problem_tag,
                problem_difficult=problem_difficult,
                problem_creator=user_id,
            )
            message = {'status': True, 'message': '添加成功'}
        else:
            message = {'status': False, 'message': '消息不全'}
        return JsonResponse(message)

    def put(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '用户未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        if capacity != 0 and capacity != 1:
            return JsonResponse({'status': False, 'message': '没有权限'})
        problem_id = request.GET.get('problem_id')
        problem = Problem.objects.filter(problem_id=problem_id).first()
        problem_title = request.GET.get('problem_title')
        if problem_title:
            problem.problem_title = problem_title
        problem_description = request.GET.get('problem_description')
        if problem_description:
            problem.problem_description = problem_description
        problem_spj = request.GET.get('problem_spj')
        if problem_spj:
            if problem_spj in ['false', 'FALSE']:
                problem_spj = False
            elif problem_spj in ['true', 'TRUE']:
                problem_spj = True
            problem.problem_spj = problem_spj
        problem_course = request.GET.get('problem_course')
        if problem_course:
            problem.problem_course = problem_course
        time_limit = request.GET.get('time_limit')
        if time_limit:
            problem.time_limit = time_limit
        memory_limit = request.GET.get('memory_limit')
        if memory_limit:
            problem.memory_limit = memory_limit
        problem_tag = request.GET.get('problem_tag')
        if problem_tag:
            problem.problem_tag = problem_tag
        problem_difficult = request.GET.get('problem_difficult')
        if problem_difficult:
            problem.problem_difficult = problem_difficult
        problem_status = request.GET.get('problem_status')
        if problem_status:
            if problem_status in ['false', 'FALSE']:
                problem_status = False
            elif problem_status in ['true', 'TRUE']:
                problem_status = True
            problem.problem_status = problem_status
        problem.save()
        message = {'status': True, 'message': '修改成功'}
        return JsonResponse(message)

    def delete(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '用户未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        if capacity != 0 and capacity != 1:
            return JsonResponse({'status': False, 'message': '没有权限'})
        problem_id = request.GET.get('problem_id')
        problem = Problem.objects.filter(problem_id=problem_id).first()
        if problem:
            problem.delete()
            Solution.objects.filter(problem_id=problem_id).delete()
            massage = {'status': True, 'message': '删除成功'}
        else:
            massage = {'status': False, 'message': '没有这个问题'}
        return JsonResponse(massage)


class ChangeProblem(View):
    """
    模块: 题目修改
    接口信息:
        GET:
            token:token认证
            method:Post方法
        POST:
            None
    返回信息：
        GET:
            None
        POST:
            err:错误信息【用户未登录】/【没有权限】
            massage:修改结果
    """

    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '用户未登录'})
        capacity = publicMethod.get_user_capacity(token)
        if capacity != 0 and capacity != 1:
            return JsonResponse({'status': False, 'message': '没有权限'})
        problem_id = request.GET.get('problem_id')
        problem = Problem.objects.filter(problem_id=problem_id)
        rank_data = []
        for data in problem:
            rank_data.append(
                {
                    'problem_id': data.problem_id,
                    'problem_title': data.problem_title,
                    'problem_description': data.problem_description,
                    'problem_spj': data.problem_spj,
                    'problem_course': data.problem_course,
                    'creation_time': data.creation_time,
                    'time_limit': data.time_limit,
                    'memory_limit': data.memory_limit,
                    'problem_tag': data.problem_tag,
                    'problem_difficult': data.problem_difficult,
                    'problem_creator': data.problem_creator,
                    'problem_status': data.problem_status,
                }
            )
        return JsonResponse({'status': True, 'message': rank_data})

    def post(self, request):
        if request.method == 'POST':
            problem_id = int(request.POST.get('problem_id'))
            data = Problem.objects.get(problem_id=problem_id)
            problem_title = request.POST.get('problem_title')
            problem_description = request.POST.get('problem_description')
            problem_spj = request.POST.get('problem_spj')
            problem_course = request.POST.get('problem_course')
            creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = int(request.POST.get('time_limit'))
            memory_limit = int(request.POST.get('memory_limit'))
            problem_tag = request.POST.get('problem_tag')
            problem_difficult = int(request.POST.get('problem_difficult'))
            problem_creator = request.POST.get('problem_creator')
            problem_status = int(request.POST.get('problem_status'))
            if data:
                data.problem_id = problem_id
                data.problem_title = problem_title
                data.problem_description = problem_description
                data.problem_spj = problem_spj
                data.problem_course = problem_course
                data.creation_time = creation_time
                data.time_limit = time_limit
                data.memory_limit = memory_limit
                data.problem_tag = problem_tag
                data.problem_difficult = problem_difficult
                data.problem_creator = problem_creator
                data.problem_status = problem_status
                data.save()
                message = {'message': 'modify succeeded'}
            else:
                Problem.objects.create(
                    problem_id=problem_id,
                    problem_title=problem_title,
                    problem_description=problem_description,
                    problem_spj=problem_spj,
                    problem_course=problem_course,
                    creation_time=creation_time,
                    time_limit=time_limit,
                    memory_limit=memory_limit,
                    problem_tag=problem_tag,
                    problem_difficult=problem_difficult,
                    problem_creator=problem_creator,
                    problem_status=problem_status
                )
                message = {'message': 'add succeeded'}
            return JsonResponse({'status': True, 'message': message})


# class DeleteProblem(View):
#     """
#     模块: 题目删除(暂存)
#     接口信息:
#         GET:
#             token:token认证
#             method:Post方法
#         POST:
#             None
#     返回信息：
#     GET:
#         None
#     POST:
#         err:错误信息【用户未登录】/【没有权限】
#         massage:重判结果
#     """
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         token = request.POST.get('token')
#         user_id = publicMethod.check_user_login(token)
#         if not user_id:
#             return JsonResponse({'status': False, 'message': '用户未登录'})
#         capacity = publicMethod.get_user_capacity(token)
#         if capacity != 0 and capacity != 1:
#             return JsonResponse({'status': False, 'message': '没有权限'})
#         problem_id = request.POST.get('problem_id')
#         problem = Problem.objects.filter(problem_id=problem_id)
#         if problem:
#             problem.delete()
#             massage = {'pass': 'Delete succeeded'}
#         else:
#             massage = {'err': 'Delete failed'}
#         return JsonResponse(massage)


class ReprimandProblem(View):
    """
    模块: 题目重判
    接口信息:
        GET:
            token:token认证
            method:Post方法
        POST:
            None
    返回信息：
        GET:
            None
        POST:
            err:错误信息【用户未登录】/【没有权限】
            massage:重判结果
    """

    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '用户未登录'})
        capacity = publicMethod.get_user_capacity(token)
        if capacity != 0 and capacity != 1:
            return JsonResponse({'err': '没有权限'})
        problem_id = request.POST.get('problem_id')
        if problem_id:
            problems = Solution.objects.filter(problem_id=problem_id).all()
            if problems:
                for data in problems:
                    Solution.objects.create(
                        problem_id=data.problem_id,
                        user_id=data.user_id,
                        contest_id=data.contest_id,
                        solution_code=data.solution_code,
                        solution_language=data.solution_language,
                        solution_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        code_length=data.code_length,
                        run_pass_rate=data.run_pass_rate,
                        run_all_rate=data.run_all_rate
                    )
                    message = {'massage': 'yes'}
            else:
                message = {'err': 'failed'}
        else:
            message = {'err': 'failed'}
        return JsonResponse(message, safe=False)


class UpImage(View):
    def post(self, request):
        images = request.FILES.get('images')
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        if user_id:
            print(images)
            obj = FilePath.objects.create(
                file_path=images,
                file_creator=user_id,
                file_time=timezone.now()
            )
            message = {'status': True, 'message': str(obj.file_path)}
        else:
            message = {'status': False, 'message': '未登录'}
        return JsonResponse(message)


class ImageList(View):
    def get(self, request):
        images = FilePath.objects.all()
        image_list = []
        for image in images:
            image_list.append({
                'file_id': image.file_id,
                'file_path': str(image.file_path),
                'file_creator': image.file_creator,
                'file_time': image.file_time
            })
        return JsonResponse({'status': True, 'message': image_list})


class ProblemSample(View):
    def get(self, request):
        problem_id = request.GET.get('problem_id')
        print(problem_id)
        target_path = config.PROBLEM_DATA
        target_path = os.path.join(target_path, problem_id)
        if not os.path.exists(target_path):
            return JsonResponse({'status': True, 'message': []})
        dir_list = os.listdir(target_path)
        files_list = []
        for file in dir_list:
            paths = os.path.join(target_path, file)
            name, ext = file.split('.')
            with open(paths) as f:
                text = f.read()
            files_list.append({
                'files_name': file,
                'create_time': os.path.getctime(paths),
                'files_size': os.path.getsize(paths),
                'files_ext': ext,
                'files_text': text
            })
        return JsonResponse({'status': True, 'message': files_list})

    def post(self, request):
        files = request.FILES.get('files')
        problem_id = request.POST.get('problem_id')
        print(problem_id)
        target_path = config.PROBLEM_DATA
        target_path = os.path.join(target_path, problem_id)
        if not os.path.exists(target_path):
            os.mkdir(target_path)
        if isinstance(files, list):
            for file in files:
                path = os.path.join(target_path, file.name)
                if file:
                    with open(path, 'wb') as f:
                        f.write(file.read())
        else:
            path = os.path.join(target_path, files.name)
            if files:
                with open(path, 'wb') as f:
                    f.write(files.read())
        return JsonResponse({'status': True, 'message': '上传成功'})

    def put(self, request):
        problem_id = request.GET.get('problem_id')
        files_name = request.GET.get('files_name')
        files_text = request.GET.get('files_text')
        print(files_name)
        target_path = config.PROBLEM_DATA
        target_path = os.path.join(target_path, problem_id, files_name)
        if os.path.exists(target_path):
            with open(target_path, 'w') as f:
                f.write(files_text)
            return JsonResponse({'status': True, 'message': '修改成功'})
        else:
            return JsonResponse({'status': False, 'message': '没有这个文件'})

    def delete(self, request):
        problem_id = request.GET.get('problem_id')
        files_name = request.GET.get('files_name')
        print(files_name)
        target_path = config.PROBLEM_DATA
        target_path = os.path.join(target_path, problem_id, files_name)
        if os.path.exists(target_path):
            os.remove(target_path)
            return JsonResponse({'status': True, 'message': '删除成功'})
        else:
            return JsonResponse({'status': True, 'message': '没有这个文件'})

    def patch(self, request):
        problem_id = request.GET.get('problem_id')
        files_name = request.GET.get('files_name')
        new_name = request.GET.get('new_name')
        if files_name == new_name:
            return JsonResponse({'status': False, 'message': '新名字不能和老名字一样'})
        target_path = config.PROBLEM_DATA
        target_path = os.path.join(target_path, problem_id)
        new_path = os.path.join(target_path, new_name)
        target_path = os.path.join(target_path, files_name)
        print(target_path, new_path)
        if os.path.exists(target_path):
            os.rename(target_path, new_path)
            return JsonResponse({'status': True, 'message': '文件名修改成功'})
        else:
            return JsonResponse({'status': False, 'message': '没有这个文件'})
