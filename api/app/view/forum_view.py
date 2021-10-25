from django.http import JsonResponse
from django.views.generic import View
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.RoleMethod.PublicMethod import PublicMethod
from app.RoleMethod.SensitiveWordCheck import SensitiveWordCheck
from app.models import *
import numpy

publicMethod = PublicMethod()
sensitiveWordCheck = SensitiveWordCheck()


class CreateForum(View):
    """
        模块: 创建论坛
        接口信息:
        GET:
        POST:
            token: token认证
            forum_title: 标题
            forum_content: 内容
            forum_section: 板块类型
            section_id: 板块编号
    """

    def get(self, request):
        massage = {'err': '错误的访问方式'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        forum_title = request.POST.get('forum_title')
        forum_content = request.POST.get('forum_content')
        forum_section = request.POST.get('forum_section')
        section_id = request.POST.get('section_id')
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        if not (forum_title and forum_content):
            return JsonResponse({'status': False, 'message': '信息不完全'})

        if sensitiveWordCheck.search(forum_title) or sensitiveWordCheck.search(forum_content):
            return JsonResponse({'status': False, 'message': '用词不文明'})

        if not forum_section:
            forum_section = '0'

        if not section_id:
            section_id = None

        forum = Forum.objects.create(
            forum_title=forum_title,
            forum_content=forum_content,
            forum_creator=user_id,
            create_time=timezone.now(),
            forum_status='1',
            forum_section=forum_section,
            section_id=section_id,
            forum_priority='0',
            forum_visits='0'
        )

        massage = {'massage': '添加成功', 'forum_id': forum.forum_id}
        return JsonResponse(massage, safe=False)


class GetForumList(View):
    """
    模块: 用户获取论坛
    接口信息: 
    """
    
    def get(self, request):
        content = []
        forums = Forum.objects.all()
        for forum in forums:
            forum_data = []
            if forum.forum_section != 3 and forum.forum_section != 4:
                forum_like = ForumUser.objects.filter(forum_id=forum.forum_id, is_like='1').count()
                forum_collect = Collection.objects.filter(collection_forget_key=forum.forum_id, collection_type='2').count()
                replies = Reply.objects.filter(forum_id=forum.forum_id)
                forum_data.append({
                    'forum_id': forum.forum_id,
                    'forum_title': forum.forum_title,
                    'forum_content': forum.forum_content,
                    'forum_creator': forum.forum_creator,
                    'create_time': forum.create_time,
                    'forum_section': forum.forum_section,
                    'section_id': forum.section_id,
                    'forum_priority': forum.forum_priority,
                    'forum_visits': forum.forum_visits,
                    'like_num': forum_like,
                    'collect_num': forum_collect,
                    'reply_num': replies.count(),
                })
                reply_data = []
                for reply in replies:
                    reply_like = ReplyUser.objects.filter(reply_id=reply.reply_id, is_like='1').count()
                    reply_data.append({
                        'reply_id': reply.reply_id,
                        'reply_content': reply.reply_content,
                        'reply_creator': reply.reply_creator,
                        'pre_reply': reply.pre_reply,
                        'reply_priority': reply.reply_priority,
                        'create_time': reply.create_time,
                        'reply_like': reply_like,
                    })
                content.append({'forum': forum_data, 'reply': reply_data})
        return JsonResponse({'content': content})

    def post(self, request):
        return JsonResponse({'err': '无POST接口'})


class GetForumPage(View):
    """
    模块: 用户获取论坛页面/审核论坛
    接口信息:
    GET:
        section: 板块样式 0公共 1问题 2竞赛 3课程
        section_id: 板块编号
    POST:
        token: token认证
        forum_id: 论坛ID
        forum_status: 论坛状态
    """

    def get(self, request):
        section = request.GET.get('section')
        section_id = request.GET.get('section_id')

        forum_data = []
        if not section or section == '0':
            forum = Forum.objects.filter(forum_section='0')
        elif not section_id:
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        else:
            if section in ['1', '2', '3']:
                forum = Forum.objects.filter(forum_section=section, section_id=section_id)
            elif section == '4':
                forum = Forum.objects.filter(forum_section=section, section_id=section_id)
                for data in forum:
                    if data.forum_status == '1':
                        users = User.objects.filter(user_id=data.forum_creator).first()
                        if not users:
                            nick = data.forum_creator
                        else:
                            nick = users.user_nick
                        
                        forum_like = ForumUser.objects.filter(forum_id=data.forum_id, is_like='1').count()
                        forum_collect = Collection.objects.filter(collection_forget_key=data.forum_id,
                                                                  collection_type='2').count()
                        forum_reply = Reply.objects.filter(forum_id=data.forum_id).count()

                        forum_data.append({
                            'forum_id': data.forum_id,
                            'forum_title': data.forum_title,
                            'forum_content': data.forum_content,
                            'forum_creator': data.forum_creator,
                            'user_nick': nick,
                            'create_time': data.create_time,
                            'forum_section': data.forum_section,
                            'section_id': data.section_id,
                            'forum_priority': data.forum_priority,
                            'forum_visits': data.forum_visits,
                            'like_num': forum_like,
                            'collect_num': forum_collect,
                            'reply_num': forum_reply,
                        })

                course_id = CourseUser.objects.filter(course_class=section_id).values('course_id').first()
                forum = Forum.objects.filter(forum_section='3', section_id=course_id)
            else:
                massage = {'err': '没有这个板块'}
                return JsonResponse(massage, safe=False)
        
        
        for data in forum:
            if data.forum_status == 1:
                users = User.objects.filter(user_id=data.forum_creator).first()
                if not users:
                    nick = data.forum_creator
                else:
                    nick = users.user_nick

                forum_like = ForumUser.objects.filter(forum_id=data.forum_id, is_like='1').count()
                forum_collect = Collection.objects.filter(collection_forget_key=data.forum_id,
                                                          collection_type='2').count()
                forum_reply = Reply.objects.filter(forum_id=data.forum_id).count()

                forum_data.append({
                    'forum_id': data.forum_id,
                    'forum_title': data.forum_title,
                    'forum_content': data.forum_content,
                    'forum_creator': data.forum_creator,
                    'user_nick': nick,
                    'create_time': data.create_time,
                    'forum_section': data.forum_section,
                    'section_id': data.section_id,
                    'forum_priority': data.forum_priority,
                    'forum_visits': data.forum_visits,
                    'like_num': forum_like,
                    'collect_num': forum_collect,
                    'reply_num': forum_reply,
                })
        
        massage = {'content': forum_data}
        return JsonResponse(massage, safe=False)
            
    def post(self, request):
        token = request.POST.get('token')
        forum_id = request.POST.get('forum_id')
        forum_status = request.POST.get('forum_status')

        if not (token and forum_id and forum_status):
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
        
        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '论坛不存在'}
            return JsonResponse(massage, safe=False)

        if identity not in [0, 1]:
            if forum.forum_creator == '2':
                contest = Contest.objects.filter(contest_id=forum.section_id).first()
                if user_id != contest.contest_creator:
                    massage = {'err': '用户无权限'}
                    return JsonResponse(massage, safe=False)
            elif forum.forum_creator == '3' or forum.forum_creator == '4':
                users = CourseUser.objects.filter(course_id=forum.section_id).values('course_user')
                for data in users:
                    if data.values == user_id:
                        massage = {'err': '用户无权限'}
                        return JsonResponse(massage, safe=False)
            else:
                massage = {'err': '用户无权限'}
                return JsonResponse(massage, safe=False)
        
        forum.forum_status = forum_status
        forum.save()
        
        massage = {'massage': '已审核过'}
        return JsonResponse(massage, safe=False)


class GetMyForum(View):
    """
    模块: 用户查看自己的帖子、管理员查看所有帖子
    接口信息:
    GET:
        token: token认证
        forum_status: 帖子状态
        is_admin: 是否是管理员 0否 1是
    POST:
        None
    """

    def get(self, request):
        token = request.GET.get('token')
        forum_status = request.GET.get('forum_status')
        is_admin = request.GET.get('is_admin')

        if not (token and forum_status):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)
        
        if not is_admin:
            is_admin = '0'

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
        if is_admin == '1' and identity not in [0, 1]:
            massage = {'err': '身份不正确'}
            return JsonResponse(massage, safe=False)

        forum_data = []

        if is_admin == '1':
            forum = Forum.objects.filter(forum_status=forum_status)
        else:
            forum = Forum.objects.filter(forum_status=forum_status, forum_creator=user_id)

        for data in forum:
            users = User.objects.filter(user_id=data.forum_creator).first()
            if not users:
                nick = data.forum_creator
            else:
                nick = users.user_nick
            forum_data.append({
                'forum_id': data.forum_id,
                'forum_title': data.forum_title,
                'forum_content': data.forum_content,
                'forum_creator': data.forum_creator,
                'user_nick': nick,
                'create_time': data.create_time,
                'forum_section': data.forum_section,
                'section_id': data.section_id,
                'forum_priority': data.forum_priority,
                'forum_visits': data.forum_visits,
            })

        massage = {'content': forum_data}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        massage = {'err': '访问方式错误'}
        return JsonResponse(massage, safe=False)


class DeleteForum(View):
    """
    模块: 删除帖子
    接口信息:
    GET:
        None
    POST:
        token: token认证
        forum_id: 帖子ID
    """

    def get(self, request):
        massage = {'err': '访问方式错误'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        forum_id = request.POST.get('forum_id')

        if not (token and forum_id):
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

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '论坛不存在'}
            return JsonResponse(massage, safe=False)

        if user_id != forum.forum_creator and identity not in [0, 1]:
            if forum.forum_section == 2:
                contest = Contest.objects.filter(contest_id=forum.section_id).first()
                if user_id != contest.contest_creator:
                    massage = {'err': '用户无权限'}
                    return JsonResponse(massage, safe=False)
            elif forum.forum_section == 3 or forum.forum_section == 4:
                users = CourseUser.objects.filter(course_id=forum.section_id).values('course_user')
                if user_id not in users:
                    massage = {'err': '用户无权限'}
                    return JsonResponse(massage, safe=False)
            else:
                massage = {'err': '用户无权限'}
                return JsonResponse(massage, safe=False)

        forum.forum_status = '3'
        forum.save()

        content = {'content': '删除成功'}
        return JsonResponse(content, safe=False)


class UndeleteForum(View):
    """
    模块: 撤销删除帖子
    接口信息:
    GET:
        None
    POST:
        token: token认证
        forum_id: 帖子ID
    """

    def get(self, request):
        massage = {'err': '访问方式错误'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        forum_id = request.POST.get('post_id')

        if not (token and forum_id):
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

        forum = Forum.objects.filter(forum_id=int(forum_id)).first()
        if not forum:
            massage = {'err': '帖子不存在'}
            return JsonResponse(massage, safe=False)

        if forum.forum_creator != user_id and identity not in [0, 1]:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        forum.forum_status = '0'
        forum.save()

        massage = {'message': '修改成功'}
        return JsonResponse(massage, safe=False)


class ModifyForum(View):
    """
    模块: 修改帖子
    接口信息:
    GET:
        token: token认证
        forum_id: 帖子ID
    POST:
        token: token认证
        forum_id: 帖子ID
        forum_title:帖子标题
        forum_content:内容
    """

    def get(self, request):
        token = request.GET.get('token')
        forum_id = request.GET.get('forum_id')

        if not (token and forum_id):
            massage = {'err': 'Incomplete information'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            massage = {'err': '未登录'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                massage = {'err': '用户不存在or用户信息未完善'}
                return JsonResponse(massage, safe=False)

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '帖子不存在'}
            return JsonResponse(massage, safe=False)

        if forum.fourm_creator != user_id:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        content = {
            'forum_id': forum.forum_id,
            'forum_title': forum.forum_title,
            'forum_content': forum.forum_content,
        }

        massage = {'content': content}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        forum_id = request.POST.get('forum_id')
        forum_title = request.POST.get('forum_title')
        forum_content = request.POST.get('forum_content')

        if not (token and forum_id and forum_title and forum_content):
            massage = {'err': '访问方式错误'}
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

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '帖子不存在'}
            return JsonResponse(massage, safe=False)

        if forum.creator != user_id and identity not in [0, 1]:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        if forum.forum_title == forum_title and forum.forum_content == forum_content:
            massage = {'massage': '信息未修改'}
            return JsonResponse(massage, safe=False)

        forum.forum_title = forum_title
        forum.forum_content = forum_content
        forum.forum_status = '1'
        forum.save()

        content_date = {
            'forum_id': forum.forum_id,
            'forum_title': forum.forum_title,
            'forum_content': forum.forum_content,
        }

        content = {'content': '修改成功', 'forum': content_date}
        return JsonResponse(content, safe=False)


class GetReplyPage(View):
    """
    模块: 查看帖子
    接口信息:
    GET:
        forum_id: 论坛ID
    POST:
        None
    """
    def get(self, request):
        forum_id = request.GET.get('forum_id')

        if not forum_id:
            massage = {'err': '信息不完善'}
            return JsonResponse(massage, safe=False)
        
        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '论坛不存在'}
            return JsonResponse(massage, safe=False)

        users = User.objects.filter(user_id=forum.forum_creator).first()
        if not users:
            nick = forum.forum_creator
        else:
            nick = users.user_nick
        
        forum_like = ForumUser.objects.filter(forum_id=forum.forum_id, is_like='1').count()
        forum_collect = Collection.objects.filter(collection_forget_key=forum.forum_id, collection_type='2').count()
        forum_reply = Reply.objects.filter(forum_id=forum.forum_id).count()

        forum_data = {
            'forum_id': forum.forum_id,
            'forum_title': forum.forum_title,
            'forum_content': forum.forum_content,
            'creator_nick': nick,
            'create_time': forum.create_time,
            'forum_like': forum_like,
            'forum_collect': forum_collect,
            'forum_reply': forum_reply,
        }

        replies = Reply.objects.filter(forum_id=forum_id, reply_status=0)
        reply_data = []
        for data in replies:
            if data.reply_status == 0:
                users = User.objects.filter(user_id=data.reply_creator).first()
                reply_like = ReplyUser.objects.filter(reply_id=data.reply_id, is_like='1').count()
                if not users:
                    nick = forum.forum_creator
                else:
                    nick = users.user_nick
                reply_data.append({
                    'reply_id': data.reply_id,
                    'reply_content': data.reply_content,
                    'reply_creator': data.reply_creator,
                    'nick': nick,
                    'pre_reply': data.pre_reply,
                    'reply_priority': data.reply_priority,
                    'create_time': data.create_time,
                    'reply_like': reply_like,
                })

        forum.forum_visits = forum.forum_visits + 1
        forum.save()

        result = {'forum': forum_data, 'reply': reply_data}
        return JsonResponse(result, safe=False)

    def post(self, request):
        massage = {'err': '访问方式错误'}
        return JsonResponse(massage, safe=False)


class AddReply(View):
    """
    模块: 添加回复
    接口信息:
    GET:
        None
    POST:
        token: token认证
        forum_id: 帖子ID
        reply_id: 回复ID
        reply_content: 内容
    """

    def get(self, request):
        massage = {'err': '访问方式错误'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        forum_id = request.POST.get('forum_id')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        if not reply_id:
            reply_id = '-1'

        if not (token and forum_id and reply_content):
            massage = {'err': '信息不完善'}
            return JsonResponse(massage, safe=False)

        if sensitiveWordCheck.search(reply_content):
            massage = {'err': '用词不文明'}
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

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            massage = {'err': '论坛不存在'}
            return JsonResponse(massage, safe=False)

        reply = Reply.objects.create(
            forum_id=forum_id,
            reply_content=reply_content,
            reply_creator=user_id,
            create_time=timezone.now(),
            pre_reply=reply_id,
            reply_status='0',
            reply_priority='0'
        )
        
        reply_data = []

        reply_data.append({
            'reply_id': reply.reply_id,
            'forum_id': reply.forum_id,
            'reply_content': reply.reply_content,
            'reply_creator': reply.reply_creator,
            'pre_reply': reply.pre_reply,
            'create_time': reply.create_time,
            'reply_status': reply.reply_status,
            'reply_priority': reply.reply_priority,
        })

        massage = {'content': '添加成功', 'reply': reply_data}
        return JsonResponse(massage, safe=False)


class ModifyReply(View):
    """
    模块: 修改回复
    接口信息:
    GET:
        token: token认证
        reply_id: 回复ID
    POST:
        token: token认证
        reply_id: 回复ID
        content: 内容
    """

    def get(self, request):
        token = request.GET.get('token')
        reply_id = request.GET.get('reply_id')

        if not (token and reply_id):
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

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            massage = {'err': '没有这个回复'}
            return JsonResponse(massage, safe=False)

        if reply.creator != user_id and identity not in [0, 1]:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        content = {
            'content': reply.content,
        }

        massage = {'content': content}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        if not (token and reply_id and reply_content):
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

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            massage = {'err': '没有这个回复'}
            return JsonResponse(massage, safe=False)

        if reply.creator != user_id and identity not in [0, 1]:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        reply.reply_content = reply_content
        reply.save()

        massage = {'massage': '修改成功'}
        return JsonResponse(massage, safe=False)


class DeleteReply(View):
    """
    模块: 删除回复
    接口信息:
    GET:
        None
    POST:
        token: token认证
        reply_id: 回复ID
    """

    def get(self, request):
        massage = {'err': 'Wrong request method'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        reply_id = request.POST.get('reply_id')

        if not (token and reply_id):
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

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            massage = {'err': '回复不存在'}
            return JsonResponse(massage, safe=False)

        forum = Forum.objects.filter(forum_id=reply.forum_id).first()
        if not forum:
            massage = {'err': '论坛不存在'}
            return JsonResponse(massage, safe=False)
        
        creator = []

        if forum.forum_section == '3' or forum.forum_section == '4':
            course_user = CourseUser.objects.filter(course_id=forum.section_id)
            for data in course_user:
                creator.append(data.course_user)

        if reply.reply_creator != user_id and identity not in [0, 1] and reply.reply_creator not in creator:
            massage = {'err': '用户无权限'}
            return JsonResponse(massage, safe=False)

        reply.reply_status = '1'
        reply.save()

        massage = {'massage': '删除成功'}
        return JsonResponse(massage, safe=False)


class GetMyReply(View):
    """
    模块: 查看回复和删除自己帖子的回复
    接口信息:
    GET:
        token: token认证
    POST:
        None
    """

    def get(self, request):
        token = request.GET.get('token')

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

        reply_data = []
        replies = Reply.objects.filter(reply_creator=user_id)
        for data in replies:
            reply_data.append({
                'reply_id': data.reply_id,
                'forum_id': data.forum_id,
                'reply_content': data.reply_content,
                'reply_creator': data.reply_creator,
                'pre_reply': data.pre_reply,
                'create_time': data.create_time,
                'reply_status': data.reply_status,
            })

        message = {'content': reply_data}
        return JsonResponse(message, safe=False)

    def post(self, request):
        massage = {'err': 'Wrong request method'}
        return JsonResponse(massage, safe=False)


class LikeCollection(View):
    """
    模块: 点赞收藏
    接口信息:
    GET:
        None
    POST:
        token: token认证
        section_id: 点赞ID
        section_type: 点赞类型 0帖子 1回复
        do_type: 点击类型 0点赞 1收藏
    """

    def get(self, request):
        massage = {'err': 'Wrong request method'}
        return JsonResponse(massage, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        section_id = request.POST.get('post_id')
        section_type = request.POST.get('section_type')
        do_type = request.POST.get('do_type')

        if not (token and section_id and section_type and do_type):
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        if section_type == '1' and do_type == '1':
            massage = {'err': '回复不能收藏'}
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

        if section_type == '0':
            forum_user = ForumUser.objects.filter(forum_id=section_id, forum_user=user_id).first()
            if not forum_user:
                ForumUser.objects.create(
                    forum_id=section_id,
                    forum_user=user_id,
                    is_like='0'
                )
            forum_user = ForumUser.objects.filter(forum_id=section_id, forum_user=user_id).first()
            if do_type == '0':
                if forum_user.is_like == '0':
                    forum_user.is_like = '1'
                else:
                    forum_user.is_like = '0'
                forum_user.save()
            else:
                collection = Collection.objects.filter(collection_type='2', collection_forget_key=section_id).first()
                if not collection:
                    Collection.objects.create(
                        collection_type='2',
                        collection_user=user_id,
                        collection_forget_key=section_id,
                        collection_time=timezone.now,
                    )
                else:
                    collection.delete()
        else:
            reply_user = Reply.objects.filter(reply_id=section_id, reply_user=user_id).first()
            if not reply_user:
                ReplyUser.objects.create(
                    reply_id=section_id,
                    reply_user=user_id,
                    is_like='0'
                )
            reply_user = ReplyUser.objects.filter(reply_id=section_id, reply_user=user_id).first()
            if reply_user.is_like == '0':
                reply_user.is_like = '1'
            else:
                reply_user.is_like = '0'
            reply_user.save()

        message = {'message': 'Like or Bookmark Success'}
        return JsonResponse(message, safe=False)


class GetForumCollect(View):
    """
    模块: 查看和删除论坛收藏
    接口信息:
    GET:
        token: token认证
    POST:
        token: token认证
        collection_id: 收藏ID
    """

    def get(self, request):
        token = request.GET.get('token')

        if not token:
            massage = {'err': 'Incomplete information'}
            return JsonResponse(massage, safe=False)

        user_id = publicMethod.check_user_login(token)
        if not user_id:
            massage = {'err': 'No login'}
            return JsonResponse(massage, safe=False)
        else:
            user = User.objects.get(user_id__user_id=user_id)
            if not user:
                massage = {'err': 'No such user'}
                return JsonResponse(massage, safe=False)

        collection = Collection.objects.filter(user_id=user_id, collection_type='2')

        content_data = []
        for data in collection:
            forum=Forum.objects.filter(forum_id=collection.collection_forget_key).first()
            content_data.append({
                'collection_id': data.collection_id,
                'forum_id': forum.forum_id,
                'forum_title': forum.forum_title,
                'forum_content': forum.forum_content, 
            })

        result = {'content': content_data}
        return JsonResponse(result, safe=False)

    def post(self, request):
        token = request.POST.get('token')
        collection_id = request.POST.get('collection_id')

        if not (token and collection_id):
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

        collection = Collection.objects.filter(collection_id=collection_id).first()
        if not collection:
            massage = {'err': '无此收藏'}
            return JsonResponse(massage, safe=False)
        
        collection.delete()

        massage = {'massage': 'Modified successfully'}
        return JsonResponse(massage, safe=False)


class AddWord(View):
    """
    模块: 添加敏感词
    接口信息:
    GET:
        token: token认证
    POST:
        token: token认证
        word: 敏感词
    """
    def __init__(self):
        self.keyword_chains = []

    def getWord(self, level, char):
        for str in level:
            if str == sensitiveWordCheck.delimit:
                self.keyword_chains.append(char)
            else:
                self.getWord(level[str], char + str)

    def get(self, request):
        token = request.GET.get('token')

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
        if identity not in [0, 1]:
            massage = {'err': '身份不正确'}
            return JsonResponse(massage, safe=False)

        self.getWord(sensitiveWordCheck.keyword_chains, "")

        massage = {"word": self.keyword_chains}
        return JsonResponse(massage, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        word = request.POST.get('word')

        if not (token and word):
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
        if identity not in [0, 1]:
            massage = {'err': '身份不正确'}
            return JsonResponse(massage, safe=False)
        
        sensitiveWordCheck.add(word)

        massage = {'massage': '添加成功'}
        return JsonResponse(massage, safe=False)


class DeleteWord(View):
    """
    模块: 删除敏感词
    接口信息:
    GET:
        None
    POST:
        token: token认证
        word: 敏感词 
    """
    def get(self, request):
        massage = {'err': 'Wrong request method'}
        return JsonResponse(massage, safe=False)
    
    def post(self, request):
        token = request.POST.get('token')
        word = request.POST.get('word')

        if not (token and word):
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
        if identity not in [0, 1]:
            massage = {'err': '身份不正确'}
            return JsonResponse(massage, safe=False)
        
        if sensitiveWordCheck.delete(word):
            massage = {'massage': '添加成功'}
        else:
            massage = {'massage': '没有这个单词'}

        return JsonResponse(massage, safe=False)
