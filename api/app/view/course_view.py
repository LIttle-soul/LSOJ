from datetime import datetime
import json
from time import time
from django.core.checks import messages
from django.http import JsonResponse, FileResponse, request
from django.http.response import HttpResponse
from django.views.generic import View
from django.utils import timezone
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.models import *
from django.forms import model_to_dict
import base64
import numpy
import pandas as pd
from app.RoleMethod.PublicMethod import PublicMethod
publicMethod = PublicMethod()

# 将数据库查询的Object数据转为json类型数据方法
def changeToJson(data):
    json_list = []
    for i in data:
        json_dict = model_to_dict(i)
        json_list.append(json_dict)
    return json_list


class WeCourseHome(View):
    """
    模块: 我的课程首页
    接口信息:
    GET:
        None
    POST:
        token: token认证
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': "用户认证失败"})
        course_ids = CourseUser.objects.filter(course_user=user_id).values('course_id')
        course_ids = [item['course_id'] for item in course_ids]
        course_data = []
        for data in course_ids:
            course = Course.objects.filter(course_id=data).all()
            course = changeToJson(course)
            course_class = CourseUser.objects.filter(course_id=data).values('course_class')
            course_class = [item['course_class'] for item in course_class]
            course_data.append(
                {
                    'course_name': course[0]['course_name'],
                    'course_creator': course[0]['course_creator'],
                    'course_cover': str(course[0]['course_cover']),
                    'course_class': course_class,
                    'course_introduce': course[0]['course_introduce'],
                    'course_status': course[0]['course_status'],
                }
            )
        return JsonResponse({'status': 'Ture', 'course': course_data})


class CreateCourse(View):
    """
    模块: 创建课程
    接口信息:
    GET:
        None
    POST:
        token: token认证
        course_name: 课程名字
        course_introduce: 课程介绍
        course_cost: 课程价格
        course_cover: 课程封面
    """

    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        course_name = request.POST.get('course_name')
        course_introduce = request.POST.get('course_introduce')
        course_cost = request.POST.get('course_cost')
        course_cover = request.POST.get('course_cover')

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        course = Course.objects.create(
            course_name=course_name,
            course_introduce=course_introduce,
            course_cover=course_cover,
            create_time=timezone.now,
            course_cost=course_cost,
            course_creator=user_id,
            course_status='0',
            course_browse='0',
        )

        CourseUser.objects.create(
            course_id=course.course_id,
            course_user=user_id,
            user_identity='0'
        )
        
        courseClass = Class.objects.create(
            class_name='默认班级',
            class_creator=user_id,
            create_time=timezone.now,
            class_type='3',
        )

        CourseClass.objects.create(
            course_id=course.course_id,
            course_class=courseClass.class_id,
            class_type = '1'
        )

        massage = {'massage': '创建成功', 'course_id': course.course_id}
        return JsonResponse(massage, safe=False)


class DeleteCourse(View):
    """
    模块: 创建课程
    接口信息:
    GET:
        None
    POST:
        token: token认证
        course_id: 课程ID
    """
    def get(self, request):
        return JsonResponse({'err': '错误的访问方式'}, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        course = Course.objects.filter(course_id=course_id).first()
        if course.course_creator != user_id:
            return JsonResponse({'err': '无权限删除'})

        CourseUser.objects.filter(course_id=course_id).delete()
        UserClass.objects.filter(course_id=course_id).delete()
        CourseMenu.objects.filter(course_id=course_id).delete()
        CourseFile.objects.filter(course_id=course_id).delete()
        CourseEvaluation.objects.filter(evaluation_course=course_id).delete()
        CourseFile.objects.filter(course_id=course_id).delete()
        chapters = Chapter.objects.filter(course_id=course_id)
        for chapter in chapters:
            ChapterContent.objects.filter(chapter_id=chapter.chapter_id).delete()
            ChapterClass.objects.filter(chapter_id=chapter.chapter_id).delete()
            ChapterUser.objects.filter(chapter_id=chapter.chapter_id).delete()
        chapters.delete()
        classes = CourseClass.objects.filter(course_id=course_id)
        for i in classes:
            Class.objects.filter(class_id=i.course_class).delete()
            ClassUser.objects.filter(class_id=i.course_class).delete()
        classes.delete()
        return JsonResponse({'massage': '删除成功'})


class AddCourseMenu(View):
    """
    模块: 查看资料/新建文件夹
    接口信息:
    GET:
        course_id: 课程ID
        pre_menu: 前置文件夹ID
    POST:
        token: token认证
        course_id: 课程ID
        pre_menu: 前置文件夹ID
        menu_name: 文件夹名字
    """
    def get(self, request):
        course_id = request.GET.get('course_id')
        pre_menu = request.GET.get('pre_menu')
        menu_type = request.GET.get('menu_type')

        if not course_id:
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        
        menus = CourseMenu.objects.filter(course_id=course_id, pre_menu=pre_menu, menu_type=menu_type).order_by('menu_number')
        files = CourseFile.objects.filter(course_id=course_id, file_menu=pre_menu)

        menus_data = []
        files_data = []

        for menu in menus:
            menus_data.append({
                'menu_id': menu.menu_id,
                'course_id': menu.course_id,
                'menu_name': menu.menu_name,
                'pre_menu': menu.pre_menu,
            })
        
        for file in files:
            user = User.objects.filter(user_id=file.file_creator).first()
            files_data.append({
                'file_id': file.file_id,
                'course_id': file.course_id,
                'file_type': file.file_type,
                'file_name': file.file_name,
                'file_creator': file.file_creator,
                'file_creator_nick': user.user_nick,
                'file_menu': file.file_menu,
                # 'course_file': str(file.course_file),
            })

        massage = {'menus_data': menus_data, 'files_data': files_data}
        return JsonResponse(massage, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        pre_menu = request.POST.get('pre_menu')
        menu_name = request.POST.get('menu_name')
        menu_type = request.POST.get('menu_type')

        if not (token and course_id and menu_name and menu_type):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        users = CourseUser.objects.filter(course_id=course_id, course_user=user_id).first()
        if not users:
            massage = {'err': '无权限'}
            return JsonResponse(massage, safe=False)
        
        CourseMenu.objects.create(
            course_id=course_id,
            menu_name=menu_name,
            menu_number='0',
            pre_menu=pre_menu,
            menu_status='0',
            menu_type=menu_type
        )

        massage = {'massage': '创建成功'}
        return JsonResponse(massage, safe=False)
    

class UploadCourseFile(View):
    """
    模块: 上传文件
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            menu_id: 文件夹ID
            file: 文件
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        menu_id = request.POST.get('menu_id')
        file = request.FILES.get('file')

        if not (token and course_id and file):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        users = CourseUser.objects.filter(course_id=course_id, course_user=user_id).first()
        if not users:
            return JsonResponse({'err': '无权限'}, safe=False)

        audio_list = ['cda', 'wav', 'mp3', 'aif', 'aiff', 'mid', 'wma', 'ra', 'vqf', 'ape']
        video_list = ['wmv', 'asf', 'asx', 'rm', 'rmvb', 'mpg', 'mpeg', 'mpe', '3gp', 'mov', 'mp4', 'm4v', 'avi', 'dat', 'mkv', 'flv', 'vob']
        image_list = ['psd', 'pdd', 'gif', 'jpeg', 'png', 'pdf', 'bmp']

        ext = file.name.split('.')[-1]

        if ext in audio_list:
            file_type = '1'
        elif ext in video_list:
            file_type = '2'
        elif ext in image_list:
            file_type = '3'
        else:
            file_type = '0'

        obj = CourseFile.objects.create(
            course_id=course_id,
            file_type=file_type,
            file_name=file.name,
            upload_time=timezone.now,
            file_creator=user_id,
            file_menu=menu_id,
            file_status='0'
        )

        obj.course_file = file
        obj.save()

        return JsonResponse({'massage': '上传成功'}, safe=False)


def get(request):
    massage = {'err': '错误的访问方式'}
    return JsonResponse(massage, safe=False)


class DownloadCourseFile(View):
    """
    模块: 下载文件
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            file_id: 文件ID
    """

    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        file_id = request.POST.get('file_id')

        if not (token and course_id and file_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        files = CourseFile.objects.filter(course_id=course_id, file_id=file_id).first()
        if not files:
            massage = {'err': '文件不存在'}
            return JsonResponse(massage, safe=False)
        some_file = files.course_file
        some_file = open(some_file.path, "rb")

        return FileResponse(some_file)


class ChapterHome(View):
    """
    模块: 章节首页
    接口信息:
        GET:
            token: token认证
            course_id: 课程ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')

        if not (token and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        class_id = CourseClass.objects.filter(course_id=course_id, class_type=1).first().course_class
        classes = CourseClass.objects.filter(course_id=course_id).values('course_class')
        chapters = Chapter.objects.filter(course_id=course_id, pre_chapter=None).order_by('chapter_number')
        for course_class in classes:
            class_user = ClassUser.objects.filter(class_id=course_class).values('user_id')
            if user_id in class_user:
                class_id=course_class
                pass

        content = []
        for chapter in chapters:
            content.append({
                'chapter_id': chapter.chapter_id,
                'course_id': chapter.chapter_id,
                'chapter_title': chapter.chapter_title,
                'chapter_grade': chapter.chapter_grade,
                'chapter_number': chapter.chapter_number,
                'pre_chapter': chapter.pre_chapter,
                'create_time': chapter.create_time,
            })
            sections = Chapter.objects.filter(course_id=course_id, pre_chapter=chapter.chapter_id).order_by('chapter_number')
            for section in sections:
                chapter_class = ChapterClass.objects.filter(class_id=class_id, chapter_id=section.chapter_id, chapter_status=0).first()
                if not chapter_class:
                    content.append({
                        'chapter_id': section.chapter_id,
                        'course_id': section.chapter_id,
                        'chapter_title': section.chapter_title,
                        'chapter_grade': section.chapter_grade,
                        'chapter_number': section.chapter_number,
                        'pre_chapter': section.pre_chapter,
                        'create_time': section.create_time,
                    })

        return JsonResponse({'massage': content}, safe=False)

    def post(self, request):
        return JsonResponse({'err': '错误的访问方式'}, safe=False)


class ManagementChapter(View):
    """
    模块: 查看章节列表/隐藏章节
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')

        if not (token and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        users = CourseUser.objects.filter(course_id=course_id).values('course_user')
        if user_id not in users and identity not in [0, 1]:
            return JsonResponse({'err': '无权限'})

        content = []
        classes = CourseClass.objects.filter(course_id=course_id).values('course_class')
        chapters = Chapter.objects.filter(course_id=course_id, pre_chapter=None).order_by('chapter_number')

        for class_id in classes:
            the_class = Class.objects.filter(class_id=class_id).first()
            chapter_data = []
            for chapter in chapters:
                chapter_data.append({
                    'chapter_id': chapter.chapter_id,
                    'course_id': chapter.chapter_id,
                    'chapter_title': chapter.chapter_title,
                    'chapter_grade': chapter.chapter_grade,
                    'chapter_number': chapter.chapter_number,
                    'pre_chapter': chapter.pre_chapter,
                    'create_time': chapter.create_time,
                })
                sections = Chapter.objects.filter(course_id=course_id, pre_chapter=chapter.chapter_id).order_by('chapter_number')
                for section in sections:
                    chapter_class = ChapterClass.objects.filter(class_id=class_id, chapter_id=section.chapter_id, chapter_status=0).first()
                    if not chapter_class:
                        is_show = False
                    else:
                        is_show = True
                    chapter_data.append({
                        'chapter_id': section.chapter_id,
                        'course_id': section.chapter_id,
                        'chapter_title': section.chapter_title,
                        'chapter_grade': section.chapter_grade,
                        'chapter_number': section.chapter_number,
                        'pre_chapter': section.pre_chapter,
                        'create_time': section.create_time,
                        'is_show': is_show
                    })
            content.append({'class_name': the_class.class_name, 'chapter': chapter_data})
        
        return JsonResponse({'content': content})

    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        class_id = request.POST.get('class_id')
        chapter_id = request.POST.get('chapter_id')
        is_show = request.POST.get('is_show')

        if not (token and course_id and class_id and chapter_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        users = CourseUser.objects.filter(course_id=course_id).values('course_user')
        if user_id not in users:
            return JsonResponse({'err': '无权限'})
        
        chapter = ChapterClass.objects.filter(course_id=course_id, chapter_id=chapter_id).first()
        if not chapter:
            ChapterClass.objects.create(
                chapter_id=chapter_id,
                class_id=class_id,
                chapter_status='0',
                chapter_time=timezone.now
            )
        
        chapter.chapter_status = is_show
        chapter.save()
        
        return JsonResponse({'massage': '修改成功'})


class FreeChapter(View):
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        chapter_id = request.POST.get('chapter_id')
        is_free = request.POST.get('is_free')

        if not (token and course_id and chapter_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        course = Course.objects.filter(course_id=course_id).first()
        if course.course_creator != user_id:
            return JsonResponse({'err': '无权限'})
        
        chapter = Chapter.objects.filter(chapter_id=chapter_id).first()
        chapter.chapter_states = is_free
        chapter.save()

        return JsonResponse({'massage': '修改成功'})


class CreateChapter(View):
    """
    模块: 新建章节
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            chapter_title: 章节标题
            pre_chapter: 前置章节ID
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        chapter_title = request.POST.get('chapter_title')
        pre_chapter = request.POST.get('pre_chapter')

        if not (token and chapter_title):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        course_user = CourseUser.objects.filter(course_id=course_id, user_identity=0).values('course_user')
        if user_id not in course_user:
            return JsonResponse({'err': '身份不正确'})

        if pre_chapter:
            chapter = Chapter.objects.filter(chapter_id=pre_chapter).first()
            if chapter.pre_chapter:
                pre_chapter = chapter.pre_chapter

        chapter = Chapter.objects.create(
            course_id=course_id,
            chapter_title=chapter_title,
            pre_chapter=pre_chapter,
            create_time=timezone.now,
        )

        chapter_number = Chapter.objects.filter(course_id=course_id, chapter_id=pre_chapter).count()
        chapter.chapter_number = chapter_number
        chapter.save()

        return JsonResponse({'massage': '创建成功'}, safe=False)


class ModifyChapter(View):
    """
    模块: 修改章节
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            chapter_id: 章节ID
            chapter_title: 章节标题
    """
    def get(self, request):
        return JsonResponse({'err': '错误的访问方式'}, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        chapter_id = request.POST.get('chapter_id')
        chapter_title = request.POST.get('chapter_title')

        if not (token and chapter_title):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        course_user = CourseUser.objects.filter(course_id=course_id, user_identity=0).values('course_user')
        if user_id not in course_user:
            return JsonResponse({'err': '身份不正确'})
        
        chapter = Chapter.objects.filter(chapter_id=chapter_id).first()
        chapter.chapter_title = chapter_title
        chapter.save()

        return JsonResponse({'massage': '修改成功'}, safe=False)


class CourseAddStudent(View):
    """
        模块: 添加学生
            接口信息:
            GET:
                None
            POST:
                传参：token, course_id, real_name, cell_phone_number, student_number, course_name, class_name
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        real_name = request.POST.get('real_name')
        cell_phone_number = request.POST.get('cell_phone_number')
        student_number = request.POST.get('user_id')
        course_name = request.POST.get('course_name')
        class_name = request.POST.get('class_name')
        if not (token and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            massage = {'err': '未登录'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                massage = {'err': '用户不存在or用户信息未完善'}
                return JsonResponse(massage, safe=False)
        # 手动添加
        if student_number:
            user_name = User.objects.filter(user_id=student_number).values('user_name').first()
            user_name = user_name['user_name']
            if user_name != real_name:
                message = {'err': '用户姓名不匹配'}
                return JsonResponse(message, safe=False)
            else:
                CourseUser.objects.create(
                    course_id=course_id,
                    course_user=student_number,
                    user_identity='3',
                )
        if cell_phone_number:
            user_name = User.objects.filter(user_telephone=cell_phone_number).values('user_name').first()
            user_name = user_name['user_name']
            if user_name != real_name:
                message = {'err': '用户姓名不匹配'}
                return JsonResponse(message, safe=False)
            else:
                student_number = User.objects.filter(user_telephone=cell_phone_number).values('user_id').first()
                CourseUser.objects.create(
                    course_id=course_id,
                    course_user=student_number['user_id'],
                    user_identity='3',
                )
                message = {'err': '添加成功'}
                return JsonResponse(message, safe=False)
        # 课程班级添加
        if class_name:
            class_id = Class.objects.filter(class_name=class_name).values('class_id').first()
            class_id = class_id['class_id']
            course_id = CourseUser.objects.filter(course_class=class_id).values('course_id').first()
            course_id = course_id['course_id']
            if not course_id:
                message = {'err': '班级没有对应的课程'}
                return JsonResponse(message, safe=False)
            else:
                class_users = ClassUser.objects.filter(class_id=class_id).values('user_id')
                class_users = [item['user_id'] for item in class_users]
                course_name = Course.objects.filter(course_id=course_id).values('course_name').first()

                for data in class_users:
                    CourseUser.objects.create(
                        course_id=course_id,
                        course_user=data,
                        course_class=class_id,
                        user_identity='3',
                    )
                message = {'err': '添加成功'}
                return JsonResponse(message, safe=False)


class CourseAddTeacher(View):
    """
        模块: 添加老师
            接口信息:
            GET:
                None
            POST:
                传参：token, real_name, teacher_id, user_identity, course_id
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        real_name = request.POST.get("real_name")
        teacher_id = request.POST.get('teacher_id')
        user_identity = request.POST.get('user_identity')
        course_id = request.POST.get('course_id')
        if not (token and course_id and real_name and teacher_id and user_identity):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            massage = {'err': '未登录'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                massage = {'err': '用户不存在or用户信息未完善'}
                return JsonResponse(massage, safe=False)
        user_id = User.ojects.filter(user_name=real_name).values('user_id').first()
        user_id = user_id['user_id']
        if not user_id:
            message = {'err': '姓名用户不存在'}
            return JsonResponse(message, safe=False)
        elif user_id != teacher_id:
            message = {'err': '姓名用户不匹配'}
            return JsonResponse(message, safe=False)
        else:
            CourseUser.objects.create(
                course_id=course_id,
                course_user=teacher_id,
                user_identity=user_identity,
            )
            message = {'err': '添加成功'}
            return JsonResponse(message, safe=False)



# 课程批量导入学生  txt文件
class BatchImportStudents(View):
    """
    模块: 批量导入学生
    接口信息:
        GET:
            None
        POST:
            token:token认证
            course_id：课程ID
            file：文件
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POST.get('course_id')
        file = request.POST.get('file')
        if not token:
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            massage = {'err': '未登录'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                massage = {'err': '用户不存在or用户信息未完善'}
                return JsonResponse(massage, safe=False)
        '''
        excel_raw_data = pd.read_excel(request.FILES.get('file', ''), header=None)
        # 删除第一行的标题
        excel_raw_data.drop([0, 0], inplace=True)
        # 获取每列
        name = excel_raw_data.iloc[:, [0]]
        user_id = excel_raw_data.iloc[:, [1]]
        # 对每一列数据进行处理，从DataFrame类型转换为list类型
        name_list = name.values.tolist()
        user_id_list = user_id.values.tolist()
        # 对每一列的每一行的数据进行转换，转换为相应类型，保存在数据库中
        for i in range(len(name_list)):
            dct = {}
            dct['name'] = str(name_list[i][0])
            dct['user_id'] = int(str(user_id_list[i][0]))
            if all([dct['name'], dct['user_id']]):
                insertRes = CourseUser.objects.create(**dct)
                course_id = insertRes.course_id
        '''
        pf = 'D:\course1.'+'xlsx'
        df = pd.read_excel(pf, sheet_name='Sheet1', header=None)
        pf = 'D:\course1.'+'txt'
        df.to_csv(pf, header=None, sep=',', index=False)
        data_list = []
        with open(pf, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split(',')
                course = CourseUser(course_id=course_id, course_user=parts[0], user_identity=parts[1])
                data_list.append(course)
            CourseUser.objects.bulk_create(data_list)
        message = {'err': '添加成功'}
        return JsonResponse(message, safe=False)


class ChapterUp(View):
    """
    模块: 上调章节
    接口信息:
        POST:
            token: token认证
            chapter_id: 章节ID
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        chapter_id = request.POST.get('chapter_id')

        if not (token and chapter_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        chapter = Chapter.objects.filter(chapter_id=chapter_id).first()
        # chapters_number = Chapter.objects.filter(pre_chapter=chapter.pre_chapter).count()
        if chapter.chapter_number == 1:
            return JsonResponse({'err': '已经是最高'})

        next_chapter = Chapter.objects.filter(chapter_number=chapter.chapter_number-1, pre_chapter=chapter.pre_chapter).first()
        chapter.chapter_number = chapter.chapter_number - 1
        chapter.save()
        next_chapter.chapter_number = next_chapter.chapter_number + 1
        next_chapter.save()

        return JsonResponse({'massage': '修改成功'})


class ChapterDown(View):
    """
    模块: 下调章节
    接口信息:
        POST:
            token: token认证
            chapter_id: 章节ID
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        chapter_id = request.POST.get('chapter_id')

        if not (token and chapter_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        chapter = Chapter.objects.filter(chapter_id=chapter_id).first()
        chapters_number = Chapter.objects.filter(pre_chapter=chapter.pre_chapter).count()
        if chapter.chapter_number == chapters_number:
            return JsonResponse({'err': '已经是最低'})

        next_chapter = Chapter.objects.filter(chapter_number=chapter.chapter_number+1, pre_chapter=chapter.pre_chapter).first()
        chapter.chapter_number = chapter.chapter_number + 1
        chapter.save()
        next_chapter.chapter_number = next_chapter.chapter_number - 1
        next_chapter.save()

        return JsonResponse({'massage': '修改成功'})


class CreateChapterContent(View):
    """
    模块: 显示章节内容/创建章节内容
    接口信息:
        GET:
            token: token认证
            chapter_id: 章节ID
        POST:
            token: token认证
            course_id: 课程ID
            chapter_id: 章节ID
            chapter_content_title: 章节内容标题
            chapter_content: 章节内容
    """
    def get(self, request):
        token = request.GET.get('token')
        chapter_id = request.GET.get('chapter_id')

        if not (token and chapter_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            massage = {'err': '未登录'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                massage = {'err': '用户不存在or用户信息未完善'}
                return JsonResponse(massage, safe=False)

        contents = ChapterContent.objects.filter(chapter_id=chapter_id)
        if not contents:
            return JsonResponse({'err': '此页不存在'}, safe=False)
        
        content_data = []
        for content in contents:
            content_data.append({
                'chapter_id': content.chapter_id,
                'chapter_content_title': content.chapter_content_title,
                'chapter_content': content.chapter_content,
                'chapter_creator': content.chapter_creator,
                'create_time': content.create_time,
            })

        return JsonResponse({'massage': content_data}, safe=False)

    def post(self, rquest):
        token = request.POST.get('token')
        course_id = request.POSt.get('course_id')
        chapter_id = request.POST.get('chapter_id')
        chapter_content_title = request.POST.get('chapter_content_title')
        chapter_content = request.POST.get('chapter_content')

        if not (token and chapter_id and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        users = CourseUser.objects.filter(course_id=course_id, user_identity='0').values('course_user')
        if user_id not in users:
            return JsonResponse({'err': '无权限'}, safe=False)
        
        ChapterContent.objects.create(
            chapter_id=chapter_id,
            chapter_content_title=chapter_content_title,
            chapter_content=chapter_content,
            chapter_creator=user_id,
            create_time=timezone.now
        )
        
        return JsonResponse({'massage': '创建成功'}, safe=False)

    
class ModifyChapterContent(View):
    """
    模块: 修改章节内容
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            chapter_id: 章节ID
            chapter_content_id: 章节内容ID
            chapter_content_title: 章节内容标题
            chapter_content: 章节内容
    """
    def get(self, request):
        return JsonResponse({'err': '错误的访问方式'}, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POSt.get('course_id')
        chapter_id = request.POST.get('chapter_id')
        chapter_content_id = request.POST.get('chapter_content_id')
        chapter_content_title = request.POST.get('chapter_content_title')
        chapter_content = request.POST.get('chapter_content')

        if not (token and chapter_id and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        users = CourseUser.objects.filter(course_id=course_id, user_identity='0').values('course_user')
        if user_id not in users:
            return JsonResponse({'err': '无权限'}, safe=False)

        content = ChapterContent.objects.filter(chapter_content_id=chapter_content_id).first()
        content.chapter_content_title = chapter_content_title
        content.chapter_content = chapter_content
        content.save()

        return JsonResponse({'massage': '修改成功'}, safe=False)


class DeleteChapterContent(View):
    """
    模块: 删除章节内容
    接口信息:
        POST:
            token: token认证
            course_id: 课程ID
            chapter_id: 章节ID
            chapter_content_id: 章节内容ID
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        course_id = request.POSt.get('course_id')
        chapter_id = request.POST.get('chapter_id')
        chapter_content_id = request.POST.get('chapter_content_id')

        if not (token and chapter_id and course_id):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)

        users = CourseUser.objects.filter(course_id=course_id, user_identity='0').values('course_user')
        if user_id not in users:
            return JsonResponse({'err': '无权限'}, safe=False)

        content = ChapterContent.objects.filter(chapter_content_id=chapter_content_id).first()
        content.delete()

        return JsonResponse({'massage': '删除成功'}, safe=False)     


class getCourseClass(View):
    """
            模块: 消息广播 获取当前课程的班级信息
            接口信息:
            GET:
            token，course_id
                返回相应的班级列表信息和教师团队信息
            POST:
                传参：class_id,token，course_id
                返回该课程班级的所有班级成员
        """
    def get(self,request):
        course_id = int(request.GET.get('course_id',0))
        token = request.GET.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        capacity = publicMethod.get_user_capacity(token)
        user_id = publicMethod.check_user_login(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission', 'data': []})
        data = []


        pass



    def post(self,request):
        pass

class GetCourseInfo(View):
    """
    模块: 老师获取班级老师信息
    接口信息:
        GET:
            token: token认证
            course_id: 课程ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')

        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'err': '信息未完善'})

        class_data = []
        classes = CourseClass.objects.filter(course_id=course_id)
        for it in classes:
            other = Class.objects.filter(class_id=it.course_class).first()
            class_data.append({
                'class_id': other.course_class,
                'class_name': other.class_name,
            })

        user_data = []
        users = CourseUser.objects.filter(course_id=course_id)
        for it in users:
            user = User.objects.filter(user_id=it.course_user)
            user_data.append({
                'user_id': user.user_id,
                'user_nick': user.user_nick,
            })

        return JsonResponse({'class': class_data, 'user': user_data}, safe=False)

    def post(self, request):
        JsonResponse({'err': '错误的访问方式'})
    

class GetClassInfo(View):
    """
    模块: 老师获取自己班级信息
    接口信息:
        GET:
            token: token认证
            course_id: 课程ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')

        user_id = publicMethod.check_user_login(token)
        identity = publicMethod.get_user_capacity(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'err': '信息未完善'})
            
        course = Course.objects.filter(course_id=course_id).first()
        if user_id == course.course_creator or identity in [0, 1]:
            user_class = UserClass.objects.filter(course_id=course_id)
        else:
            user_class = UserClass.objects.filter(course_id=course_id, course_user = user_id)
        
        class_data = []
        user_data = []
        for it in user_class:
            classes = Class.objects.filter(class_id=it.course_class).first()
            users = ClassUser.objects.filter(class_id=it.course_class, user_type=0)
            class_data.append({
                'class_id': classes.class_id,
                'class_name': classes.class_name,
                'class_introduce': classes.class_introduce,
                'create_time': classes.create_time,
                'class_creator': classes.class_creator,
                'users_num': users.count(),
            })
            data = []
            for j in users:
                user = User.objects.filter(user_id=j.user_id).first()
                data.append({
                    'user_id': user.user_id,
                    'user_name': user.user_name,
                    'user_nick': user.user_nick,
                    'add_time': j.add_time,
                    'user_school': user.user_school,
                })
            user_data.append(data)
        
        return JsonResponse({'class': class_data, 'user': user_data}, safe=False)

    def post(self, request):
        JsonResponse({'err': '错误的访问方式'})


class ViewTeachCourse(View):
    """
    模块: 查看我教的课程
    接口信息:
        GET:
            token:token认证
            user_id：用户账号
        POST:
            massage:搜寻结果
    """
    def get(self,request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        rank_data = []
        classes = ClassUser.objects.filter(Q(user_id=user_id) & (Q(user_type='1') | Q(user_type='2')))
        for item in classes:
            course_idd = CourseClass.objects.get(course_class=item.class_id)
            course = Course.objects.filter(course_id=course_idd.course_id)
            for iteem in course:
                rank_data.append(
                    {
                        'course_id': iteem.course_id,
                        'course_name': iteem.course_name,
                        'course_introduce': iteem.course_introduce,
                        'course_cover': str(iteem.course_cover),
                        'create_time': iteem.create_time,
                        'course_cost': iteem.course_cost,
                        'course_creator': iteem.course_creator,
                        'course_status': iteem.course_status,
                        'course_browse': iteem.course_browse
                    }
                )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)

    def post(self,request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class JoinCourse(View):
    """
    模块: 学生加入课程
    接口信息:
        GET:
            token:token认证
            invitation_code:邀请码
            course_id：课程编号
            course_status:课程状态
            payment_results:支付结果
            user_id：用户账号
        POST:
            massage:加入结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        invitation_code = request.POST.get('invitation_code')
        course_status = request.POST.get('course_status')
        course_id = request.POST.get('course_id')
        payment_results = request.POST.get('payment_results')
        classes = CourseClass.objects.get(Q(course_id=course_id) & Q(class_type='1'))
        class_id = classes.course_class
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        if not course_id:
            return JsonResponse({'err': '信息不完全'}, safe=False)
        if not course_status:
            return JsonResponse({'err': '信息不完全'}, safe=False)
        if course_status != '1' and course_status != '3':
            return JsonResponse({'err': '添加失败，该课程不能加入'}, safe=False)
        if invitation_code == "":
            invitation_code = None
        if not invitation_code:
            if course_status == '3':
                if payment_results == '1':
                    ClassUser.objects.create(
                        class_id=class_id,
                        user_id=user_id,
                        user_type='0',
                        add_time=datetime.datetime.now(),
                        add_type='1',
                    )
                    return JsonResponse({'massage': '添加成功'}, safe=False)
                else:
                    return JsonResponse({'err': '添加失败，请完成支付'}, safe=False)
            else:
                ClassUser.objects.create(
                    class_id=class_id,
                    user_id=user_id,
                    user_type='0',
                    add_time=datetime.datetime.now(),
                    add_type='1',
                )
                return JsonResponse({'massage': '添加成功'}, safe=False)
        else:
            classes = Class.objects.get(class_invitation=invitation_code)
            ClassUser.objects.create(
                class_id=classes.class_id,
                user_id=user_id,
                user_type='0',
                add_time=datetime.datetime.now(),
                add_type='0',
            )
            return JsonResponse({'massage': '添加成功'}, safe=False)

class CourseHome(View):
    def get(self, request):
        course = Course.objects.filter().all().order_by('course_id')
        course_data = []
        for data in course:
            create_time = Course.objects.filter(course_id=data.course_id).values('create_time').first()
            create_time = create_time['create_time']
            create_time = datetime.datetime.strftime(create_time, '%Y-%m-%d %H:%M:%S')
            course_data.append(
                {
                    'course_id': data.course_id,
                    'course_name': data.course_name,
                    'course_introduce': data.course_introduce,
                    'course_cover': str(data.course_cover),
                    'create_time': create_time,
                    'course_cost': data.course_cost,
                    'course_creator': data.course_creator,
                    'course_status': data.course_status,
                    'course_browse': data.course_browse,
                }
            )
        return JsonResponse({'status': 'Ture', 'course': course_data})


class CreateClass(View):
    """
    模块: 创建班级
    接口信息:
        GET:
            token:token认证
            use_id:创建者
            course_id：课程编号
            class_name:班级名称
            class_introduce:班级介绍
            create_time：创建时间
            class_type：班级类型
            class_college：班级所在学院
            class_invitation：班级邀请码
        POST:
            massage:创建结果
    """
    def get(self,request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        class_name = request.POST.get('class_name')
        class_introduce = request.POST.get('class_introduce')
        create_time = request.POST.get('create_time')
        class_type = request.POST.get('class_type')
        class_college = int(request.POST.get('class_college'))
        class_invitation = request.POST.get('class_invitation')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        if not course_id:
            return JsonResponse({'status': False, 'err': '信息不完全'})
        if not class_name or not user_id or not class_type:
            return JsonResponse({'status': False, 'err': '信息不完全'})
        else:
            Class.objects.create(
                class_name=class_name,
                class_creator=user_id,
                create_time=create_time,
                class_introduce=class_introduce,
                class_type=class_type,
                class_college=class_college,
                class_invitation=class_invitation
            )
        classes = Class.objects.get(Q(class_name=class_name) & Q(class_creator=user_id) & Q(class_introduce=class_introduce))
        if class_type != '3':
            class_type = '0'
        CourseClass.objects.create(
            course_id=course_id,
            course_class=classes.class_id,
            class_type=class_type
        )
        UserClass.objects.create(
            course_id=course_id,
            course_user=user_id,
            course_class=classes.class_id
        )
        return JsonResponse({'massage': '创建成功'}, safe=False)


class ViewCourseChapter(View):
    """
    模块: 查看课程章节
    接口信息:
        GET:
            token:token认证
            user_id:用户账号
            course_id：课程编号
        POST:
            massage:课程章节
    """
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.GET.get('course_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        if not course_id:
            return JsonResponse({'status': False, 'err': '信息不完全'})
        classes = CourseClass.objects.filter(course_id=course_id).all()
        for item in classes:
            classes_id = ClassUser.objects.get(Q(class_id=item.course_class) & Q(user_id=user_id))
            if classes_id:
                break
        chapters = ChapterClass.objects.filter(class_id=classes_id.class_id)
        rank_data = []
        for item in chapters:
            chapter = Chapter.objects.get(chapter_id=item.chapter_id)
            chapter_content = ChapterContent.objects.get(chapter_id=item.chapter_id)
            chapter_status = ChapterUser.objects.get(chapter_id=item.chapter_id)
            rank_data.append(
                {
                    'chapter_id': chapter.chapter_id,
                    'course_id': chapter.course_id,
                    'chapter_title': chapter.chapter_title,
                    'chapter_grade': chapter.chapter_grade,
                    'pre_chapter': chapter.pre_chapter,
                    'create_time': chapter.create_time,
                    'chapter_states': chapter.chapter_states,
                    'chapter_content': chapter_content.chapter_content,
                    'chapter_number': chapter_content.chapter_number,
                    'chapter_creator': chapter_content.chapter_creator,
                    'chapter_status': item.chapter_status,
                    'chapter_time': item.chapter_time,
                    'status': chapter_status.status
                }
            )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class ViewJoinCourse(View):
    """
    模块: 查看参加课程
    接口信息:
        GET:
            token:token认证
            user_id:用户账号
        POST:
            massage:课程信息
    """
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        rank_data = []
        classes = ClassUser.objects.filter(user_id=user_id, user_type='0')
        for item in classes:
            courses = CourseClass.objects.get(course_class=item.class_id)
            course = Course.objects.get(course_id=courses.course_id)
            rank_data.append(
                {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_introduce': course.course_introduce,
                    'course_cover': str(course.course_cover),
                    'create_time': course.create_time,
                    'course_cost': course.course_cost,
                    'course_creator': course.course_creator,
                    'course_status': course.course_status,
                    'course_browse': course.course_browse
                }
            )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class ViewCourseAssignment(View):
    """
    模块：查看课程作业/考试
    接口信息：
        GET：
            token：token认证
            user_id:用户账号
            course_id:课程ID
            class_id:班级ID
        POST：
            massage:结果列表
    """
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.GET.get('course_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登入'})
        if not course_id:
            return JsonResponse({'status': False, 'err': '信息不完全'})
        classes = CourseClass.objects.filter(course_id=course_id)
        classes_id = None
        for item in classes:
            classes_id = ClassUser.objects.get(class_id=item.course_class, user_id=user_id)
            if classes_id:
                break
        if not classes_id:
            return JsonResponse({'err': '无数据'}, safe=False)
        task = Task.objects.filter(task_class=classes_id.class_id)
        rank_data = []
        for item in task:
            rank_data.append(
                {
                    'task_id': item.task_id,
                    'task_title': item.task_title,
                    'task_explain': item.task_explain,
                    'task_creator': item.task_creator,
                    'create_time': item.create_time,
                    'task_type': item.task_type,
                    'begin_time': item.begin_time,
                    'end_time': item.end_time,
                    'task_status': item.task_status,
                    'task_judge': item.task_judge,
                    'task_chapter': item.task_chapter,
                    'task_course': item.task_course,
                    'task_class': item.task_class
                }
            )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class ViewAllCourse(View):
    """
    模块：查看所有课程
    接口信息：
        GET:
            None
        POST:
            massage:课程列表
    """
    def get(self, request):
        rank_data = []
        courses = Course.objects.all()
        for item in courses:
            rank_data.append(
                {
                    'course_id': item.course_id,
                    'course_name': item.course_name,
                    'course_introduce': item.course_introduce,
                    'course_cover': str(item.course_cover),
                    'create_time': item.create_time,
                    'course_cost': item.course_cost,
                    'course_creator': item.course_creator,
                    'course_status': item.course_status,
                    'course_browse': item.course_browse
                }
            )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)


    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class ModifyCourseIntroduction(View):
    """
    模块：修改课程介绍
    接口信息：
        GET:
            token:token认证
            user_id:用户账号
            course_id:课程ID
            introduction:修改内容
        POST：
            massage:修改结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        introduction = request.POST.get('introduction')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not (course_id and introduction):
            return JsonResponse({'status': False, 'err': '信息不完全'})
        user_identity = CourseUser.objects.filter(course_id=course_id, course_user=user_id, user_identity='0')
        if not user_identity:
            return JsonResponse({'status': False, 'err': '无权限'})
        else:
            for item in user_identity:
                course = Course.objects.get(course_id=item.course_id)
                course.course_introduce = introduction
                course.save()
            massage = {'pass': 'modify succeeded'}
        return JsonResponse(massage, safe=False)


class ViewClassList(View):
    """
    模块：查看班级列表
    接口信息：
        GET:
            token：token认证
            user_id:用户账号
            course_id:课程ID
        POST:
            massage：班级列表
    """
    def get(self, request):
        token = request.GET.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.GET.get('course_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not course_id:
            return JsonResponse({'err': '信息不完全'})
        jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & (Q(user_identity='0') | Q(user_identity='1')))
        if not jurisdiction:
            return JsonResponse({'err': '无权限'})
        rank_data = []
        classes = CourseClass.objects.filter(course_id=course_id)
        for item in classes:
            classed = Class.objects.get(class_id=item.course_class)
            rank_data.append(
                {
                    'class_id': classed.class_id,
                    'class_name': classed.class_name,
                    'class_creator': classed.class_creator,
                    'create_time': classed.create_time,
                    'class_introduce': classed.class_introduce,
                    'class_type': classed.class_type,
                    'class_college': classed.class_college,
                    'class_invitation': classed.class_invitation
                }
            )
        massage = {'massage': rank_data}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class DeleteClassPersonnel(View):
    """
    模块：删除班级人员
    接口信息：
        GET:
            token:token认证
            user_id:用户账号
            course_id:课程ID
            delete_id:删除人员ID
        POST:
            massage:删除结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        delete_id = request.POST.get('delete_id')
        class_id = request.POST.get('class_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not (course_id and delete_id and class_id):
            return JsonResponse({'err': '信息不完全'})
        if user_id == delete_id:
            return JsonResponse({'err': '无法删除自己'})
        creater = Course.objects.get(course_id=course_id)
        if user_id == str(creater.course_creator):
            course_user = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=delete_id))
            if not course_user:
                return JsonResponse({'err': '删除用户不存在'})
            for item in course_user:
                if str(item.user_identity) == '0' or str(item.user_identity) == '1':
                    user_class = UserClass.objects.filter(Q(course_id=course_id) & Q(course_user=delete_id) & Q(course_class=class_id))
                    user_class.delete()
                else:
                    object_id = ClassUser.objects.filter(Q(class_id=class_id) & Q(user_id=delete_id))
                    object_id.delete()
                    course_user.delete()
            massage = {'pass': 'Delete Success'}
        else:
            jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & Q(user_identity='0'))
            if not jurisdiction:
                return JsonResponse({'err': '无权限'})
            course_user = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=delete_id))
            if not course_user:
                return JsonResponse({'err': '删除用户不存在'})
            for item in course_user:
                if str(item.user_identity) == '0':
                    return JsonResponse({'err': '无权限'})
                elif str(item.user_identity) == '1':
                    user_class = UserClass.objects.filter(Q(course_id=course_id) & Q(course_user=delete_id) & Q(course_class=class_id))
                    user_class.delete()
                else:
                    object_id = ClassUser.objects.filter(Q(class_id=class_id) & Q(user_id=delete_id))
                    object_id.delete()
                    course_user.delete()
            massage = {'pass': 'Delete Success'}
        return JsonResponse(massage, safe=False)


class AddAssistantTeacher(View):
    """
    模块：添加助教和协同老师
    接口信息：
        GET：
            token:token认证
            user_id:用户账号
            course_id:课程ID
            object_id:对象ID
            user_identity:用户身份
        POST：
            massage：操作结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        object_id = request.POST.get('object_id')
        user_identity = request.POST.get('user_identity')
        class_id = request.POST.get('class_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not (course_id and object_id and user_identity):
            return JsonResponse({'err': '信息不完全'})
        if user_id == object_id:
            return JsonResponse({'err': '无法添加自己'})
        jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & Q(user_identity='0'))
        if not jurisdiction:
            return JsonResponse({'err': '无权限'})
        if not class_id:
            existence = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=object_id))
            if existence:
                return JsonResponse({'err': '对象已存在'})
            else:
                CourseUser.objects.create(
                    course_id=course_id,
                    course_user=object_id,
                    user_identity=user_identity
                )
        else:
            classes = CourseClass.objects.filter(course_id=course_id)
            belong = '0'
            for item in classes:
                if class_id == str(item.course_class):
                    belong = '1'
                    break
            if belong == '0':
                return JsonResponse({'err': '该班级不属于该课程'})
            existence = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=object_id))
            if existence:
                exist = UserClass.objects.filter(Q(course_id=course_id) & Q(course_user=object_id) & Q(course_class=class_id))
                if exist:
                    return JsonResponse({'err': '对象已存在'})
                else:
                    UserClass.objects.create(
                        course_id=course_id,
                        course_user=object_id,
                        course_class=class_id
                    )
            else:
                CourseUser.objects.create(
                    course_id=course_id,
                    course_user=object_id,
                    user_identity=user_identity
                )
                UserClass.objects.create(
                    course_id=course_id,
                    course_user=object_id,
                    course_class=class_id
                )
        massage = {'pass': 'Add succeed'}
        return JsonResponse(massage, safe=False)


class DeleteAssistantTeacher(View):
    """
    模块：删除助教和协同老师
    接口信息：
        GET:
            token:token认证
            user_id:用户账号
            course_id:课程ID
            object_id:对象ID
        POST:
            massage：操作结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        object_id = request.POST.get('object_id')
        class_id = request.POST.get('class_id')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not (course_id and object_id):
            return JsonResponse({'err': '信息不完全'})
        if user_id == object_id:
            return JsonResponse({'err': '无法删除自己'})
        jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & Q(user_identity='0'))
        if not jurisdiction:
            return JsonResponse({'err': '无权限'})
        if not class_id:
            existence = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=object_id))
            if not existence:
                return JsonResponse({'err': '对象不存在'})
            else:
                existence.delete()
                exist = UserClass.objects.filter(course_id=course_id, course_user=object_id)
                exist.delete()
        else:
            classes = CourseClass.objects.filter(course_id=course_id)
            belong = '0'
            for item in classes:
                if class_id == str(item.course_class):
                    belong = '1'
                    break
            if belong == '0':
                return JsonResponse({'err': '该班级不属于该课程'})
            existence = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=object_id))
            if existence:
                exist = UserClass.objects.filter(Q(course_id=course_id) & Q(course_user=object_id) & Q(course_class=class_id))
                if exist:
                    exist.delete()
                else:
                    return JsonResponse({'err': '删除对象不存在'})
            else:
                return JsonResponse({'err': '删除对象不存在'})
        return JsonResponse({'pass': 'delete succeed'})


class ReleaseHomeworkTest(View):
    """
    模块：发布作业/考试
    接口信息：
        GET：
            token：token认证
            user_id:用户账号
            course_id:课程ID
            task_title：作业标题
            task_explain：作业描述
            task_creator：作业创建者
            create_time：创建时间
            task_type：作业类型
            begin_time：开始时间
            end_time：结束时间
            task_status：作业状态
            task_judge：是否自动判题
            task_chapter：所属章节
            task_course：所属课程
            task_class：所属班级
        POST：
            massage:发布结果
    """
    def get(self, request):
        massage = {'status': False, 'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        task_title = request.POST.get('task_title')
        task_explain = request.POST.get('task_explain')
        task_creator = request.POST.get('task_creator')
        task_type = request.POST.get('task_type')
        begin_time = request.POST.get('task_title')
        end_time = request.POST.get('end_time')
        task_status = request.POST.get('task_status')
        task_judge = request.POST.get('task_judge')
        task_chapter = request.POST.get('task_chapter')
        task_course = request.POST.get('task_course')
        task_class = request.POST.get('task_class')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not (course_id and task_type and task_status and task_judge and task_class):
            return JsonResponse({'err': '信息不完全'})
        creater = Course.objects.get(course_id=course_id)
        if user_id == str(creater.course_creator):
            Task.objects.create(
                task_title=task_title,
                task_explain=task_explain,
                task_creator=task_creator,
                task_type=task_type,
                begin_time=begin_time,
                end_time=end_time,
                task_status=task_status,
                task_judge=task_judge,
                task_chapter=task_chapter,
                task_course=task_course,
                task_class=task_class
            )
            massage = {'pass': 'release success'}
        else:
            jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & Q(user_identity='0'))
            if not jurisdiction:
                return JsonResponse({'err': '无权限'})
            user_class = UserClass.objects.filter(course_id=course_id, course_user=user_id)
            if not user_class:
                Task.objects.create(
                    task_title=task_title,
                    task_explain=task_explain,
                    task_creator=task_creator,
                    task_type=task_type,
                    begin_time=begin_time,
                    end_time=end_time,
                    task_status=task_status,
                    task_judge=task_judge,
                    task_chapter=task_chapter,
                    task_course=task_course,
                    task_class=task_class
                )
                massage = {'pass': 'release success'}
            else:
                if task_class == '0':
                    return JsonResponse({'err': '无权限'})
                else:
                    for item in user_class:
                        if task_class == str(item.course_class):
                            Task.objects.create(
                                task_title=task_title,
                                task_explain=task_explain,
                                task_creator=task_creator,
                                task_type=task_type,
                                begin_time=begin_time,
                                end_time=end_time,
                                task_status=task_status,
                                task_judge=task_judge,
                                task_chapter=task_chapter,
                                task_course=task_course,
                                task_class=task_class
                            )
                            massage = {'pass': 'release success'}
                            break
                        else:
                            massage = {'err': '无权限'}
        return JsonResponse(massage, safe=False)


class ModifyHomeworkTest(View):
    """
    模块：修改作业/考试
    接口信息：
        GET:
            token：token认证
            user_id:用户账号
            course_id:课程ID
            begin_time：开始时间
            end_time：结束时间
            question_type：问题类型
            question_id：问题编号
            question_number：问题序号
            question_score：问题分数
        POST：
            massage:修改结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        course_id = request.POST.get('course_id')
        task_id = request.POST.get('task_id')
        begin_time = request.POST.get('begin_time')
        end_time = request.POST.get('end_time')
        question_type = request.POST.get('question_type')
        question_id = request.POST.get('question_id')
        question_number = request.POST.get('question_number')
        question_score = request.POST.get('question_score')
        question_description = request.POST.get('question_description')
        question_option = request.POST.get('question_option')
        question_answer = request.POST.get('question_answer')
        question_course = request.POST.get('question_course')
        question_change = request.POST.get('question_change')
        upload_user = request.POST.get('upload_user')
        upload_time = request.POST.get('upload_time')
        question_status = request.POST.get('question_status')
        belong_menu = request.POST.get('belong_menu')
        if not user_id:
            return JsonResponse({'status': False, 'err': '未登录'})
        if not task_id:
            return JsonResponse({'err': '信息不完全'})
        if not ((begin_time and end_time) or (question_type and question_id and question_number and question_score)):
            return JsonResponse({'err': '信息不完全'})
        if not (question_description and question_option and question_option and question_answer and question_course and question_change and upload_user and upload_time and question_status and belong_menu):
            return JsonResponse({'err': '信息不完全'})
        jurisdiction = CourseUser.objects.filter(Q(course_id=course_id) & Q(course_user=user_id) & Q(user_identity='0'))
        if not jurisdiction:
            return JsonResponse({'err': '无权限'})
        data = Task.objects.get(task_id=task_id)
        data.begin_time = begin_time
        data.end_time = end_time
        data.save()
        date = TaskQuestion.objects.get(task_id=task_id, question_id=question_id)
        date.question_type = question_type
        date.question_number = question_number
        date.question_score = question_score
        date.save()
        question = Question.objects.get(question_id=question_id)
        question.question_description = question_description
        question.question_type = question_type
        question.question_option = question_option
        question.question_answer = question_answer
        question.question_course = question_course
        question.question_change = question_change
        question.upload_user = upload_user
        question.upload_time = upload_time
        question.question_status = question_status
        question.belong_menu = belong_menu
        question.save()
        massage = {'pass': 'modify success'}
        return JsonResponse(massage, safe=False)

class StudentCourseHome(View):
    """
    模块：学生课程章节列表
    接口信息：
        GET:
            token:token认证
            course_id:课程ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        class_id = -1
        classes = CourseClass.objects.filter(course_id=course_id).values("class_id")
        for classs in classes:
            user = ClassUser.objects.filter(class_id = classs, user_id=user_id).first()
            if user:
                class_id = classs
                break
        
        if class_id == -1:
            return JsonResponse({'err': '未加入课程'}, safe=False)
        
        chapters = Chapter.objects.filter(course_id=course_id, pre_chapter=None).order_by('chapter_number')
        content = []
        for chapter in chapters:
            content.append({
                'chapter_id': chapter.chapter_id,
                'course_id': chapter.chapter_id,
                'chapter_title': chapter.chapter_title,
                'chapter_grade': chapter.chapter_grade,
                'chapter_number': chapter.chapter_number,
                'pre_chapter': chapter.pre_chapter,
                'create_time': chapter.create_time,
            })

            content_data = []
            sections = Chapter.objects.filter(course_id=course_id, pre_chapter=chapter.chapter_id).order_by('chapter_number')
            for section in sections:
                chapter_class = ChapterClass.objects.filter(class_id=class_id, chapter_id=section.chapter_id).first()
                it = ChapterClass.objects.filter(chapter_id=section.chapter_id, class_id=class_id, chapter_status=0).first()
                if it:
                    continue
                content_num = ChapterContent.objects.filter(chapter_id=section.chapter_id).count()
                study_num = ChapterUser.objects.filter(chapter_id=section.chapter_id, user_id=user_id, status=1).count()
                if not chapter_class:
                    content_data.append({
                        'chapter_id': section.chapter_id,
                        'course_id': section.chapter_id,
                        'chapter_title': section.chapter_title,
                        'chapter_grade': section.chapter_grade,
                        'chapter_number': section.chapter_number,
                        'pre_chapter': section.pre_chapter,
                        'create_time': section.create_time,
                        'study_num': content_num - study_num,
                    })
            content.append({chapter.chapter_id: content_data})
        
        return JsonResponse({'massage': content}, safe=False)
        

class TeacherCourseHome(View):
    """
    模块：老师课程章节列表
    接口信息：
        GET:
            token:token认证
            course_id:课程ID
            class_id:班级ID
    """
    def get(self, request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id')
        class_id = request.GET.get('class_id')

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            return JsonResponse({'err': '未登录'}, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'err': '用户不存在or用户信息未完善'}, safe=False)
        
        teacher = CourseUser.objects.filter(course_id=course_id, course_user=user_id).first
        if not teacher:
            return JsonResponse({'err': '不在课程中当老师'}, safe=False)
        
        # user_class = UserClass.objects.filter(course_id=course_id, course_user=user_id).values('course_class')
        # if class_id not in user_class:
        #     return JsonResponse({'err': '该班级不在此用户的管辖范围内'})
        
        chapters = Chapter.objects.filter(course_id=course_id, pre_chapter=None).order_by('chapter_number')
        content = []
        for chapter in chapters:
            content.append({
                'chapter_id': chapter.chapter_id,
                'course_id': chapter.chapter_id,
                'chapter_title': chapter.chapter_title,
                'chapter_grade': chapter.chapter_grade,
                'chapter_number': chapter.chapter_number,
                'pre_chapter': chapter.pre_chapter,
                'create_time': chapter.create_time,
            })

            content_data = []
            sections = Chapter.objects.filter(course_id=course_id, pre_chapter=chapter.chapter_id).order_by('chapter_number')
            for section in sections:
                chapter_class = ChapterClass.objects.filter(class_id=class_id, chapter_id=section.chapter_id).first()
                student_num = ClassUser.objects.filter(class_id=class_id).count()
                content_num = ChapterContent.objects.filter(chapter_id=section.chapter_id).count()
                study_num = ChapterUser.objects.filter(chapter_id=section.chapter_id, status=1).count()
                if not chapter_class:
                    content_data.append({
                        'chapter_id': section.chapter_id,
                        'course_id': section.chapter_id,
                        'chapter_title': section.chapter_title,
                        'chapter_grade': section.chapter_grade,
                        'chapter_number': section.chapter_number,
                        'pre_chapter': section.pre_chapter,
                        'create_time': section.create_time,
                        'study_num': study_num / (student_num * content_num) * 100,
                    })
            content.append({chapter.chapter_id: content_data})
        
        return JsonResponse({'massage': content}, safe=False)


class ViewCourseAssignmentExam(View):
    """
    模块：查看课程作业/考试
    接口信息：
        GET：
            token：token认证
            task_course:所属课程
            task_class：所属班级
        POST：
            massage：信息列表
    """
    def get(self, request):
        token = request.GET.get('token')
        task_course = request.GET.get('task_course')
        task_class = request.GET.get('task_class')
        if not token:
            return JsonResponse({'err': '用户未登录'})
        if not (task_course and task_class):
            return JsonResponse({'err': '信息不完全'})
        task = Task.objects.filter(task_course=task_course, task_class=task_class)
        rank_data = []
        for item in task:
            rank_data.append(
                {
                    'task_id': item.task_id,
                    'task_title': item.task_title,
                    'task_explain': item.task_explain,
                    'task_creator': item.task_creator,
                    'create_time': item.create_time,
                    'task_type': item.task_type,
                    'begin_time': item.begin_time,
                    'end_time': item.end_time,
                    'task_status': item.task_status,
                    'task_judge': item.task_judge,
                    'task_chapter': item.task_chapter,
                    'task_course': item.task_course,
                    'task_class': item.task_class,
                }
            )
        massage = {'rank': rank_data}
        return JsonResponse(massage, safe=False)


    def post(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)


class SubmitJob(View):
    """
    模块：提交作业
    接口信息：
        GET:
            token:token认证
            user_id:用户账号
            task_id:作业编号
            create_time：提交时间
            use_time：花费时间
            submit_content：提交答案|json格式存储
            submit_score：作业分数
            submit_ip：提交ip地址
            judge_time：判题时间
            judge_user：判题者
        POST:
            massage:提交结果
    """
    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        user_id = publicMethod.check_user_login(token)
        task_id = request.POST.get('task_id')
        create_time = request.POST.get('create_time')
        use_time = request.POST.get('use_time')
        submit_content = request.POST.get('submit_content')
        submit_score = request.POST.get('submit_score')
        submit_ip = request.POST.get('submit_ip')
        judge_user = request.POST.get('judge_user')
        if not token:
            return JsonResponse({'err': '未登录'})
        if not (task_id and create_time and use_time and submit_content and submit_score and submit_ip and judge_user):
            return JsonResponse({'err': '信息不完全'})
        TaskSubmit.objects.create(
            task_id=task_id,
            task_user=user_id,
            create_time=create_time,
            use_time=use_time,
            submit_content=submit_content,
            submit_score=submit_score,
            submit_ip=submit_ip,
            judge_user=judge_user
        )
        massage = {'massage': 'pass'}
        return JsonResponse(massage, safe=False)