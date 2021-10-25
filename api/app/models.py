from django.db import models
import uuid


# ---------------------------地址管理------------------------------
class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=25, verbose_name='省份')

    class Meta:
        verbose_name = '省份管理'
        managed = True
        db_table = 'province'


class Municipality(models.Model):
    municipality_id = models.AutoField(primary_key=True)
    municipality_name = models.CharField(max_length=50, verbose_name='市级城市')
    municipality_province = models.IntegerField(null=True, blank=True, verbose_name='城市所在省份')

    class Meta:
        verbose_name = '城市管理'
        managed = True
        db_table = 'municipality'


# -------------------------------学校管理--------------------------
class School(models.Model):
    school_id = models.CharField(max_length=20, primary_key=True)
    school_name = models.CharField(max_length=50, verbose_name='学校名称')
    school_describe = models.TextField(null=True, blank=True, verbose_name='学校描述')
    school_department = models.CharField(max_length=20, null=True, blank=True, verbose_name='主管部门')
    school_municipality = models.IntegerField(null=True, blank=True, verbose_name='学校所在城市')
    school_rank = models.CharField(max_length=20, blank=True, null=True, verbose_name='办学层次')
    school_remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='学校备注')

    class Meta:
        verbose_name = '学校管理'
        managed = True
        db_table = 'school'


class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50, verbose_name='学院名称')
    college_school = models.CharField(max_length=20, null=True, blank=True, verbose_name='学院所在学校')

    class Meta:
        verbose_name = '学院管理'
        managed = True
        db_table = 'college'


# ---------------------------班级管理------------------------------
class Class(models.Model):
    CLASS_TYPE = [
        (0, '行政班级'),
        (1, '团队类型'),
        (2, '课程班级'),
        (3, '默认班级'),
        (4, '临时团队')
    ]

    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, verbose_name='班级名称')
    class_creator = models.CharField(max_length=48, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    class_introduce = models.CharField(max_length=256, null=True, blank=True, verbose_name='班级介绍')
    class_type = models.SmallIntegerField(null=True, blank=True, choices=CLASS_TYPE, verbose_name='班级类型')
    class_college = models.CharField(max_length=20, null=True, blank=True, verbose_name='班级所在学院')
    class_invitation = models.CharField(max_length=10, null=True, blank=True, verbose_name='班级邀请码')

    class Meta:
        verbose_name = '班级管理'
        managed = True
        db_table = 'class'


class ClassUser(models.Model):
    USER_TYPE = [
        (0, '学生'),
        (1, '教师'),
        (2, '助教')
    ]

    ADD_TYPE = [
        (0, '邀请码加入'),
        (1, '付费加入'),
        (2, '教师邀请')
    ]
    class_id = models.IntegerField(verbose_name='班级序号')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    user_type = models.IntegerField(default='0', verbose_name='用户类型')
    add_time = models.DateTimeField(auto_now=True, verbose_name='加入时间')
    add_type = models.SmallIntegerField(null=True, blank=True, choices=ADD_TYPE, verbose_name='加入方式')
    user_remark = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户备注')
    user_status = models.BooleanField(default='1', verbose_name='用户状态')

    class Meta:
        verbose_name = '班级用户'
        managed = True
        db_table = 'class_user'


# ---------------------------用户管理------------------------------
class Password(models.Model):
    user_id = models.CharField(max_length=48, primary_key=True, verbose_name='用户账号')
    password = models.CharField(max_length=48, verbose_name='用户密码')
    registration_time = models.DateTimeField(auto_now=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '密码管理'
        managed = True
        db_table = 'password'


# 用户头像文件重命名
def user_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'user_file/{instance.user_id}/user_icon/{filename}'


class User(models.Model):
    SEX_CHOICE = [
        (0, '男'),
        (1, '女'),
    ]

    POWER_CHOICE = [
        (0, '超级管理员'),
        (1, '管理员'),
        (2, '教师'),
        (3, '志愿者'),
        (4, '用户'),
    ]

    user_id = models.CharField(max_length=48, primary_key=True, verbose_name='用户账号')
    user_icon = models.TextField(null=True, blank=True, verbose_name='用户头像')
    student_id = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户学号')
    user_name = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户姓名')
    user_nick = models.CharField(max_length=24, blank=True, null=True, verbose_name='用户昵称')
    user_introduce = models.CharField(max_length=250, blank=True, null=True, verbose_name='用户介绍')
    user_power = models.SmallIntegerField(choices=POWER_CHOICE, default=4, verbose_name='用户身份')
    user_score = models.IntegerField(default=0, verbose_name='用户得分')
    user_sex = models.SmallIntegerField(choices=SEX_CHOICE, verbose_name='用户性别')
    user_telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户电话')
    user_email = models.EmailField(blank=True, null=True, verbose_name='用户邮箱')
    user_birthday = models.DateTimeField(null=True, blank=True, verbose_name='用户生日')
    user_school = models.CharField(max_length=20, null=True, blank=True, verbose_name='用户所在学校')
    user_class = models.IntegerField(null=True, blank=True, verbose_name='用户所在班级')
    user_team = models.IntegerField(null=True, blank=True, verbose_name='用户所在团队')
    user_address = models.IntegerField(null=True, blank=True, verbose_name='用户所在地址')
    user_status = models.BooleanField(default='1', verbose_name='用户状态')

    class Meta:
        verbose_name = '用户管理'
        managed = True
        db_table = 'user'


class LoginLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=48, verbose_name='登陆日志')
    login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='用户IP')
    login_time = models.DateTimeField(auto_now=True, verbose_name='登陆时间')
    login_way = models.CharField(max_length=256, blank=True, null=True, verbose_name='登录方法')

    class Meta:
        verbose_name = '登录日志'
        managed = True
        db_table = 'login_log'


class LimitLogin(models.Model):
    LIMIT_TYPE = [
        (0, '黑名单模式'),
        (1, '白名单模式')
    ]

    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    limit_type = models.SmallIntegerField(default='0', choices=LIMIT_TYPE, verbose_name='限制类型')
    limit_time = models.IntegerField(default='0', verbose_name='限制时长')

    class Meta:
        verbose_name = '登录限制'
        managed = True
        db_table = 'limit_login'


class Collection(models.Model):
    TYPE_CHOICES = [
        (0, '问题'),
        (1, '竞赛'),
        (2, '帖子'),
        (3, '课程')
    ]

    collection_id = models.AutoField(primary_key=True)
    collection_user = models.CharField(max_length=48, verbose_name='用户编号')
    collection_type = models.SmallIntegerField(default='0', choices=TYPE_CHOICES, verbose_name='收藏类型')
    collection_forget_key = models.IntegerField(verbose_name='收藏内容的编号')
    collection_time = models.DateTimeField(auto_now=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        managed = True
        db_table = 'collection'


# ---------------------------题目管理------------------------------
class Problem(models.Model):
    problem_id = models.IntegerField(primary_key=True, verbose_name='题目编号')
    problem_title = models.CharField(max_length=200, verbose_name='题目标题')
    problem_description = models.TextField(verbose_name='题目描述')
    problem_spj = models.BooleanField(default='0', verbose_name='是否特判')
    problem_course = models.CharField(max_length=256, blank=True, null=True, verbose_name='题目来源')
    creation_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    time_limit = models.IntegerField(default='1000', verbose_name='时间限制')
    memory_limit = models.IntegerField(default='128', verbose_name='空间限制')
    problem_tag = models.CharField(max_length=256, blank=True, null=True, verbose_name='题目标签')
    problem_difficult = models.SmallIntegerField(default='0', verbose_name='题目难度')
    problem_creator = models.CharField(max_length=48, null=True, blank=True, verbose_name='题目创建者')
    problem_status = models.BooleanField(default='1', verbose_name='题目状态')

    class Meta:
        verbose_name = '问题管理'
        managed = True
        db_table = 'problem'


class ProblemFile(models.Model):
    problem_id = models.IntegerField(verbose_name='问题编号')
    problem_file = models.ImageField(verbose_name='问题图片')

    class Meta:
        verbose_name = '问题文件'
        managed = True
        db_table = 'problem_file'


# ---------------------------提交管理------------------------------
class Solution(models.Model):
    solution_id = models.AutoField(primary_key=True)
    problem_id = models.IntegerField(verbose_name='问题编号')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    contest_id = models.IntegerField(null=True, blank=True, verbose_name='竞赛编号')
    solution_code = models.TextField(null=True, blank=True, verbose_name='提交代码')
    solution_language = models.SmallIntegerField(default='0', verbose_name='提交语言')
    solution_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')
    solution_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='提交地址')
    code_length = models.IntegerField(default='0', verbose_name='代码长度')
    run_time = models.IntegerField(blank=True, null=True, verbose_name='运行时间')
    run_memory = models.IntegerField(blank=True, null=True, verbose_name='运行空间')
    run_result = models.SmallIntegerField(default='0', verbose_name='运行结果')
    run_error = models.TextField(null=True, blank=True, verbose_name='错误信息')
    run_pass_rate = models.IntegerField(default='0', verbose_name='通过的测试数')
    run_all_rate = models.IntegerField(default='1', verbose_name='所有的测试数')

    class Meta:
        verbose_name = '提交信息'
        managed = True
        db_table = 'solution'


class Sim(models.Model):
    solution_id = models.IntegerField(blank=True, null=True, verbose_name='提交编号')
    sim_solution_id = models.IntegerField(blank=True, null=True, verbose_name='重复的提交编号')
    sim_ratio = models.IntegerField(blank=True, null=True, verbose_name='重复率')

    class Meta:
        verbose_name = '提交判重'
        managed = True
        db_table = 'sim'


# ---------------------------竞赛管理------------------------------
class Contest(models.Model):
    PROVINCE_CHOICE = [
        (0, '公开'),
        (1, '私有'),
        (2, '作业'),
        (3, '竞赛')
    ]

    contest_id = models.AutoField(primary_key=True)
    contest_title = models.CharField(max_length=256, blank=True, null=True, verbose_name='竞赛标题')
    contest_introduce = models.TextField(null=True, blank=True, verbose_name='竞赛描述')
    contest_province = models.SmallIntegerField(default='0', choices=PROVINCE_CHOICE, verbose_name='竞赛类型')
    contest_password = models.CharField(max_length=50, default='0000', verbose_name='竞赛密码')
    contest_language = models.CharField(max_length=200, null=True, blank=True, verbose_name='竞赛语言')
    contest_creator = models.CharField(max_length=48, null=True, blank=True, verbose_name='创建者')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    contest_defunct = models.BooleanField(default='1', verbose_name='是否隐藏')

    class Meta:
        verbose_name = '竞赛管理'
        managed = True
        db_table = 'contest'


class ContestProblem(models.Model):
    contest_id = models.IntegerField(verbose_name='竞赛编号')
    problem_id = models.IntegerField(verbose_name='问题编号')
    problem_title = models.CharField(max_length=256, null=True, blank=True, verbose_name='问题标题')
    problem_num = models.IntegerField(verbose_name='当前竞赛题目序号')

    class Meta:
        verbose_name = '竞赛问题'
        managed = True
        db_table = 'contest_problem'


class ContestUser(models.Model):
    contest_id = models.IntegerField(verbose_name='竞赛编号')
    contest_user = models.CharField(max_length=48, null=True, blank=True, verbose_name='竞赛用户')
    contest_class = models.IntegerField(null=True, blank=True, verbose_name='竞赛团队')
    contest_account = models.CharField(max_length=48, blank=True, null=True, verbose_name='比赛账号生成')
    contest_grades = models.CharField(max_length=48, null=True, blank=True, verbose_name='获奖等级')
    contest_auditing = models.BooleanField(default='0', verbose_name='审核状态')
    apply_time = models.DateTimeField(null=True, blank=True, verbose_name='申请设计')

    class Meta:
        verbose_name = '竞赛用户'
        managed = True
        db_table = 'contest_user'


class ContestRank(models.Model):
    contest_id = models.IntegerField(verbose_name='竞赛编号')
    contest_user = models.CharField(max_length=48, verbose_name='竞赛用户')
    contest_sum = models.IntegerField(default='0', verbose_name='过题数量')
    contest_time = models.TextField(null=True, blank=True, verbose_name='总时间')
    contest_put = models.TextField(null=True, blank=True, verbose_name='题目提交数量')
    contest_score = models.TextField(null=True, blank=True, verbose_name='竞赛成绩')

    class Meta:
        verbose_name = '竞赛排名'
        managed = True
        db_table = 'contest_rank'


# ---------------------------论坛管理------------------------------
class Forum(models.Model):
    STATUS_CHOICE = [
        (0, '审核中'),
        (1, '通过'),
        (2, '未通过'),
        (3, '已删除')
    ]

    SECTION_CHOICE = [
        (0, '公共'),
        (1, '问题'),
        (2, '竞赛'),
        (3, '课程'),
        (4, '班级')
    ]

    forum_id = models.AutoField(primary_key=True)
    forum_title = models.CharField(max_length=255, verbose_name='论坛标题')
    forum_content = models.TextField(verbose_name='论坛内容')
    forum_creator = models.CharField(max_length=48, verbose_name='论坛创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='论坛创建时间')
    forum_status = models.SmallIntegerField(default='0', choices=STATUS_CHOICE, verbose_name='论坛状态')
    forum_section = models.SmallIntegerField(default='0', choices=SECTION_CHOICE, verbose_name='论坛版块')
    section_id = models.IntegerField(null=True, blank=True, verbose_name='版块编号')
    forum_priority = models.IntegerField(null=True, blank=True, verbose_name='优先级')
    forum_visits = models.IntegerField(null=True, blank=True, verbose_name='浏览量')

    class Meta:
        verbose_name = '论坛管理'
        managed = True
        db_table = 'forum'


class ForumUser(models.Model):
    forum_id = models.IntegerField(verbose_name='论坛编号')
    forum_user = models.CharField(max_length=48, verbose_name='点赞用户')
    is_like = models.BooleanField(default='0', verbose_name='是否点赞')
    # is_collect = models.BooleanField(default='0', verbose_name='是否收藏')

    class Meta:
        verbose_name = '论坛点赞'
        managed = True
        db_table = 'forum_user'


class Reply(models.Model):
    STATUS_CHOICE = [
        (0, '通过'),
        (1, '未通过'),
        (2, '隐藏')
    ]

    reply_id = models.AutoField(primary_key=True)
    forum_id = models.IntegerField(verbose_name='论坛编号')
    reply_content = models.TextField(verbose_name='回复内容')
    reply_creator = models.CharField(max_length=48, verbose_name='回复创建者')
    pre_reply = models.IntegerField(default='-1', verbose_name='前置回复')
    create_time = models.DateTimeField(auto_now=True, verbose_name='回复创建时间')
    reply_status = models.SmallIntegerField(default='0', choices=STATUS_CHOICE, verbose_name='回复状态')
    reply_priority = models.IntegerField(null=True, blank=True, verbose_name='优先级')

    class Meta:
        verbose_name = '用户回复'
        managed = True
        db_table = 'reply'


class ReplyUser(models.Model):
    reply_id = models.IntegerField(verbose_name='回复编号')
    reply_user = models.CharField(max_length=48, verbose_name='点赞用户')
    is_like = models.BooleanField(default='0', verbose_name='是否点赞')
    # is_collect = models.BooleanField(default='0', verbose_name='是否收藏')

    class Meta:
        verbose_name = '回复点赞'
        managed = True
        db_table = 'reply_user'


# ---------------------------关卡管理------------------------------
class Level(models.Model):
    LEVEL_TYPE = [
        (1, '关卡'),
        (2, '关卡大类')
    ]

    level_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='关卡标题')
    description = models.TextField(null=True, blank=True, verbose_name='关卡描述')
    level_pre = models.CharField(max_length=50, null=True, blank=True, verbose_name='前置关卡')
    pass_num = models.IntegerField(null=True, blank=True, verbose_name='通过题数')
    type = models.SmallIntegerField(choices=LEVEL_TYPE, verbose_name='类型')
    num = models.IntegerField(default='0', verbose_name='编号')
    front_id = models.IntegerField(default='0', verbose_name='属于那个大类')
    creator = models.CharField(max_length=48, null=True, blank=True, verbose_name='创建者编号')
    nick = models.CharField(max_length=48, null=True, blank=True, verbose_name='昵称')
    defunct = models.CharField(max_length=4, blank=True, null=False, verbose_name='是否不使用 N否，Y是')
    isdelete = models.BooleanField(default=0, verbose_name='是否删除')
    # level_kind = models.IntegerField(verbose_name='关卡类型编号')

    class Meta:
        verbose_name = '关卡管理'
        managed = True
        db_table = 'level'


class LevelPass(models.Model):
    level_id = models.IntegerField(null=True, blank=True, verbose_name='关卡编号')
    user_id = models.CharField(max_length=48, verbose_name='用户编号')
    pass_time = models.DateTimeField(auto_now_add=True, verbose_name='过关时间')

    class Meta:
        verbose_name = '过关用户'
        managed = True
        db_table = 'level_pass'


class LevelProblem(models.Model):
    problem_id = models.IntegerField(default='0', verbose_name='问题编号')
    level_id = models.IntegerField(blank=True, null=True, verbose_name='关卡编号')
    num = models.IntegerField(verbose_name='当前问题编号')

    class Meta:
        verbose_name = '关卡问题'
        managed = True
        db_table = 'level_problem'


class LevelProblemSubmit(models.Model):
    level_id = models.IntegerField(blank=False, null=False, verbose_name='关卡ID')
    problem_id = models.IntegerField(verbose_name='问题编号')
    user_id = models.CharField(max_length=32, verbose_name='用户ID')
    submit_time = models.DateTimeField(auto_now_add=True, blank=True, null=False, verbose_name='提交')
    status = models.IntegerField(blank=True, null=False, default=1, verbose_name='类型 1通关 2错误')
    solution_id = models.IntegerField(verbose_name='提交id')

    class Meta:
        verbose_name = '关卡问题提交'
        managed = True
        db_table = 'level_problem_submit'


class Scratch(models.Model):
    authorid = models.CharField(max_length=32, verbose_name='作者ID')
    teacherid = models.CharField(max_length=32, null=True, blank=True, verbose_name='课堂作业时所在的班级老师')
    state = models.SmallIntegerField(default=0, verbose_name='项目状态：未发布0、已发布1、开源2')
    recommented = models.SmallIntegerField(default=0, verbose_name='是否被推荐：0未被推荐，1已被推荐')
    view_count = models.IntegerField(default=0, verbose_name='被浏览次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数')
    favo_count = models.IntegerField(default=0, verbose_name='被收藏次数')
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='时间')
    title = models.CharField(max_length=32, default='Scratch新项目', verbose_name='标题')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')
    src = models.TextField(null=True, blank=True, verbose_name='源代码')

    class Meta:
        verbose_name = 'Scratch'
        managed = True
        db_table = 'scratch'


class ScratchFavo(models.Model):
    userid = models.CharField(max_length=32, verbose_name='用户ID')
    projectid = models.IntegerField(verbose_name='项目ID')
    time = models.DateTimeField(null=True, blank=True, verbose_name='时间')

    class Meta:
        verbose_name = 'ScratchFavo'
        managed = True
        db_table = 'scratch_favo'


class ScratchLike(models.Model):
    userid = models.CharField(max_length=32, verbose_name='用户ID')
    projectid = models.IntegerField(verbose_name='项目ID')
    time = models.DateTimeField(null=True, blank=True, verbose_name='时间')

    class Meta:
        verbose_name = 'ScratchLike'
        managed = True
        db_table = 'scratch_like'


# ---------------------------新闻管理------------------------------
class News(models.Model):
    NEWS_TYPE_CHOICES = [
        (0, '普通'),
        (1, '竞赛新闻'),
        (2, '课程新闻')
    ]

    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=250, null=True, blank=True, verbose_name='新闻标题')
    news_introduce = models.TextField(null=True, blank=True, verbose_name='新闻内容')
    news_creator = models.CharField(max_length=48, blank=True, null=True, verbose_name='创建者')
    creator_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    news_importance = models.IntegerField(default='0', verbose_name='优先级')
    news_type = models.SmallIntegerField(default='0', choices=NEWS_TYPE_CHOICES, verbose_name='新闻类型')
    news_forget_key = models.IntegerField(null=True, blank=True, verbose_name='外键编号')

    class Meta:
        verbose_name = '新闻管理'
        managed = True
        db_table = 'news'


# ---------------------------气球管理------------------------------
class Balloon(models.Model):
    balloon_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    solution_id = models.IntegerField(verbose_name='提交编号')
    contest_id = models.IntegerField(verbose_name='竞赛编号')
    problem_id = models.IntegerField(verbose_name='问题编号')
    balloon_status = models.SmallIntegerField(verbose_name='气球状态')

    class Meta:
        verbose_name = '气球管理'
        managed = True
        db_table = 'balloon'


# ---------------------------打印管理------------------------------
class Printer(models.Model):
    printer_id = models.AutoField(primary_key=True)
    printer_user = models.CharField(max_length=48, verbose_name='打印者')
    printer_date = models.DateTimeField(auto_now=True, verbose_name='打印时间')
    printer_status = models.BooleanField(null=True, blank=True, verbose_name='打印状态')
    printer_content = models.TextField(null=True, blank=True, verbose_name='打印内容')

    class Meta:
        verbose_name = '打印管理'
        managed = True
        db_table = 'printer'


# ---------------------------课程管理------------------------------
# 课程文件重命名
def course_cover_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'course_file/{instance.course_id}/course_cover/{filename}'


def course_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    type_list = {'0': 'file', '1': 'audio', '2': 'video', '3': 'image'}
    return f'course_file/{instance.course_id}/{type_list[instance.file_type]}/{filename}'


class Course(models.Model):
    COURSE_STATUS = [
        (0, '未激活'),
        (1, '公开'),
        (2, '私有'),
        (3, '收费'),
        (4, '结课')
    ]

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=48, verbose_name='课程名称')
    course_introduce = models.TextField(null=True, blank=True, verbose_name='课程介绍')
    course_cover = models.ImageField(upload_to=course_cover_path, null=True, blank=True, verbose_name='封面')
    create_time = models.DateTimeField(auto_now=True, verbose_name='课程创建时间')
    course_cost = models.IntegerField(default='0', verbose_name='课程价格')
    course_creator = models.CharField(max_length=48, verbose_name='课程创建者')
    course_status = models.SmallIntegerField(default='0', choices=COURSE_STATUS, verbose_name='课程状态')
    course_browse = models.IntegerField(default='0', verbose_name='浏览数量')

    class Meta:
        verbose_name = '课程管理'
        managed = True
        db_table = 'course'


class CourseUser(models.Model):
    IDENTITY_CHOICES = [
        (0, '教师'),
        (1, '助教'),
        (2, '专属班级老师'),
        (3, '专属班级助教')
    ]

    course_id = models.IntegerField(verbose_name='课程编号')
    course_user = models.CharField(max_length=48, verbose_name='用户账号')
    # course_class = models.IntegerField(null=True, blank=True, verbose_name='班级编号')
    user_identity = models.SmallIntegerField(default='0', verbose_name='用户身份')

    class Meta:
        verbose_name = '课程用户'
        managed = True
        db_table = 'course_user'


class CourseClass(models.Model):
    CLASS_TYPES = [
        (0, '普通班级'),
        (1, '默认班级'),
    ]

    course_id = models.IntegerField(verbose_name='课程编号')
    course_class = models.IntegerField(verbose_name='班级编号')
    class_type = models.SmallIntegerField(default='0', verbose_name='班级身份')

    class Meta:
        verbose_name = '课程班级'
        managed = True
        db_table = 'course_class'


class UserClass(models.Model):
    course_id = models.IntegerField(verbose_name='课程编号')
    course_user = models.CharField(max_length=48, verbose_name='用户账号')
    course_class = models.IntegerField(verbose_name='班级编号')

    class Meta:
        verbose_name = '老师管理班级'
        managed = True
        db_table = 'user_class'


class CourseMenu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField(verbose_name='课程编号')
    menu_name = models.CharField(max_length=255, verbose_name='文件夹名称')
    # menu_grade = models.IntegerField(default='0', verbose_name='文件夹级别')
    menu_number = models.IntegerField(default='0', verbose_name='文件夹编号')
    pre_menu = models.IntegerField(null=True, blank=True, verbose_name='前导文件夹')
    menu_status = models.BooleanField(default='0', verbose_name='目录状态')
    menu_type = models.SmallIntegerField(default='0', verbose_name='文件夹所属0文件1题库')

    class Meta:
        verbose_name = '课程菜单'
        managed = True
        db_table = 'course_menu'


class CourseFile(models.Model):
    FILE_TYPE_CHOICE = [
        (0, '文件'),
        (1, '音频'),
        (2, '视频'),
        (3, '图片')
    ]

    file_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField(verbose_name='课程编号')
    file_type = models.SmallIntegerField(default='0', choices=FILE_TYPE_CHOICE, verbose_name='文件类型')
    file_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='上传时间')
    file_creator = models.CharField(max_length=48, verbose_name='用户编号')
    file_menu = models.IntegerField(null=True, blank=True, verbose_name='文件目录')
    file_number = models.IntegerField(null=True, blank=True, verbose_name='文件编号')
    course_file = models.FileField(upload_to=course_file_path, null=True, blank=True, verbose_name='文件')
    file_status = models.BooleanField(default='0', verbose_name='文件状态')

    class Meta:
        verbose_name = '课程文件'
        managed = True
        db_table = 'course_file'


class CourseEvaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    evaluation_creator = models.CharField(max_length=48, verbose_name='评价创建者')
    evaluation_course = models.IntegerField(verbose_name='课程编号')
    evaluation_content = models.TextField(verbose_name='评价内容')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    evaluation_score = models.IntegerField(default='0')

    class Meta:
        verbose_name = '课程评价'
        managed = True
        db_table = 'course_evaluation'


# ---------------------------课程章节管理----------------------------
class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField(verbose_name='课程编号')
    chapter_title = models.CharField(max_length=50, verbose_name='章节标题')
    chapter_grade = models.IntegerField(default='0', verbose_name='章节级别')
    chapter_number = models.IntegerField(default='0', verbose_name='章节编号')
    pre_chapter = models.IntegerField(null=True, blank=True, verbose_name='前导章节')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    chapter_states = models.SmallIntegerField(default='0', verbose_name='章节状态0不免费1免费')

    class Meta:
        verbose_name = '章节管理'
        managed = True
        db_table = 'chapter'


class ChapterContent(models.Model):
    chapter_content_id = models.AutoField(primary_key=True)
    chapter_id = models.IntegerField(verbose_name='章节编号')
    chapter_content_title = models.CharField(max_length=48, null=True, blank=True, verbose_name='章节内容标题')
    chapter_content = models.TextField(null=True, blank=True, verbose_name='章节内容')
    chapter_number = models.IntegerField(default='0', verbose_name='章节内容顺序')
    chapter_creator = models.CharField(max_length=48, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '章节内容'
        managed = True
        db_table = 'chapter_content'


class ChapterClass(models.Model):
    STATUS_CHOICES = [
        (0, '未公开'),
        (1, '公开'),
        (2, '创建中')
    ]

    chapter_id = models.IntegerField(verbose_name='章节编号')
    class_id = models.IntegerField(verbose_name='班级编号')
    chapter_status = models.SmallIntegerField(default='0', choices=STATUS_CHOICES, verbose_name='章节状态')
    chapter_time = models.DateTimeField(auto_now=True, verbose_name='需改时间')

    class Meta:
        verbose_name = '章节班级'
        managed = True
        db_table = 'chapter_class'


class ChapterUser(models.Model):
    chapter_id = models.IntegerField(verbose_name='章节编号')
    chapter_content_id = models.IntegerField(verbose_name='章节内容编号')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    status = models.BooleanField(default='0', verbose_name='学习状态')
    class_id = models.IntegerField(verbose_name='学习的班级')

    class Meta:
        verbose_name = '用户学习状态'
        managed = True
        db_table = 'chapter_user'


# ---------------------------课程问题管理----------------------------
class Question(models.Model):
    QUESTION_TYPE_CHOICE = [
        (0, '单选题'),
        (1, '多选题'),
        (2, '判断题'),
        (3, '填空题'),
        (4, '解答题')
    ]

    question_id = models.AutoField(primary_key=True)
    question_description = models.TextField()
    question_type = models.SmallIntegerField(choices=QUESTION_TYPE_CHOICE)
    question_option = models.TextField(null=True, blank=True, verbose_name='问题选项：`|`分割选项')
    question_answer = models.TextField(null=True, blank=True, verbose_name='问题答案：json存储')
    question_course = models.IntegerField(verbose_name='所属课程id')
    question_change = models.BooleanField(default='0', verbose_name='允许答案互换')
    upload_user = models.CharField(max_length=48, null=True, blank=True, verbose_name='上传用户')
    upload_time = models.DateTimeField(auto_now=True, blank='上传时间')
    question_status = models.BooleanField(default='0', verbose_name='问题发布状态')
    belong_menu = models.IntegerField(default='0', verbose_name="所属目录")

    class Meta:
        verbose_name = '课程问题管理'
        managed = True
        db_table = 'question'


# ---------------------------课程作业管理----------------------------
class Task(models.Model):
    TYPE_CHOICE = [
        (0, '测试'),
        (1, '作业'),
        (2, '考试')
    ]

    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=50, null=True, blank=True, verbose_name='作业标题')
    task_explain = models.TextField(null=True, blank=True, verbose_name='作业描述')
    task_creator = models.CharField(max_length=48, blank=True, null=True, verbose_name='作业创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    task_type = models.SmallIntegerField(default='0', choices=TYPE_CHOICE, verbose_name='作业类型')
    begin_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    task_status = models.BooleanField(default='0', verbose_name='作业状态')
    task_judge = models.SmallIntegerField(default='0', verbose_name='是否自动判题')
    task_chapter = models.IntegerField(null=True, blank=True, verbose_name='所属章节')
    task_course = models.IntegerField(null=True, blank=True, verbose_name='所属课程')
    task_class = models.IntegerField(default='0', verbose_name='所属班级【0为所有班级】')

    class Meta:
        verbose_name = '课程作业管理'
        managed = True
        db_table = 'task'


class TaskQuestion(models.Model):
    QUESTION_TYPE = [
        (0, '题库题目'),
        (1, '编程题目')
    ]

    task_id = models.IntegerField(verbose_name='作业编号')
    question_type = models.SmallIntegerField(default='0', choices=QUESTION_TYPE, verbose_name='问题类型')
    question_id = models.IntegerField(verbose_name='问题编号')
    question_number = models.IntegerField(null=True, blank=True, verbose_name='问题序号')
    question_score = models.IntegerField(null=True, blank=True, verbose_name='问题分数')

    class Meta:
        verbose_name = '作业问题管理'
        managed = True
        db_table = 'take_question'


class TaskSubmit(models.Model):
    submit_id = models.AutoField(primary_key=True)
    task_id = models.IntegerField(verbose_name='作业编号')
    task_user = models.CharField(max_length=48, verbose_name='用户编号')
    create_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')
    use_time = models.IntegerField(null=True, blank=True, verbose_name='花费时间')
    submit_content = models.TextField(verbose_name='提交答案|json格式存储')
    submit_score = models.IntegerField(default='-1', verbose_name='作业分数')
    submit_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='提交ip地址')
    judge_time = models.DateTimeField(auto_now_add=True, verbose_name='判题时间')
    judge_user = models.CharField(max_length=48, null=True, blank=True, verbose_name='判题者')

    class Meta:
        verbose_name = '作业提交'
        managed = True
        db_table = 'task_submit'


# ---------------------------消息表管理----------------------------
class Message(models.Model):

    message_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=False,blank=False,verbose_name="消息标题")
    content = models.TextField(null=False,blank=False,verbose_name="消息内容,保存html")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    creator = models.CharField(max_length=32,null=False,blank=False,verbose_name="发布者")
    creator_nick = models.CharField(max_length=24, blank=True, null=True, verbose_name='发布者昵称')
    recipient_des = models.TextField(null=False,blank=False,verbose_name="接收对象说明")
    recipient_type =models.CharField(max_length=10,null=False,blank=False,verbose_name="接收对象类型|class|course|person|contest")
    recipient_id = models.IntegerField(default=0,null=False,blank=True,verbose_name="当是课程中的消息时，存储课程id，其它情况为0")
    display_mode = models.IntegerField(default=1,null=False,blank=True,verbose_name="展示方式，1普通消息，2弹窗提示")
    defunct = models.CharField(default='N',max_length=4,null=False,blank=True,verbose_name="是否失效，N否，Y是")
    is_delete = models.CharField(default='N',max_length=4,null=False,blank=True,verbose_name="是否删除，N否，Y是")

    class Meta:
        verbose_name = '消息表'
        managed = True
        db_table = 'message'


class UserMessage(models.Model):

    user_message_id = models.AutoField(primary_key=True)
    message_id = models.IntegerField(null=False, blank=False, verbose_name="消息Id")
    user_id = models.CharField(max_length=32, null=False, blank=False, verbose_name="接受的用户")
    is_view = models.IntegerField(default=0, null=False, blank=True, verbose_name="是否已读，0否，1是")
    view_date = models.DateTimeField(null=True, blank=True, verbose_name="查看时间")

    class Meta:
        verbose_name = '用户消息表'
        managed = True
        db_table = 'user_message'


class PaymentHistory(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=48, verbose_name='用户编号')
    course_id = models.IntegerField(verbose_name='课程编号')
    class_id = models.IntegerField(verbose_name='班级编号')
    payment_amount = models.IntegerField(verbose_name='支付金额')
    is_payment = models.SmallIntegerField(verbose_name='是否支付')
    payment_time = models.DateTimeField(auto_now=True, verbose_name='判题者')


def files_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'image/{filename}'


class FilePath(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_path = models.ImageField(upload_to=files_path, verbose_name='文件地址')
    file_creator = models.CharField(max_length=48, verbose_name='提交用户')
    file_time = models.DateTimeField(verbose_name='提交时间')

    class Meta:
        verbose_name = '文件管理表'
        managed = True
        db_table = 'file_path'


class NewMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    target_user = models.CharField(max_length=48, verbose_name='接收用户')
    message_creator = models.CharField(max_length=48, verbose_name='发送用户')
    message_content = models.TextField(null=True, blank=True, verbose_name='内容')
    message_time = models.DateTimeField(verbose_name='创建时间')
    message_type = models.SmallIntegerField(default=0, verbose_name='信息类型')
    message_team = models.IntegerField(null=True, blank=True, verbose_name='消息发送团队')

    class Meta:
        verbose_name = '新消息表'
        managed = True
        db_table = 'new_message'
