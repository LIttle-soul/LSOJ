from django.db import models


# -------------------------------------------------------用户管理---------------------------------------
class Password(models.Model):
    user_id = models.CharField(max_length=32, primary_key=True, verbose_name='学号/工号')
    password = models.CharField(max_length=64, verbose_name='密码')

    class Meta:
        managed = True
        db_table = 'password'


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

    user_id = models.OneToOneField(to='Password', to_field='user_id', on_delete=models.CASCADE, primary_key=True, verbose_name='已注册用户')
    real_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='真实姓名')
    nick = models.CharField(max_length=24, blank=True, null=True, verbose_name='昵称')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    submit = models.IntegerField(default=0, verbose_name='提交数量')
    solved = models.IntegerField(default=0, verbose_name='解决数量')
    defunct = models.BooleanField(default=0, verbose_name='是否隐藏')
    ip = models.GenericIPAddressField(verbose_name='ip地址')
    access_time = models.DateTimeField(blank=True, null=True, verbose_name='登陆时间')
    reg_time = models.DateTimeField(blank=True, null=True, verbose_name='注册时间')
    school = models.CharField(max_length=20, verbose_name='学校')
    score = models.IntegerField(default=0, verbose_name='得分')
    sex = models.IntegerField(choices=SEX_CHOICE, verbose_name='性别')
    role_pri = models.IntegerField(choices=POWER_CHOICE, default='4', verbose_name='权限')
    is_delete = models.BooleanField(default=0, verbose_name='保护')

    class Meta:
        managed = True
        db_table = 'user'


class LoginLog(models.Model):
    log_id = models.AutoField(primary_key=True, verbose_name='登陆日志')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='登录IP')
    time = models.DateTimeField(null=True, blank=True, verbose_name='登入时间')
    login_way = models.CharField(max_length=256, blank=True, null=True, verbose_name='登录方法')

    class Meta:
        managed = True
        db_table = 'login_log'


class Online(models.Model):
    hash = models.CharField(max_length=32, primary_key=True, verbose_name='主键')
    ip = models.GenericIPAddressField(verbose_name='ip地址')
    ua = models.CharField(max_length=255, verbose_name='浏览器相关的标识字符串')
    refer = models.CharField(max_length=255, blank=True, null=True, verbose_name='访问的上个页面的地址')
    last_move = models.IntegerField(verbose_name='最后一次修改的时间')
    first_time = models.IntegerField(blank=True, null=True, verbose_name='第一次访问的时间')
    uri = models.CharField(max_length=255, blank=True, null=True, verbose_name='统一资源指示器')

    class Meta:
        managed = True
        db_table = 'online'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, verbose_name='队伍名')
    users = models.ForeignKey(to='User', to_field='user_id', on_delete=models.CASCADE, verbose_name='团队成员')
    trainer = models.CharField(max_length=48, null=True, blank=True, verbose_name='指导老师')
    school = models.CharField(max_length=50, verbose_name='学校名')
    defunct = models.BooleanField(default='0', verbose_name='是否屏蔽')

    class Meta:
        managed = True
        db_table = 'team'


# --------------------------------------------------------题目管理-----------------------------------------
class Problems(models.Model):
    problem_id = models.AutoField(primary_key=True, verbose_name='题目编号')
    title = models.CharField(max_length=50, verbose_name='题目标题')
    description = models.TextField(blank=True, null=True, verbose_name='题目描述')
    input = models.TextField(blank=True, null=True, verbose_name='输入描述')
    output = models.TextField(blank=True, null=True, verbose_name='输出描述')
    sample_input = models.TextField(blank=True, null=True, verbose_name='样例输入')
    sample_output = models.TextField(blank=True, null=True, verbose_name='样例输出')
    spj = models.BooleanField(default=0, verbose_name='是否特判')
    hint = models.TextField(blank=True, null=True, verbose_name='提示')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    in_data = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    time_limit = models.IntegerField(default=1000, verbose_name='时间限制')
    memory_limit = models.IntegerField(default=128, verbose_name='空间限制')
    defunct = models.BooleanField(default=0, verbose_name='是否隐藏')
    accepted = models.IntegerField(default=0, verbose_name='通过数')
    submit = models.IntegerField(default=0, verbose_name='提交数')
    # solved = models.IntegerField(blank=True, null=True, verbose_name='解答')
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='知识点')
    difficulty = models.IntegerField(blank=True, null=True, verbose_name='难度')
    creator = models.OneToOneField(to='User', to_field='user_id', on_delete=models.CASCADE, blank=True, null=True, verbose_name='创建者')
    is_delete = models.BooleanField(default=0, verbose_name='题目保护')

    class Meta:
        managed = True
        db_table = 'problems'


class Solution(models.Model):
    solution_id = models.IntegerField(primary_key=True, verbose_name='运行编号')
    problem_id = models.IntegerField(verbose_name='问题编号')
    user_id = models.CharField(max_length=48, verbose_name='用户编号')
    time = models.IntegerField(verbose_name='运行时间')
    memory = models.IntegerField(verbose_name='运行空间')
    in_date = models.DateTimeField(verbose_name='加入时间')
    result = models.IntegerField(verbose_name='运行结果')
    language = models.IntegerField(verbose_name='所用语言')
    ip = models.GenericIPAddressField(verbose_name='用户地址')
    contest_id = models.IntegerField(blank=True, null=True, verbose_name='所属竞赛组')
    valid = models.BooleanField(default='1', verbose_name='是否有效')
    num = models.IntegerField(blank=True, null=True, verbose_name='代码在竞赛中的顺序号')
    code_length = models.IntegerField(verbose_name='代码长度')
    judge_time = models.DateTimeField(blank=True, null=True, verbose_name='判题时间')
    pass_rate = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='通过百分比')

    class Meta:
        managed = True
        db_table = 'solution'


class SourceCode(models.Model):
    solution_id = models.AutoField(primary_key=True, verbose_name='运行编号')
    source = models.TextField(null='True', blank='True', verbose_name='源代码')

    class Meta:
        managed = True
        db_table = 'source_code'


class CustomInput(models.Model):
    solution_id = models.AutoField(primary_key=True, verbose_name='用户编号')
    input_text = models.TextField(null='True', verbose_name='输入测试数据')

    class Meta:
        managed = True
        db_table = 'custom_input'


class Sim(models.Model):
    s_id = models.IntegerField(verbose_name='solution_id')
    sim_s_id = models.IntegerField(null=True, blank=True, verbose_name='与 s_id 相似的 solution_id')
    sim = models.IntegerField(null=True, blank=True, verbose_name='相似度（50-100）')

    class Meta:
        managed = True
        db_table = 'sim'


class CompileInfo(models.Model):
    solution_id = models.IntegerField(primary_key=True, verbose_name='运行编号')
    error = models.TextField(null=True, blank=True, verbose_name='编译错误原因')

    class Meta:
        managed = True
        db_table = 'compile_info'


class RuntimeInfo(models.Model):
    solution_id = models.IntegerField(primary_key=True, verbose_name='运行编号')
    error = models.TextField(null=True, blank=True, verbose_name='编译错误原因')

    class Meta:
        managed = True
        db_table = 'runtime_info'


# --------------------------------------------------------新闻管理-----------------------------------------
class News(models.Model):
    news_id = models.AutoField(primary_key=True, verbose_name='新闻编号')
    user_id = models.CharField(max_length=48, verbose_name='用户账号')
    title = models.CharField(max_length=50, verbose_name='新闻标题')
    content = models.TextField(verbose_name='新闻内容')
    time = models.DateTimeField(verbose_name='创建时间')
    importance = models.IntegerField(default=0, verbose_name='关键字')
    defunct = models.BooleanField(default=0, verbose_name='是否失效')
    # image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='新闻图片')
    # image_path = models.FilePathField(path=os.path.join(settings.LOCAL_FILE_DIR, 'images'), match="new.*.png$", verbose_name='图片路径')

    class Meta:
        managed = True
        db_table = 'news'


# ---------------------------------------------------竞赛管理----------------------------------------------
class Contest(models.Model):
    contest_id = models.AutoField(primary_key=True, verbose_name='竞赛编号')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='竞赛标题')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    defunct = models.BooleanField(default='0', verbose_name='是否屏蔽')
    description = models.TextField(blank=True, null=True, verbose_name='竞赛描述')
    private = models.BooleanField(default='1', verbose_name='是否公开')
    lang_mask = models.IntegerField(default='1', verbose_name='竞赛语言')

    class Meta:
        managed = True
        db_table = 'contest'


class ContestProblem(models.Model):
    contest_id = models.IntegerField(verbose_name='竞赛编号')
    problem_id = models.IntegerField(verbose_name='题目编号')
    title = models.CharField(max_length=200, verbose_name='标题')
    num = models.IntegerField(verbose_name='竞赛题目编号')

    class Meta:
        managed = True
        db_table = 'contest_problem'


# ---------------------------------------------------论坛模块----------------------------------------------
class Topic(models.Model):
    TOPIC_CHOICE = [
        (0, '不置顶'),
        (1, '题目置顶'),
        (2, '分区置顶'),
        (3, '总置顶'),
    ]
    tid = models.AutoField(primary_key=True, verbose_name='论坛序号')
    title = models.CharField(max_length=60, verbose_name='标题')
    status = models.BooleanField(verbose_name='状态')
    top_level = models.IntegerField(default='0', verbose_name='置顶等级')
    cid = models.IntegerField(null=True, blank=True, verbose_name='竞赛编号')
    pid = models.IntegerField(null=True, blank=True, verbose_name='竞赛中题目编号')
    author_id = models.CharField(max_length=48, verbose_name='作者账号')

    class Meta:
        managed = True
        db_table = 'topic'


class Reply(models.Model):
    REPLY_CHOICE = [
        (0, '正常'),
        (1, '锁定'),
        (2, '删除'),
    ]
    rid = models.AutoField(primary_key=True, verbose_name='帖子序号')
    author_id = models.CharField(max_length=48, verbose_name='作者账号')
    time = models.DateTimeField(verbose_name='发布时间')
    content = models.TextField(verbose_name='帖子内容')
    topic_id = models.IntegerField(verbose_name='帖子分组')
    status = models.IntegerField(choices=REPLY_CHOICE, verbose_name='论坛状态')
    ip = models.GenericIPAddressField(verbose_name='发帖者地址')

    class Meta:
        managed = True
        db_table = 'reply'


if __name__ == '__main__':
    for i in range(11):
        print(i)