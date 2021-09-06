SEX_CHOICES = [
    (0, '男'),
    (1, '女')
]

POWER_CHOICES = [
    (0, '超级管理员'),
    (1, '管理员'),
    (2, '教师'),
    (3, '志愿者'),
    (4, '普通用户')
]

TYPE_CHOICES = [
    (0, '公共'),
    (1, '问题'),
    (2, '竞赛'),
    (3, '课程'),
    (4, '论坛'),
    (5, '帖子'),
    (6, '闯关'),
    (7, '班级')
]

CODE_CHOICES = [
    (0, 'C'),
    (1, 'C++'),
    (2, 'Java'),
    (3, 'Python2'),
    (4, 'Python3'),
    (5, 'Switch'),
    (6, 'C#'),
    (7, 'Go'),
    (8, 'Ruby'),
    (9, 'Bash'),
]

SUBMIT_RESULT = [
    (0, '等待中'),
    (1, '重判中'),
    (2, '编译中'),
    (3, '判题中'),
    (4, '答案正确'),
    (5, '格式错误'),
    (6, '答案错误'),
    (7, '时间超限'),
    (9, '内存超限'),
    (9, '输出超限'),
    (10, '运行错误'),
    (11, '编译错误'),
    (12, '编译器错误')
]

CLASS_TYPE = [
    (0, '行政班级'),
    (1, '团队类型'),
    (2, '课程班级')
]

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

LIMIT_TYPE = [
    (0, '黑名单模式'),
    (1, '白名单模式')
]

PROBLEM_STATUS_CHOICE = [
    (0, '公开'),
    (1, '隐藏'),
    (2, '竞赛')
]

PROVINCE_CHOICE = [
    (0, '公开'),
    (1, '私有'),
    (2, '作业')
]

STATUS_CHOICE = [
    (0, '审核中'),
    (1, '通过'),
    (2, '未通过'),
    (3, '已删除')
]

LEVEL_TYPE = [
    (1, '关卡'),
    (2, '关卡大类')
]

NEWS_TYPE_CHOICES = [
    (0, '普通'),
    (1, '竞赛新闻'),
    (2, '课程新闻')
]

COURSE_STATUS = [
    (0, '未激活'),
    (1, '公开'),
    (2, '私有'),
    (3, '收费')
]

FILE_TYPE_CHOICE = [
    (0, '文件'),
    (1, '音频'),
    (2, '视频'),
    (3, '图片')
]

CHAPTER_CLASS_STATUS_CHOICES = [
    (0, '公开'),
    (1, '未公开'),
    (2, '创建中')
]

QUESTION_TYPE_CHOICE = [
    (0, '单选题'),
    (1, '多选题'),
    (2, '判断题'),
    (3, '填空题'),
    (4, '解答题')
]

TASK_TYPE_CHOICE = [
    (0, '测试'),
    (1, '作业'),
    (2, '考试')
]

QUESTION_TYPE = [
    (0, '题库题目'),
    (1, '编程题目')
]