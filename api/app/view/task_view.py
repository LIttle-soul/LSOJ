from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import sessions
from app import models
from django.views.generic import View
from django.utils import timezone
from app.RoleMethod.PublicMethod import PublicMethod
from django.views import View
from django.core import serializers
import json
from django import forms
import xlrd


# Create your views here.


"""
    所开设的题库分类，又或是直接放进去
    获取分类下的题目列表
    题目的增删改查
    曾 批量增加 文件批量增加 预设xls 后续在加

"""


class Task(View):
    """
        模块：题库创建（非批量）
        接口信息：
            get:
                返回课程下的所有题目，（根据查询条件返回对应信息）
            post:
                添加题目（题目类型 单选、多选、填空、简答）
        返回信息：
            get:
                返回题目信息
            post:
                返回添加成功信息，并在列表中显示
    """
    def get(self, request):
        course = request.GET.get("course")
        menu = request.GET.get("menu")
        # token = request.GET.get("token")
        # user = PublicMethod.parse_payload(token)
        questions = models.Question.objects.all().filter(
            question_course=course,
            belong_menu=menu,
        )
        info = []
        for question in questions:
            info.append({
                "question_description": question.question_description,
                "question_type": question.question_type,
                "upload_user": question.upload_user,
                "upload_time": question.upload_time,
                "question_status": question.question_status,
            })
        return JsonResponse({"contest": info})

    def choice(self, content, user):
        """
            单选题
            接口返回model.Question
        """
        choices = content["choice"]
        if True:
            task = models.Question.objects.create(
                question_description=content["content"],
                question_type=0,
                question_option=choices["a"]+"|"+choices["b"]+"|"+choices["c"]+"|"+choices["d"],
                question_answer=content.get("answer"),
                question_course=content.get("course"),
                upload_user=user["data"]["data"]["user_id"],
                upload_time=timezone.now(),
                belong_menu=content["menu"]
            )
        return task

    def choices(self, content, user):
        """
            多选题
        """
        if True:
            task = models.Question.objects.create(
                question_description=content["content"],
                question_type=1,
                question_option=choices["a"] + "|" + choices["b"] + "|" + choices["c"] + "|" + choices["d"],
                question_answer=content.get("answer"),
                question_course=content.get("course"),
                upload_user=user["data"]["data"]["user_id"],
                upload_time=timezone.now(),
                belong_menu=content["menu"]
            )
        return task

    def judge(self, content, user):
        """
            判断题
        """
        if True:
            task = models.Question.objects.create(
                question_description=content["content"],
                question_type=2,
                question_answer=content.get("answer"),
                question_course=content.get("course"),
                upload_user=user["data"]["data"]["user_id"],
                upload_time=timezone.now(),
                belong_menu=content["menu"]
            )
        return task

    def completion(self, content, user):
        """
            填空题
        """
        if True:
            task = models.Question.objects.create(
                question_description=content["content"],
                question_type=3,
                question_answer=content.get("answer"),
                question_course=content.get("course"),
                upload_user=user["data"]["data"]["user_id"],
                upload_time=timezone.now(),
                belong_menu=content["menu"]
            )
        return task

    def shortAnswer(self, content, user):
        """
            简答题
        """
        if True:
            task = models.Question.objects.create(
                question_description=content["content"],
                question_type=4,
                question_answer=content.get("answer"),
                question_course=content.get("course"),
                upload_user=user["data"]["data"]["user_id"],
                upload_time=timezone.now(),
                belong_menu=content["menu"]
            )
        return task

    def post(self, request):
        info = json.loads(request.body)
        print(info)
        user = PublicMethod().parse_payload(info.get("token"))
        form = info["content"]["type"]
        if user["status"]:
            if form == 0:
                self.choice(info.get("content"), user)
                print("1")
            elif form == 1:
                self.choices(info, user)
            elif form == 2:
                self.judge(info, user)
            elif form == 3:
                self.completion(info, user)
            elif form == 4:
                self.shortAnswer(info, user)
            return JsonResponse({"msg": 1})
        else:
            return JsonResponse({"msg": "logout"})


class TaskContent(View):
    """
    接口信息：
        获取题目具体信息
        get:
            获取单一题目的具体新欻
        post:
            修改题目信息

        返回信息：
        get:
            题目具体信息
        post:
            返回信息添加成功
    """
    def get(self, request):
        task = request.GET.get("task")
        content = models.Question.objects.all().get(question_id=task)
        choice = content.question_option
        choice = choice.split("|", 3)
        info = {
            "question_id": content.question_id,
            "content": content.question_description,
            "type": content.question_type,
            "option": {
                        "a": choice[0],
                        "b": choice[1],
                        "c": choice[2],
                        "d": choice[3]
                        },
            "answer": content.question_answer,
            "course": content.question_course,
            "uploader_user": content.upload_user,
            "question_status": content.question_status
        }
        return JsonResponse(info)

    def post(self, request):
        pass

class Menu(View):
    """
        模块：题库目录
        接口信息：
            get：
                获取目录，没有所属目录的直接显示题目
            post：
                修改添加目录，目录命名规则遵循新建文件规则

        返回信息：
            get：
                返回题库

            post：
                返回新建成功
    """
    def get(self, request):
        course = request.GET.get("courseId")
        menuQuerry = models.CourseMenu.objects.all().filter(menu_type=1, course_id=course)
        questions = models.Question.objects.all().filter(belong_menu=0, question_course=course)
        info = []
        task = []
        if menuQuerry or questions:
            for menu, question in menuQuerry, questions:
                info.append({
                    "menu_name": menu.menu_name,
                    "menu_number": menu.menu_number,
                    "pre_menu": menu.pre_menu,
                    "menu_status": menu.menu_status
                })
                task.append({
                    "question": question.question_id,
                    "question_name": question.question_description,
                    "create_time": question.upload_time,
                    "question_status": question.question_status,
                    "belong_menu": question.belong_menu
                })
        return JsonResponse({"menu": info, "task": task})

    def post(self, request):
        menu_name = request.POST.get("menuName")
        course_id = request.POST.get("course_id")
        pre_menu = request.POST.get("preMenu")
        if menu_name:
            models.CourseMenu.objects.create(
                course_id=course_id,
                menu_name=menu_name,
                pre_menu=pre_menu,
                menu_type=1,
            )
        return JsonResponse({"msg": "true"})



class deleteMenu(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class deleteTask(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class fileAdd(View):

    def get(self, request):
        pass

    def post(self, request):
        token = request.get("token")
        try:
            # 1.获取上传文件
            file = request.FILES.get('task_file')
            wb = xlrd.open_workbook(filename=None, file_contents=file.read())
            # 2.获取电源个对应值
            table = wb.sheet()[0]
            # 获取表的行数
            row_count = table.nrows
            # 获取列数
            col_count = table.ncols
        except:
            pass

