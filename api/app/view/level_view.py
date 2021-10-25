from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from app.models import *
from django.core.cache import cache
from app.RoleMethod.PublicMethod import PublicMethod

publicMethod = PublicMethod()


# 添加关卡
class addLevel(View):
    """
    方法：GET
    请求参数：
        type:关卡类型
        token：用户验证
    返回数据：
        levels:当type=1即进行添加关卡时，返回所有的关卡和大类数据
        当类型为2时不返回数据
    """

    def get(self, request):
        type = int(request.GET.get('type', -1))
        token = request.COOKIES.get('token')
        if publicMethod.get_user_capacity(token) != 0:
            return JsonResponse({'status': False, 'err': 'You do not have permission to operate'})
        if not token:
            return JsonResponse({'status': False, 'err': 'You need to log in to add levels'})
        if not type or type < 0:
            return JsonResponse({'status': False, 'err': 'Some parameters are missing'})
        # 添加关卡，需要返回大类，和关卡信息，供用户选择
        # 若为添加关卡，则需要返回关卡大类和关卡供用户选择
        if type == 1:
            levelKind = Level.objects.only('level_id', 'title', 'num').filter(type=2, isdelete=0).order_by('num')
            levels = Level.objects.only('level_id', 'title', 'num', 'front_id').filter(type=1, isdelete=0).order_by(
                'front_id', 'num')
            data = []
            for kind in levelKind:
                k = []
                for level in levels:
                    if (kind.level_id == level.front_id):
                        k.append({
                            'id': level.level_id,
                            'title': level.title,
                            'num': level.num
                        })
                data.append({
                    'id': kind.level_id,
                    'title': kind.title,
                    'num': kind.num,
                    'levels': k
                })
            message = {'status': True, 'levels': data}
            return JsonResponse(message, safe=False)
        # 类型为2时即添加关卡大类，此时是get请求不需要返回任何值
        elif type == 2:
            return JsonResponse({'status': False, 'err': 'There is nothing to return'})
        else:
            return JsonResponse({'status': False, 'err': 'type is wrong'})

    """
    方法：POST
    请求参数：
        type:关卡类型 1关卡，2大类
        token：用户验证
        title:关卡标题
        description:描述
        type=1:

        type=2:

    返回数据：

    """

    def post(self, request):
        type = int(request.POST.get('type', -1));
        token = request.COOKIES.get('token')
        title = request.POST.get('title', None)
        description = request.POST.get('description', '')
        userNick = publicMethod.get_user_nick(token)
        userId = publicMethod.check_user_login(token)
        if userId == None:
            return JsonResponse({'status': False, 'err': 'The token is invalid'})
        if not token:
            return JsonResponse({'status': False, 'err': 'You need to log in to add levels'})
        if (publicMethod.get_user_capacity(token) != 0):
            return JsonResponse({'status': False, 'err': 'You do not have permission to operate'})
        if not type or type < 0:
            return JsonResponse({'status': False,
                                 'err': 'What wrong with you?What information do you want to add?The type parameter is missing.'})
        if title == None or title == '':
            return JsonResponse({'status': False, 'err': 'Some parameters are missing'})
        if type == 1:
            levelPre = request.POST.get('level_pre', None)
            fonrtId = int(request.POST.get('front_id'), 0)
            passNum = int(request.POST.get('pass_num'), 0)
            num = Level.objects.filter(front_id=fonrtId).count() + 1;
            problems = str(request.POST.get('problems')).split(',')

            if title == None or title == '' or fonrtId == 0 or problems == None or problems == '':
                return JsonResponse({'status': False, 'err': 'Some parameters are missing'})

            # 判断问题格式是否正确
            for problem in problems:
                if not problem.isdigit():
                    return JsonResponse({'status': False, 'er': 'Problem ID field format error'})
                if int(problem) < 1000 or Problem.objects.filter(problem_id=int(problem)).count() == 0:
                    return JsonResponse({'status': False, 'err': str(problem).join('Problem ID id non-existent')})
            if userId == None:
                return JsonResponse({'status': False, 'err': 'You need to log in to add levels'})
            message = {}
            try:
                Level.objects.create(
                    title=title,
                    description=description,
                    level_pre=levelPre,
                    pass_num=passNum,
                    type=1,
                    num=num,
                    front_id=fonrtId,
                    creator=userId,
                    nick=userNick,
                    defunct='N'
                )
                message['leveladd'] = 'success'
            except:
                return JsonResponse({'status': False,
                                     'err': 'Failed to add data with table named level. You may be missing a parameter'})

            level_id = Level.objects.filter(front_id=fonrtId).values('level_id').order_by('level_id').first()
            level_id = level_id['level_id']
            i = 1;
            for problem in problems:
                LevelProblem.objects.create(
                    level_id=level_id,
                    problem_id=int(problem),
                    num=i
                )
                i += 1
            if i - 1 == len(problems):
                message['addproblem'] = 'success'
                message['status'] = True
            else:
                message['addproblem'] = 'some problem not add'
            return JsonResponse(message)
        # 关卡大类添加
        elif type == 2:
            num = Level.objects.filter(front_id=0).count() + 1;

            try:
                Level.objects.create(
                    title=title,
                    description=description,
                    level_pre=None,
                    pass_num=0,
                    type=2,
                    num=num,
                    front_id=0,
                    creator=userId,
                    nick=userNick,
                    defunct='N'
                )
                return JsonResponse({'status': True, 'err': 'success'})
            except:
                return JsonResponse({'status': False,
                                     'err': 'Failed to add data with table named level. You may be missing a parameter'})
        else:
            return JsonResponse({'status': False, 'err': 'Please input right type'})


class editLevel(View):

    def get(self, request):
        levelId = int(request.GET.get('level_id', -1))
        type = int(request.GET.get('type', -1))
        token = request.GET.get('token')

        if publicMethod.get_user_capacity(token) != 0:
            return JsonResponse({'status': False, 'err': 'You do not have permission to operate'})
        if not token:
            return JsonResponse({'status': False, 'err': 'You need to log in to edit levels'})
        if not levelId or levelId < 1:
            return JsonResponse({'status': False, 'err': 'Error to level ID'})

        if type == 1:
            thisLevel = Level.objects.filter(level_id=levelId, type=type)
            if thisLevel.count() == 0:
                return JsonResponse({'status': False, 'err': 'not have this level'})
            levelKind = Level.objects.only('level_id', 'title', 'num').filter(type=2).order_by('num')
            levels = Level.objects.only('level_id', 'title', 'num', 'front_id').filter(type=1).order_by('front_id',
                                                                                                        'num')
            data = []
            for kind in levelKind:
                k = []
                for level in levels:
                    if (kind.level_id == level.front_id):
                        k.append({
                            'id': level.level_id,
                            'title': level.title,
                            'num': level.num
                        })
                data.append({
                    'id': kind.level_id,
                    'title': kind.title,
                    'num': kind.num,
                    'levels': k
                })

            message = {'levels': data, 'thisLevel': thisLevel.values().first(), 'status': True}
            return JsonResponse(message)
        elif type == 2:
            message = {}
            thisLevel = Level.objects.only('level_id', 'title', 'description', 'num').filter(level_id=levelId,
                                                                                             type=type)
            if thisLevel.count() == 0:
                message = {'status': False, 'thisLevel': '', 'err': 'nothing found'}
            else:
                message = {'status': True, 'thisLevel': thisLevel.values().first()}
            return JsonResponse(message)
        else:
            return JsonResponse({'status': False, 'err': 'Error to type'})

    def post(self, request):
        levelId = int(request.POST.get('level_id', -1))
        type = int(request.POST.get('type', -1))
        token = request.POST.get('token')
        userNick = publicMethod.get_user_nick(token)
        userId = publicMethod.check_user_login(token)
        thisLevel = Level.objects.filter(level_id=levelId, type=type)
        if thisLevel.count() == 0:
            return JsonResponse({'status': False, 'err': 'not have this level'})
        if userId == None:
            return JsonResponse({'status': False, 'err': 'You need to log in to edit levels'})
        if not token:
            return JsonResponse({'status': False, 'err': 'You need to log in to edit levels'})
        if levelId < 1:
            return JsonResponse({'status': False, 'err': 'Error to level ID'})
        if type == 1:
            title = request.POST.get('title', None)
            description = request.POST.get('description', '')
            levelPre = request.POST.get('level_pre', None)
            fonrtId = int(request.POST.get('front_id'), 0)
            passNum = int(request.POST.get('pass_num'), 0)
            problems = str(request.POST.get('problems')).split(',')
            if title == None or title == '' or fonrtId == 0 or problems == None or problems == '':
                return JsonResponse({'status': False, 'err': 'Some parameters are missing'})

            # 判断问题格式是否正确
            for problem in problems:
                if not problem.isdigit():
                    return JsonResponse({'status': False, 'er': 'Problem ID field format error'})
                if int(problem) < 1000 or Problem.objects.filter(problem_id=int(problem)).count() == 0:
                    return JsonResponse({'status': False, 'err': str(problem) + '.Problem ID id non-existent'})
            LevelProblem.objects.filter(level_id=levelId).delete()
            i = 1;
            message = {}
            for problem in problems:
                LevelProblem.objects.create(
                    level_id=levelId,
                    problem_id=int(problem),
                    num=i
                )
                i += 1
            if i - 1 == len(problems):
                message['editproblem'] = 'success'
            Level.objects.filter(level_id=levelId).update(
                title=title,
                description=description,
                level_pre=levelPre,
                pass_num=passNum,
                type=1,
                front_id=fonrtId,
                creator=userId,
                nick=userNick,
                defunct='N'
            )
            message['err'] = 'success'
            message['status'] = True
            return JsonResponse(message, safe=False)
        elif type == 2:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            if userId == None:
                return JsonResponse({'status': False, 'err': 'You need to log in to edit levels'})
            if title == None or title == '':
                return JsonResponse({'status': False, 'err': 'Some parameters are missing'})
            try:
                Level.objects.filter(level_id=levelId).update(
                    title=title,
                    description=description,
                    creator=userId,
                    nick=userNick,
                )
                return JsonResponse({'status': True, 'err': 'success'})
            except:
                return JsonResponse({'status': False,
                                     'err': 'Failed to edit data with table named level. You may be missing a parameter'})
        else:
            return JsonResponse({'status': False, 'err': 'Error to type'})


class deleteLevel(View):

    def get(self, request):
        return JsonResponse({'status': True, 'err': 'return nothing'})

    def post(self, request):
        levelId = int(request.POST.get('level_id', -1))
        token = request.POST.get('token')
        userNick = publicMethod.get_user_nick(token)
        userId = publicMethod.check_user_login(token)
        thisLevel = Level.objects.filter(level_id=levelId)
        if thisLevel.count() == 0:
            return JsonResponse({'status': False, 'err': 'not have this level'})
        if levelId < 1:
            return JsonResponse({'status': False, 'err': 'Error to level ID'})
        if publicMethod.get_user_capacity(token) != 0:
            return JsonResponse({'status': False, 'err': 'You do not have permission to operate'})
        if userId == None:
            return JsonResponse({'status': False, 'err': 'You need to log in to delete levels'})
        if not token:
            return JsonResponse({'status': False, 'err': 'You need to log in to delete levels'})

        try:
            if (thisLevel.first().type == 1):
                thisLevel.update(isdelete=1)
            else:
                thisLevel.update(isdelete=1)
                Level.objects.filter(front_id=levelId).update(isdelete=1)
            return JsonResponse({'status': True, 'err': 'success'})
        except:
            return JsonResponse({'status': False, 'err': 'sql connection failed'})


class getLevelList(View):
    def get(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        levels_list = []
        big_levels = Level.objects.filter(type=2)
        for big_level in big_levels:
            level_pass = 0
            level_list = []
            levels = Level.objects.filter(front_id=big_level.level_id)
            for level in levels:
                problem_list = []
                problems = LevelProblem.objects.filter(level_id=level.level_id)
                for problem in problems:
                    question = Problem.objects.filter(problem_id=problem.problem_id).first()
                    if question:
                        problem_title = question.problem_title
                    else:
                        continue
                    problem_status = 0
                    if user_id:
                        solutions = Solution.objects.filter(problem_id=problem.problem_id, user_id=user_id).values('run_result')
                        if solutions.exists():
                            if 1 in solutions:
                                problem_status = 1
                            else:
                                problem_status = -1
                    problem_list.append({
                        'problem_id': problem.problem_id,
                        'level_id': problem.level_id,
                        'num': problem.num,
                        'problem_title': problem_title,
                        'problem_status': problem_status
                    })
                is_pass = False
                if user_id:
                    level_pass_list = LevelPass.objects.filter(user_id=user_id, level_id=level.level_id)
                    if level_pass_list.exists():
                        is_pass = True
                        level_pass = level_pass + 1
                level_list.append({
                    'level_id': level.level_id,
                    'title': level.title,
                    'description': level.description,
                    'level_pre': level.level_pre,
                    'pass_num': level.pass_num,
                    'type': level.type,
                    'num': level.num,
                    'front_id': level.front_id,
                    'creator': level.creator,
                    'nick': level.nick,
                    'status': level.defunct,
                    'level_pass': is_pass,
                    'problem_list': problem_list,
                })
            levels_list.append({
                'level_id': big_level.level_id,
                'title': big_level.title,
                'description': big_level.description,
                'level_pre': big_level.level_pre,
                'pass_num': big_level.pass_num,
                'type': big_level.type,
                'num': big_level.num,
                'front_id': big_level.front_id,
                'creator': big_level.creator,
                'nick': big_level.nick,
                'status': big_level.defunct,
                'level_list': level_list,
                'level_pass': level_pass,
            })
        return JsonResponse({'status': True, 'message': levels_list})

    def post(self, request):
        type = int(request.POST.get('type', -1))
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        keyword = request.POST.get('keyword', '')
        if publicMethod.get_user_capacity(token) != 0:
            return JsonResponse({'status': False, 'err': 'You do not have permission to operate'})
        if not token or token == '':
            return JsonResponse({'status': False, 'err': 'You need to log in'})
        if user_id == None:
            return JsonResponse({'status': False, 'err': 'The token is invalid'})
        # levelKind = Level.objects.values_list('level_id','title','description','num').filter(type=2,isdelete=0).order_by('front_id','num')
        levelKind = Level.objects.filter(type=2, isdelete=0).order_by('front_id', 'num')
        data = []
        if type == 1:
            Levels = Level.objects.filter(type=1, isdelete=0).filter(
                Q(title__contains=keyword) | Q(description__contains=keyword)).order_by('front_id', 'num')
            for level in Levels:
                temp = []
                for kind in levelKind:
                    if (kind.level_id == level.front_id):
                        prelist = []
                        if level.level_pre != None and level.level_pre != '':
                            pre = level.level_pre.split(',')
                            for p in pre:
                                prelist.append(
                                    p + "." + Level.objects.get(level_id=int(p)))
                        temp.append({
                            'level_id': level.level_id,
                            'title': level.title,
                            'description': level.description,
                            'num': level.num,
                            'level_pre': ','.join(prelist),
                            'front_id': level.front_id,
                            'kindTitle': kind.title,
                            'defunct': level.defunct
                        })
                        break
                data.append(temp)
            return JsonResponse({'status': True, 'err': 'Success', 'data': data})
        elif type == 2:
            for kind in levelKind:
                data.append({
                    'level_id': kind.level_id,
                    'title': kind.title,
                    'description': kind.description,
                    'num': kind.num,
                })
            return JsonResponse({'status': True, 'err': 'Success', 'data': data})
        else:
            return JsonResponse({'status': False, 'err': 'Type is error'})


# get方法可传可不穿，post方法传level_id，返回该题目的做题信息
class openClass(View):
    def get(self, request):
        token = request.GET.get('token')
        userId = publicMethod.check_user_login(token)
        # if not token or token=='':
        #     return JsonResponse({'status': False, 'err': 'You need to log in'})
        # if userId == None:
        #     return JsonResponse({'status': False, 'err': 'The token is invalid'})
        levelKind = Level.objects.only('level_id', 'title', 'description', 'num').filter(type=2, isdelete=0).order_by(
            'num')
        levels = Level.objects.only('level_id', 'title', 'description', 'level_pre', 'num', 'front_id').filter(type=1,
                                                                                                               isdelete=0).order_by(
            'front_id', 'num')
        data = []
        for kind in levelKind:
            k = []
            for level in levels:
                if (kind.level_id == level.front_id):
                    prelist = []
                    isPass = True
                    problemNum = LevelProblem.objects.filter(level_id=level.level_id).count()
                    submitNum = LevelProblemSubmit.objects.filter(level_id=level.level_id).count()
                    passNum = LevelProblemSubmit.objects.filter(level_id=level.level_id, status=1).count()
                    if LevelPass.objects.filter(level_id=level.level_id, user_id=userId).count() == 0:
                        isPass = False
                    if level.level_pre != None and level.level_pre != '':
                        pre = level.level_pre.split(',')
                        for p in pre:
                            if LevelPass.objects.filter(level_id=int(p), user_id=userId).count() == 0:
                                prelist.append(
                                    p + "." + Level.objects.get(level_id=int(p)))
                    k.append({
                        'id': level.level_id,
                        'title': level.title,
                        'description': level.description,
                        'num': level.num,
                        'level_pre': ','.join(prelist),
                        'isPass': isPass,
                        'problemNum': problemNum,
                        'submitNum': submitNum,
                        'passNum': passNum
                    })
            data.append({
                'id': kind.level_id,
                'title': kind.title,
                'description': kind.description,
                'num': kind.num,
                'levels': k
            })
        message = {'status': True, 'levels': data}
        return JsonResponse(message, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        userId = publicMethod.check_user_login(token)
        levelId = int(request.POST.get('level_id', -1))
        if (levelId < 1):
            return JsonResponse({'status': False, 'err': 'LevelId is wrong!'})
        if not token or token == '':
            return JsonResponse({'status': False, 'err': 'You need to log in'})
        if userId == None:
            return JsonResponse({'status': False, 'err': 'The token is invalid'})

        problems = LevelProblem.objects.values_list('problem_id', flat=True).filter(level_id=levelId)
        problemsSubmits = LevelProblemSubmit.objects.filter(level_id=levelId, user_id=userId)
        data = []
        for problem in problems:
            k = 1
            for ps in problemsSubmits:
                if ps.level_id == levelId and problem.problem_id == ps.problem_id:
                    p = Problem.objects.filter(problem_id=ps.problem_id)
                    for t in p:
                        data.append({
                            'problemTitle': t,
                            'problemId': ps.problem_id,
                            'status': '通过' if ps.status == 1 else ('错误' if ps.status == 2 else '--')
                        })
                    k = 0;
                    break;
            if k == 1:
                p = Problem.objects.filter(problem_id=int(problem))
                for t in p:
                    data.append({
                        'problemTitle': t.problem_title,
                        'problemId': int(problem),
                        'status': '--'
                    })
        return JsonResponse({'status': False, 'err': data})


class levelCompletion(View):
    def get(self, request):
        token = request.GET.get('token')
        if not publicMethod.parse_payload(token)['status']:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error']})

        allClass = Class.objects.only('class_id', 'class_name').filter(class_type=0).order_by('class_name')
        levelKind = Level.objects.only('level_id', 'title').filter(type=2, isdelete=0).order_by('num')
        data = []
        temp = []
        for c in allClass:
            temp.append({
                'class_id': c.class_id,
                'class_name': c.class_name
            })
        data.append(temp)
        temp = []
        for l in levelKind:
            temp.append({
                'level_id': l.level_id,
                'title': l.title
            })
        data.append(temp)
        return JsonResponse({'status': True, 'data': data, 'err': 'success'})

    def post(self, request):
        classId = int(request.POST.get('class_id', -1))
        levelKind = int(request.POST.get('level_id', -1))
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error']})
        if classId < 1 or levelKind < 1:
            return JsonResponse({'status': False, 'err': 'Wrong parameter transfer'})

        levels = Level.objects.only('level_id', 'title').filter(isdelete=0, front_id=levelKind, type=1).order_by('num')
        with connection.cursor() as cursor:
            cursor.execute(
                "select DISTINCT(`class_user`.user_id),`user`.user_name,`user`.user_nick from `class_user` LEFT JOIN `user` ON `class_user`.user_id=`user`.user_id WHERE `class_user`.class_id = %s",
                [classId])
            classUsers = cursor.fetchall()
        classUsers = list(classUsers)
        #print(classUsers)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT(level_id),user_id FROM level_pass where level_id in (select level_id from `level` WHERE front_id = %s and isdelete=0) and user_id in (SELECT user_id from class_user where class_id = %s and user_type=0) ORDER BY user_id",
                [levelKind, classId])
            passUsers = cursor.fetchall()
        passUsers = list(passUsers)
        data = []
        for classUser in classUsers:
            temp = {}
            temp['user_id'] = classUser[0]
            temp['user_name'] = classUser[1]
            temp['user_nick'] = classUser[2]
            for level in levels:
                temp[level.level_id] = '未通过'
                for passUser in passUsers:
                    if level.level_id == passUser[0] and classUser[0] == passUser[1]:
                        temp[level.level_id] = '通过'
                        break

        return JsonResponse({'status': True, 'err': 'success', 'data': data})


