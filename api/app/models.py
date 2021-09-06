from django.db import models
from app.config.choices import *
import uuid


# ---------------------------地址管理------------------------------
class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, verbose_name='省份编号')
    province_name = models.CharField(max_length=25, verbose_name='省份名')

    class Meta:
        verbose_name = '省份管理'
        managed = True
        db_table = 'province'


class Municipality(models.Model):
    municipality_id = models.IntegerField(primary_key=True, verbose_name='城市编号')
    municipality_name = models.CharField(max_length=50, verbose_name='城市名')
    municipality_province = models.ForeignKey(to='Province', on_delete=models.CASCADE, blank=True, verbose_name='城市所在省份')

    class Meta:
        verbose_name = '城市管理'
        managed = True
        db_table = 'municipality'


# -------------------------------学校管理--------------------------
class School(models.Model):
    school_id = models.CharField(max_length=20, primary_key=True, verbose_name='学校编号')
    school_name = models.CharField(max_length=50, verbose_name='学校名称')
    school_describe = models.TextField(null=True, blank=True, verbose_name='学校描述')
    school_department = models.CharField(max_length=20, null=True, blank=True, verbose_name='主管部门')
    school_municipality = models.ForeignKey(to='Municipality', on_delete=models.SET_NULL, null=True, verbose_name='学校所在城市')
    school_rank = models.CharField(max_length=20, blank=True, null=True, verbose_name='办学层次')
    school_remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='学校备注')

    class Meta:
        verbose_name = '学校管理'
        managed = True
        db_table = 'school'


class College(models.Model):
    college_id = models.CharField(max_length=30, primary_key=True, verbose_name='学院编号')
    college_name = models.CharField(max_length=50, verbose_name='学院名称')
    college_school = models.ForeignKey(to='School', on_delete=models.CASCADE, blank=True, verbose_name='学院所在学校')

    class Meta:
        verbose_name = '学院管理'
        managed = True
        db_table = 'college'


# ---------------------------班级管理------------------------------
class Class(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True, verbose_name='班级编号')
    class_name = models.CharField(max_length=50, verbose_name='班级名称')
    class_creator = models.ForeignKey(to='User', related_name='class_creator', on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    class_introduce = models.CharField(max_length=256, null=True, blank=True, verbose_name='班级介绍')
    class_type = models.SmallIntegerField(null=True, blank=True, choices=CLASS_TYPE, verbose_name='班级类型')
    class_college = models.ForeignKey(to='College', on_delete=models.SET_NULL, null=True, verbose_name='班级所在学院')
    class_user = models.ManyToManyField(to='UserPassword', through='ClassUser', through_fields=('class_id', 'user_id'), verbose_name='班级用户')

    class Meta:
        verbose_name = '班级管理'
        managed = True
        db_table = 'class'


class ClassUser(models.Model):
    class_id = models.ForeignKey(to='Class', on_delete=models.CASCADE, verbose_name='班级序号')
    user_id = models.ForeignKey(to='UserPassword', on_delete=models.CASCADE, verbose_name='用户账号')
    user_type = models.SmallIntegerField(default='0', choices=USER_TYPE, verbose_name='用户类型')
    add_time = models.DateTimeField(auto_now=True, verbose_name='加入时间')
    add_type = models.SmallIntegerField(default='2', choices=ADD_TYPE, verbose_name='加入方式')
    user_remark = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户备注')

    class Meta:
        verbose_name = '班级用户'
        managed = True
        db_table = 'class_user'


# ---------------------------用户管理------------------------------
class UserPassword(models.Model):
    user_id = models.CharField(max_length=48, primary_key=True, verbose_name='用户账号')
    user_password = models.CharField(max_length=48, verbose_name='用户密码')
    registration_time = models.DateTimeField(auto_now=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '用户密码'
        managed = True
        db_table = 'user_password'


# 用户头像文件重命名
def user_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'user_file/{instance.user_id}/user_icon/{filename}'


class User(models.Model):
    user_id = models.OneToOneField(to='UserPassword', on_delete=models.CASCADE, primary_key=True, verbose_name='用户账号')
    user_icon = models.ImageField(upload_to=user_icon_path, null=True, blank=True, verbose_name='用户头像')
    student_id = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户学号')
    user_name = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户姓名')
    user_nick = models.CharField(max_length=24, blank=True, null=True, verbose_name='用户昵称')
    user_introduce = models.CharField(max_length=250, blank=True, null=True, verbose_name='用户介绍')
    user_power = models.SmallIntegerField(choices=POWER_CHOICES, default=4, verbose_name='用户身份')
    user_score = models.IntegerField(default='0', verbose_name='用户得分')
    user_sex = models.SmallIntegerField(choices=SEX_CHOICES, null=True, blank=True, verbose_name='用户性别')
    user_telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户电话')
    user_email = models.EmailField(blank=True, null=True, verbose_name='用户邮箱')
    user_birthday = models.DateTimeField(null=True, blank=True, verbose_name='用户生日')
    user_school = models.ForeignKey(to='School', on_delete=models.SET_NULL, null=True, verbose_name='用户所在学校')
    user_address = models.ForeignKey(to='Municipality', on_delete=models.SET_NULL, null=True, verbose_name='用户所在地址')

    class Meta:
        verbose_name = '用户管理'
        managed = True
        db_table = 'user'


class LoginLog(models.Model):
    user_id = models.ForeignKey(to='UserPassword', on_delete=models.DO_NOTHING, verbose_name='登陆用户')
    login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='用户IP')
    login_time = models.DateTimeField(auto_now=True, verbose_name='登陆时间')
    login_way = models.CharField(max_length=256, blank=True, null=True, verbose_name='登录方法')

    class Meta:
        verbose_name = '登录日志'
        managed = True
        db_table = 'login_log'


class LimitLogin(models.Model):
    user_id = models.ForeignKey(to='UserPassword', on_delete=models.CASCADE, verbose_name='用户账号')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    limit_type = models.SmallIntegerField(default='0', choices=LIMIT_TYPE, verbose_name='限制类型')
    limit_time = models.DurationField(default='0', verbose_name='限制时长')

    class Meta:
        verbose_name = '登录限制'
        managed = True
        db_table = 'limit_login'


class Collection(models.Model):
    collection_user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户编号')
    collection_type = models.SmallIntegerField(default='0', choices=TYPE_CHOICES, verbose_name='收藏类型')
    collection_forget_key = models.IntegerField(verbose_name='收藏内容的编号')
    collection_time = models.DateTimeField(auto_now=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        managed = True
        db_table = 'collection'


# ---------------------------代码语言------------------------------
class CodeLanguage(models.Model):
    language_id = models.IntegerField(primary_key=True, verbose_name='语言编号')
    language_name = models.CharField(max_length=50, verbose_name='语言名')

    class Meta:
        verbose_name = '代码语言'
        managed = True
        db_table = 'code_language'


# ---------------------------题目管理------------------------------
# 题目文件重命名
def problem_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'problem_file/{instance.problem_id}/{filename}'


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
    problem_creator = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True, verbose_name='题目创建者')
    problem_status = models.SmallIntegerField(default='0', choices=PROBLEM_STATUS_CHOICE, verbose_name='题目状态')

    class Meta:
        verbose_name = '问题管理'
        managed = True
        db_table = 'problem'


class ProblemFile(models.Model):
    problem_id = models.ForeignKey(to=Problem, on_delete=models.CASCADE, verbose_name='问题编号')
    problem_file = models.ImageField(verbose_name='问题图片')

    class Meta:
        verbose_name = '问题文件'
        managed = True
        db_table = 'problem_file'


# ---------------------------提交管理------------------------------
class Solution(models.Model):
    solution_id = models.AutoField(primary_key=True)
    problem_id = models.ForeignKey(to='Problem', on_delete=models.CASCADE, verbose_name='问题编号')
    user_id = models.ForeignKey(to='UserPassword', on_delete=models.CASCADE, verbose_name='用户账号')
    contest_id = models.ForeignKey(to='Contest', on_delete=models.SET_NULL, null=True, verbose_name='竞赛编号')
    level_id = models.ForeignKey(to='Level', on_delete=models.SET_NULL, null=True, verbose_name='关卡编号')
    solution_code = models.TextField(null=True, blank=True, verbose_name='提交代码')
    solution_language = models.ForeignKey(to='CodeLanguage', on_delete=models.DO_NOTHING, verbose_name='提交语言')
    solution_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')
    solution_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='提交地址')
    code_length = models.IntegerField(default='0', verbose_name='代码长度')
    run_time = models.IntegerField(blank=True, null=True, verbose_name='运行时间')
    run_memory = models.IntegerField(blank=True, null=True, verbose_name='运行空间')
    run_result = models.SmallIntegerField(default='0', choices=SUBMIT_RESULT, verbose_name='运行结果')
    run_error = models.TextField(null=True, blank=True, verbose_name='错误信息')
    run_pass_rate = models.IntegerField(default='0', verbose_name='通过的测试数')
    run_all_rate = models.IntegerField(default='1', verbose_name='所有的测试数')

    class Meta:
        verbose_name = '提交信息'
        managed = True
        db_table = 'solution'


class Sim(models.Model):
    solution_id = models.OneToOneField(to='Solution', on_delete=models.CASCADE, verbose_name='提交编号')
    sim_solution_id = models.ForeignKey(to='Solution', related_name='sim_solution_id', on_delete=models.CASCADE, verbose_name='重复的提交编号')
    sim_ratio = models.DecimalField(default='0.0000', max_digits=5, decimal_places=4, verbose_name='重复率')

    class Meta:
        verbose_name = '提交判重'
        managed = True
        db_table = 'sim'


class UserRank(models.Model):
    user_id = models.OneToOneField(to='User', on_delete=models.CASCADE, primary_key=True, verbose_name='用户账号')
    user_solved = models.IntegerField(default=0, verbose_name='解决')
    user_submit = models.IntegerField(default=0, verbose_name='提交')
    user_accurate = models.IntegerField(default=0, verbose_name='答案正确')
    format_error = models.IntegerField(default=0, verbose_name='格式错误')
    wrong_answer = models.IntegerField(default=0, verbose_name='答案错误')
    time_over = models.IntegerField(default=0, verbose_name='时间超限')
    memory_over = models.IntegerField(default=0, verbose_name='内存超限')
    output_over = models.IntegerField(default=0, verbose_name='输出超限')
    runtime_error = models.IntegerField(default=0, verbose_name='运行错误')
    compile_error = models.IntegerField(default=0, verbose_name='编译错误')

    class Meta:
        verbose_name = '用户排名'
        managed = True
        db_table = 'user_rank'


# ---------------------------竞赛管理------------------------------
class Contest(models.Model):
    contest_id = models.AutoField(primary_key=True)
    contest_title = models.CharField(max_length=256, blank=True, null=True, verbose_name='竞赛标题')
    contest_introduce = models.TextField(null=True, blank=True, verbose_name='竞赛描述')
    contest_province = models.SmallIntegerField(default='0', choices=PROVINCE_CHOICE, verbose_name='竞赛类型')
    contest_password = models.CharField(max_length=50, null=True, blank=True, verbose_name='竞赛密码')
    contest_language = models.ManyToManyField(to='CodeLanguage', verbose_name='竞赛语言')
    contest_creator = models.ForeignKey(to='User', related_name='contest_creator', on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    contest_defunct = models.BooleanField(default='1', verbose_name='是否隐藏')
    contest_problem = models.ManyToManyField(to='Problem', through='ContestProblem', through_fields=('contest_id', 'problem_id'), blank=True, verbose_name='竞赛问题')
    contest_user = models.ManyToManyField(to='UserPassword', through='ContestUser', through_fields=('contest_id', 'contest_user'), blank=True, verbose_name='竞赛用户')
    contest_team = models.ManyToManyField(to='Class', through='ContestUser', through_fields=('contest_id', 'contest_class'), blank=True, verbose_name='竞赛团队')

    class Meta:
        verbose_name = '竞赛管理'
        managed = True
        db_table = 'contest'


class ContestProblem(models.Model):
    contest_id = models.ForeignKey(to='Contest', on_delete=models.CASCADE, verbose_name='竞赛编号')
    problem_id = models.ForeignKey(to='Problem', on_delete=models.CASCADE, verbose_name='问题编号')
    problem_num = models.IntegerField(null=True, blank=True, verbose_name='当前竞赛题目序号')

    class Meta:
        verbose_name = '竞赛问题'
        managed = True
        db_table = 'contest_problem'


class ContestUser(models.Model):
    contest_id = models.ForeignKey(to='Contest', on_delete=models.CASCADE, verbose_name='竞赛编号')
    contest_user = models.ForeignKey(to='UserPassword', on_delete=models.CASCADE, null=True, blank=True, verbose_name='竞赛用户')
    contest_class = models.ForeignKey(to='Class', on_delete=models.CASCADE, null=True, blank=True, verbose_name='竞赛团队')
    contest_account = models.CharField(max_length=48, blank=True, null=True, verbose_name='比赛账号生成')
    contest_grades = models.CharField(max_length=48, null=True, blank=True, verbose_name='获奖等级')
    contest_auditing = models.SmallIntegerField(default='0', verbose_name='审核状态')

    class Meta:
        verbose_name = '竞赛用户'
        managed = True
        db_table = 'contest_user'


# ---------------------------论坛管理------------------------------
# 论坛文件重命名
def forum_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'news_file/{instance.forum_id}/{filename}'


class Forum(models.Model):
    forum_id = models.AutoField(primary_key=True)
    forum_title = models.CharField(max_length=255, verbose_name='论坛标题')
    forum_content = models.TextField(verbose_name='论坛内容')
    forum_creator = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True, related_name='forum_creator', verbose_name='论坛创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='论坛创建时间')
    forum_status = models.SmallIntegerField(default='0', choices=STATUS_CHOICE, verbose_name='论坛状态')
    forum_section = models.SmallIntegerField(default='0', choices=TYPE_CHOICES, verbose_name='论坛版块')
    section_id = models.IntegerField(null=True, blank=True, verbose_name='版块编号')
    forum_priority = models.IntegerField(null=True, blank=True, verbose_name='优先级')
    forum_visits = models.IntegerField(null=True, blank=True, verbose_name='浏览量')
    forum_user = models.ManyToManyField(to='User', verbose_name='点赞用户')

    class Meta:
        verbose_name = '论坛管理'
        managed = True
        db_table = 'forum'


class ForumFile(models.Model):
    forum_id = models.ForeignKey(to='Forum', on_delete=models.CASCADE, verbose_name='论坛编号')
    forum_file = models.ImageField(upload_to=forum_file_path, verbose_name='论坛图片')

    class Meta:
        verbose_name = '论坛文件'
        managed = True
        db_table = 'forum_file'


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    forum_id = models.ForeignKey(to='Forum', on_delete=models.CASCADE, verbose_name='论坛编号')
    reply_content = models.TextField(verbose_name='回复内容')
    reply_creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, related_name='reply_creator', verbose_name='回复创建者')
    pre_reply = models.ForeignKey(to='Reply', on_delete=models.CASCADE, null=True, verbose_name='前置回复')
    create_time = models.DateTimeField(auto_now=True, verbose_name='回复创建时间')
    reply_status = models.SmallIntegerField(default='0', choices=STATUS_CHOICE, verbose_name='回复状态')
    reply_priority = models.IntegerField(null=True, blank=True, verbose_name='优先级')
    reply_user = models.ManyToManyField(to='User', verbose_name='点赞用户')

    class Meta:
        verbose_name = '用户回复'
        managed = True
        db_table = 'reply'


# ---------------------------关卡管理------------------------------
class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='关卡标题')
    level_description = models.TextField(null=True, blank=True, verbose_name='关卡描述')
    level_pre = models.ForeignKey(to='Level', on_delete=models.SET_NULL, null=True, verbose_name='前置关卡')
    pass_user = models.ManyToManyField(to='User', through='PassUser', through_fields=('level_id', 'user_id'), verbose_name='通过人数')
    level_num = models.IntegerField(null=True, blank=True, verbose_name='关卡编号')
    level_belong = models.ForeignKey(to='LevelKind', on_delete=models.SET_NULL, null=True, verbose_name='属于那个大类')
    level_creator = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True, related_name='level_creator', verbose_name='创建者')
    level_status = models.BooleanField(default='1', verbose_name='关卡状态')
    level_problem = models.ManyToManyField(to='Problem', through='LevelProblem', through_fields=('level_id', 'problem_id'), verbose_name='关卡问题')

    class Meta:
        verbose_name = '关卡管理'
        managed = True
        db_table = 'level'


class LevelKind(models.Model):
    kind_id = models.AutoField(primary_key=True)
    kind_title = models.CharField(max_length=48, null=True, blank=True, verbose_name='类型名称')
    kind_description = models.TextField(null=True, blank=True, verbose_name='类型介绍')

    class Meta:
        managed = True
        db_table = 'level_kind'


class PassUser(models.Model):
    level_id = models.ForeignKey(to='Level', on_delete=models.CASCADE, verbose_name='关卡编号')
    user_id = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户编号')
    pass_time = models.DateTimeField(auto_now=True, verbose_name='过关时间')

    class Meta:
        verbose_name = '过关用户'
        managed = True
        db_table = 'pass_user'


class LevelProblem(models.Model):
    level_id = models.ForeignKey(to='Level', on_delete=models.CASCADE, verbose_name='关卡编号')
    problem_id = models.ForeignKey(to='Problem', on_delete=models.CASCADE, verbose_name='问题编号')
    num = models.IntegerField(null=True, blank=True, verbose_name='当前问题编号')

    class Meta:
        verbose_name = '关卡问题'
        managed = True
        db_table = 'level_problem'


# ---------------------------新闻管理------------------------------
# 新闻文件重命名
def news_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:8]}.{ext}'
    return f'news_file/{instance.news_id}/{filename}'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=250, null=True, blank=True, verbose_name='新闻标题')
    news_introduce = models.TextField(null=True, blank=True, verbose_name='新闻内容')
    news_creator = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    creator_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    news_importance = models.IntegerField(default='0', verbose_name='优先级')

    class Meta:
        verbose_name = '新闻管理'
        managed = True
        db_table = 'news'


class NewsFile(models.Model):
    news_id = models.ForeignKey(to=News, on_delete=models.CASCADE, verbose_name='新闻编号')
    news_file = models.FileField(upload_to=news_file_path, verbose_name='新闻文件')

    class Meta:
        verbose_name = '新闻文件'
        managed = True
        db_table = 'news_file'


# ---------------------------气球管理------------------------------
class Balloon(models.Model):
    balloon_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to='UserPassword', on_delete=models.CASCADE, verbose_name='用户账号')
    solution_id = models.ForeignKey(to='Solution', on_delete=models.DO_NOTHING, verbose_name='提交编号')
    contest_id = models.ForeignKey(to='Contest', on_delete=models.DO_NOTHING, verbose_name='竞赛编号')
    problem_id = models.ForeignKey(to='Problem', on_delete=models.DO_NOTHING, verbose_name='问题编号')
    balloon_color = models.CharField(max_length=20, null=True, blank=True, verbose_name='气球颜色')

    class Meta:
        verbose_name = '气球管理'
        managed = True
        db_table = 'balloon'


# ---------------------------打印管理------------------------------
class Printer(models.Model):
    printer_id = models.AutoField(primary_key=True)
    printer_user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='打印者')
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
    type_list = ['file', 'audio', 'video', 'image']
    return f'course_file/{instance.course_id}/{type_list[instance.file_type]}/{filename}'


class Course(models.Model):
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
    course_id = models.IntegerField(verbose_name='课程编号')
    course_user = models.CharField(max_length=48, null=True, blank=True, verbose_name='用户账号')
    course_class = models.IntegerField(null=True, blank=True, verbose_name='班级编号')
    user_identity = models.SmallIntegerField(default='0', verbose_name='用户身份')

    class Meta:
        verbose_name = '课程用户'
        managed = True
        db_table = 'course_user'


class CourseMenu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_grade = models.IntegerField(default='0', verbose_name='文件夹级别')
    menu_number = models.IntegerField(default='0', verbose_name='文件夹编号')
    pre_menu = models.IntegerField(null=True, blank=True, verbose_name='前导文件夹')
    menu_status = models.BooleanField(default='0', verbose_name='目录状态')

    class Meta:
        verbose_name = '课程菜单'
        managed = True
        db_table = 'course_menu'


class CourseFile(models.Model):
    course_id = models.IntegerField(verbose_name='课程编号')
    file_type = models.SmallIntegerField(default='0', choices=FILE_TYPE_CHOICE, verbose_name='文件类型')
    file_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='上传时间')
    file_creator = models.CharField(max_length=48, verbose_name='用户编号')
    file_menu = models.IntegerField(default='0', verbose_name='文件目录')
    file_number = models.IntegerField(null=True, blank=True, verbose_name='文件编号')
    course_file = models.FileField(upload_to=course_file_path, verbose_name='文件')
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

    class Meta:
        verbose_name = '章节管理'
        managed = True
        db_table = 'chapter'


class ChapterContent(models.Model):
    chapter_id = models.IntegerField(verbose_name='章节编号')
    chapter_content = models.TextField(verbose_name='章节内容')
    chapter_creator = models.CharField(max_length=48, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '章节内容'
        managed = True
        db_table = 'chapter_content'


class ChapterClass(models.Model):
    chapter_id = models.IntegerField(verbose_name='章节编号')
    class_id = models.IntegerField(verbose_name='班级编号')
    chapter_status = models.SmallIntegerField(default='0', choices=CHAPTER_CLASS_STATUS_CHOICES, verbose_name='章节状态')

    class Meta:
        verbose_name = '章节班级'
        managed = True
        db_table = 'chapter_class'


class ChapterUser(models.Model):
    chapter_id = models.IntegerField(verbose_name='章节编号')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    status = models.BooleanField(default='0', verbose_name='学习状态')

    class Meta:
        verbose_name = '用户学习状态'
        managed = True
        db_table = 'chapter_user'


# ---------------------------课程问题管理----------------------------
class Question(models.Model):
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

    class Meta:
        verbose_name = '课程问题管理'
        managed = True
        db_table = 'question'


# ---------------------------课程作业管理----------------------------
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=50, null=True, blank=True, verbose_name='作业标题')
    task_explain = models.TextField(null=True, blank=True, verbose_name='作业描述')
    task_creator = models.CharField(max_length=48, blank=True, null=True, verbose_name='作业创建者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    task_type = models.SmallIntegerField(default='0', choices=TASK_TYPE_CHOICE, verbose_name='作业类型')
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
