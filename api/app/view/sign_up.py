import json

import simplejson as simplejson
from django.http import JsonResponse
from app.models import *
from django.utils import timezone
from app.RoleMethod.PublicMethod import PublicMethod
from django.views import View
from django.core.cache import cache



# Create your views here.
"""
如何实现图文混排

前端使用标记，后端按照标记定位图片位置

显示已报名该比赛

生成比赛账号

修改团队信息以及删除的测试

查询
"""


# ----------------------------------报名系统 谢继业--------------------------------------- #

class signUpPage(View):
    """
        模块：报名入口
        接口信息：
            get:
            post:

        返回信息：

    """
    def get(self, request):
        contestID = request.GET.get("contest_id")
        info = []
        try:
            contestInfo = models.Contest.objects.get(contest_id=contestID)
            info.append({
                "contest_id": contestInfo.contest_id,
                "contest_title": contestInfo.contest_title,
                "contest_info": contestInfo.contest_introduce,
                "contest_language": contestInfo.contest_language,
                "contest_time": contestInfo.start_time
            })
        except:
            return JsonResponse({"msg": "竞赛id不存在"})
        return JsonResponse({"info":info})

    def post(self, request):
        contest = request.POST.get("contest")
        information = request.POST.get("contestInfo")


class singleCancel(View):
    """
    取消个人报名
    """
    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get("token")
        contestId = request.POST.get("contestId")
        user = PublicMethod().parse_payload(token)
        models.ContestUser.objects.all().filter(
            contest_id=contestId,
            contest_user=user["data"]["data"]["user_id"]
        ).delete()


"""
# 个人报名
    # 两种实现方式 form表单 一键登录
    # 个人报名，点击按钮，自动报名，
    # 所需的数据： 用户id 竞赛id 报名时间 判断是否为机器人
    # 数据验证： 查看该用户是否已经出现在报名之中
    # 功能前提 是否登录，未登录显示请先登录
    # 报名之后显示在审核中，成功后显示在比赛中
    # 竞赛时间冲突?
"""
class SingleSignUp(View):
    """
    模块: 个人报名
    接口信息:
        GET:
            None
        POST:
            获取token进行报名
            token：token
            contest_id：比赛id
    返回信息:
        {
            msg：提示信息
        }
    """
    def post(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        contest_id = request.POST.get("contest_id")
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        contest = Contest.objects.filter(contest_id=contest_id).first()
        users = ContestUser.objects.filter(contest_id=contest_id).values_list('contest_user')
        if user_id in users:
            return JsonResponse({'status': False, 'message': '已报名'})
        if contest.contest_province == 3:
            contest_auditing = 0
        else:
            contest_auditing = 1
        ContestUser.objects.create(
            contest_id=contest_id,
            contest_user=user_id,
            contest_auditing=contest_auditing,
            apply_time=timezone.now()
        )
        return JsonResponse({'status': True, 'message': '添加成功'})


"""
# 团队报名
    # 实现方式
    # 团队报名，询问是否新建队伍，或者使用现有的团队

    # 进入创建队伍页面，
    # 创建完成后，进入团队报名页面

    # 使用现有的团队
    # 用户查询自己的团队，选择团队报名
    # 查询用户所属的所有的团队名称,并返回
    # 所需数据：团队id 竞赛id 报名时间 判断是否为机器人
    # 数据验证: 查看团队中的用户是否已经出现在该报名中
    # 报名之后显示再审核中，成功之后，给该队伍发放账号密码
    # 比赛中的队员是否有比赛时间上的冲突
"""

# 团队报名
class TeamSignUp(View):
    """
        模块: 团队报名
        接口信息:
            GET:
                获取个人拥有的团队
                token: token
            POST:
                团队报名
                token：token
                teamName: 队伍名称
                teacher: 指导老师
                teamMember01：队伍成员1
                teamMember02: 队伍成员2
        返回信息:
            {
                get:
                    msg：个人的团队信息
                post:
                    msg: 报名成功提示信息
            }
        """

    def get(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        team_list = []
        teams = ClassUser.objects.filter(user_id=user_id).values_list('class_id')
        for team in teams:
            the_team = Class.objects.filter(class_id=team).first()
            if the_team.class_type != 1 and the_team.class_type != 4:
                continue
            team_list.append({
                'class_id': the_team.class_id,
                'class_type': the_team.class_type,
                'class_name': the_team.class_name
            })
        return JsonResponse({'status': True, 'message': team_list})

    def post(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        class_id = request.POST.get('class_id')
        contest_id = request.POST.get('contest_id')
        team = Class.objects.filter(class_id=class_id)
        if team.exists():
            return JsonResponse({'status': False, 'message': '没有这个团队'})
        contest = Contest.objects.filter(contest_id=contest_id).first()
        if not contest:
            return JsonResponse({'status': False, 'message': '没有这个竞赛'})
        if contest.contest_province == 3:
            contest_auditing = 0
        else:
            contest_auditing = 1
        users = ClassUser.objects.filter(class_id=class_id)
        for user in users:
            the_user = ContestUser.objects.filter(contest_id=contest_id, user_id=user.user_id).first()
            if the_user:
                the_user.contest_class = class_id
                the_user.save()
                continue
            ContestUser.objects.create(
                contest_id=contest_id,
                contest_user=user.user_id,
                contest_class=class_id,
                contest_auditing=contest_auditing,
            )
        return JsonResponse({'status': True, 'message': '报名成功'})


class teamCancel(View):
    """
        接口名称： 取消团队报名

    """

    def get(self, request):
        pass

    def post(self, request):
        pass

"""
# 报名的后台管理
    # 进入后台报名审核
    # 显示报名记录，按时间排序，使用分页器
    # 显示字段 报名id 比赛id 报名用户 报名时间 审核是否通过 在该场比赛获得的荣誉
    # 如果不通过 删除该记录 不启用数据保护
    # 审核通过
"""
# 个人报名后台管理
class singleSignUpManage(View):
    """
            模块: 个人报名的后台管理
            接口信息:
                GET:
                    查看所有的个人报名信息
                POST:
                    个人报名查询
                    token：token
            返回信息:
                {
                    get:
                        msg：个人的团队信息
                    post:
                        msg: 报名成功提示信息
                }
    """
    def __str__(self):
        pass

    def get(self, request):
        signUpInfo = []
        contestUsers = models.ContestUser.objects.all()
        total = 0
        for contestUser in contestUsers:
            if contestUser.contest_user and (not contestUser.contest_class):
                try:
                    userInfo = models.User.objects.get(user_id=contestUser.contest_user)
                    signUpInfo.append(
                        {
                            "contestId": contestUser.contest_id,
                            "name": userInfo.user_name,
                            "school": userInfo.user_school,
                            "class": userInfo.user_class,
                            "userId": contestUser.contest_user,
                            "grades": contestUser.contest_grades,
                            "auditing": contestUser.contest_auditing
                        }
                    )
                    total = total + 1
                except:
                    print(contestUser.contest_user)
        return JsonResponse({'contest': signUpInfo, 'total': total}, safe=False)

    def post(self, request):                # 查询操作
        contestName=request.POST.get("contest_name")
        singleName=request.POST.get("single_name")
        info = []
        if contestName and singleName:
            pass
        elif contestName:
            pass
        elif singleName:
            pass

# 生成比赛账号
class accountGenerator(View):
    """
        模块: 个人报名的后台管理
            接口信息:
                GET:
                    查看所有的个人报名信息
                POST:
                    个人报名查询
                    token：token
            返回信息:
                {
                    get:
                        msg：个人的团队信息
                    post:
                        msg: 报名成功提示信息
                }
    """
    def get(self, request):
        pass

    def post(self, request):
        info = json.loads(request.body)
        print(info)
        user = PublicMethod().parse_payload(info.get("token"))
        teams = info.get("teams")
        try:
            if user["status"] and teams:
                for team in teams:
                    obj = models.ContestUser.objects.all().filter(contest_id=team.id)
                    obj.contest_account = "team"+team.id
                    obj.save()
            else:
                return JsonResponse({"msg": "false"})
        except:
            return JsonResponse({"msg": "false"})
        return JsonResponse({"msg": "true"})


# 团队报名后台管理
class teamSignUpManage(View):
    """
                模块: 团队报名的后台管理
                接口信息:
                    GET:
                        查看所有的团队报名信息
                    POST:
                        团队报名查询
                        token：token
                返回信息:
                    {
                        get:
                            msg：所有的团队信息
                        post：

                    }
    """

    def get(self, request):
        signInfo = []
        contestUsers = models.ContestUser.objects.all()
        # total = 0
        for contestUser in contestUsers:
            memberInfo = []
            if contestUser.contest_class and (not contestUser.contest_user):  # 团队报名只有团队编号，也就是class_id，没有具体用户
                # total = total+1
                try:  # 如果数据库没有团队数据，此时取数据，抛出异常，团队与班级共用一张数据库
                    # print(contestUser.contest_class)
                    teamInfo = models.Class.objects.filter(class_id=contestUser.contest_class).first()
                    # print(teamInfo)
                    teamMembers = models.ClassUser.objects.all().filter(class_id=contestUser.contest_class)
                    for member in teamMembers:
                        info = models.User.objects.get(user_id=member.user_id)
                        school = models.School.objects.get(school_id=info.user_school)
                        memberInfo.append({
                                "memberInfo": info.user_id,
                                "memberName": info.user_name,
                                "memberClass": info.user_class,
                                "memberSchool": school.school_name,
                        })

                    # print(memberInfo)
                    signInfo.append({
                                "contestId": contestUser.contest_id,
                                "teamName": teamInfo.class_name,
                                "teamMember": memberInfo,
                                "grades": contestUser.contest_grades,
                                "auditing": contestUser.contest_auditing,
                                "teamAccount": contestUser.contest_account
                        })
                except:
                    print(contestUser.contest_class)
        return JsonResponse({'status': True, "message": signInfo})

    def post(self, request):                        # 团队报名查询
        contestName = request.POST.get("contest_name")
        teamName = request.POST.get("single_name")
        info = []
        if contestName and teamName:
            pass
        elif contestName:
            pass
        elif teamName:
            pass

class teamSignUpModify(View):       # 修改团队报名信息
    def __str__(self):
        pass

    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get('token')
        user = PublicMethod().parse_payload(token)
        if user["status"]:
            teamId = request.POST.get("team_id")
            teamName = request.POST.get("teamName")
            teamMembers = {}
            teamMembers[0] = request.POST.get("teamer01")
            teamMembers[1] = request.POST.get("teamer02")
            teamMembers[2] = request.POST.get("teamer03")
            if models.User.objects.all().filter(user_id=teamMembers[0]).exists() \
                    and models.User.objects.all().filter(user_id=teamMembers[1]).exists() \
                    and models.User.objects.all().filter(user_id=teamMembers[2]).exists():
                print(teamName)
                print(teamId)
                team = models.Class.objects.all().filter(class_id=teamId)
                print(team)
                if team:
                    try:
                        memebers = models.ClassUser.objects.all().fliter(class_id=team.class_id)
                        for member,teamMember in memebers,teamMembers:
                            member.user_id = teamMember
                            member.save()
                        return JsonResponse({"msg": "true"})
                    except:
                        if models.Class.objects.all().filter(class_name=teamName).exists():
                            models.Class.objects.all().filter(class_name=teamName).delete()
                        print("something wrong")
                else:
                    return JsonResponse({'msg': 'team_not_existed'})
            else:
                return JsonResponse({"msg": "wrong_team_member"})
        else:
            return JsonResponse({"msg": "请先登录"})

# 无效报名删除
class invalidSignUp(View):
    def __str__(self):
        pass

    def get(self, request):
        pass

    def post(self, request):
        token = request.POST.get("token")
        user = PublicMethod().parse_payload(token)
        if user["status"]:
            user = request.POST.get("userId")
            team = request.POST.get("teamId")
            contest = request.POST.get("contestId")
            teamUsers = models.ClassUser.objects.filter(class_id=team)
            if user and contest:
                models.ContestUser.objects.filter(contest_id=contest, user_id=user).delete()
            elif team and contest and teamUsers:
                models.Class.objects.filter(class_id=team).delete()
                for teamUser in teamUsers:
                    teamUser.delete()
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': "请先登录"}, safe=False)