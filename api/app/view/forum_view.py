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
        forums = Forum.objects.all()
        users = User.objects.all()
        replies = Reply.objects.all()
        collects = Collection.objects.all()
        likes = ForumUser.objects.all()
        forum_data = []
        for forum in forums:
            if forum.forum_section != 3 and forum.forum_section != 4:
                user = users.filter(user_id=forum.forum_creator).first()
                if not user:
                    user_name = ''
                    user_icon = ''
                else:
                    user_nick = user.user_nick
                    user_icon = user.user_icon
                forum_data.append({
                    'forum_id': forum.forum_id,
                    'forum_title': forum.forum_title,
                    'forum_content': forum.forum_content,
                    'forum_creator': forum.forum_creator,
                    'user_nick': user_nick,
                    'user_icon': user_icon,
                    'create_time': forum.create_time,
                    'forum_section': forum.forum_section,
                    'section_id': forum.section_id,
                    'forum_priority': forum.forum_priority,
                    'forum_visits': forum.forum_visits,
                    'like_num': likes.filter(forum_id=forum.forum_id, is_like='1').count(),
                    'collect_num': collects.filter(collection_forget_key=forum.forum_id, collection_type='2').count(),
                    'reply_num': replies.filter(forum_id=forum.forum_id).count(),
                })
        return JsonResponse({'status': True, 'message': forum_data})


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
            return JsonResponse({'status': False, 'message': '信息不完全'})
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
                return JsonResponse({'status': False, 'message': '没有这个板块'})
        
        
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
        return JsonResponse({'status': False, 'message': forum_data})
            
    def post(self, request):
        token = request.COOKIES.get('token')
        user_id = cache.get(token)
        forum_id = request.POST.get('forum_id')
        forum_status = request.POST.get('forum_status')

        if not (forum_id and forum_status):
            return JsonResponse({'status': False, 'message': '信息不完全'})
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})
        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

        if user.user_power not in [0, 1]:
            if forum.forum_creator == '2':
                contest = Contest.objects.filter(contest_id=forum.section_id).first()
                if user_id != contest.contest_creator:
                    return JsonResponse({'status': False, 'message': '用户无权限'})
            elif forum.forum_creator == '3' or forum.forum_creator == '4':
                users = CourseUser.objects.filter(course_id=forum.section_id).values('course_user')
                for data in users:
                    if data.values == user_id:
                        return JsonResponse({'status': False, 'message': '用户无权限'})
            else:
                return JsonResponse({'status': False, 'message': '用户无权限'})
        
        forum.forum_status = forum_status
        forum.save()

        return JsonResponse({'status': True, 'message': '审核成功'})


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
        token = request.COOKIES.get('token')
        forum_status = request.GET.get('forum_status')
        is_admin = request.GET.get('is_admin')

        if not forum_status:
            return JsonResponse({'status': False, 'message': '信息不完全'})
        
        if not is_admin:
            is_admin = '0'

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})
        if is_admin == '1' and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '身份不正确'})

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
        return JsonResponse({'status': True, 'message': forum_data})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        forum_id = request.POST.get('forum_id')

        if not forum_id:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

        if user_id != forum.forum_creator and user.user_power not in [0, 1]:
            if forum.forum_section == 2:
                contest = Contest.objects.filter(contest_id=forum.section_id).first()
                if user_id != contest.contest_creator:
                    return JsonResponse({'status': False, 'message': '用户无权限'})
            elif forum.forum_section == 3 or forum.forum_section == 4:
                users = CourseUser.objects.filter(course_id=forum.section_id).values('course_user')
                if user_id not in users:
                    return JsonResponse({'status': False, 'message': '用户无权限'})
            else:
                return JsonResponse({'status': False, 'message': '用户无权限'})

        forum.forum_status = '3'
        forum.save()
        return JsonResponse({'status': True, 'message': '删除成功'})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        forum_id = request.POST.get('post_id')

        if not forum_id:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        forum = Forum.objects.filter(forum_id=int(forum_id)).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

        if forum.forum_creator != user_id and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        forum.forum_status = '0'
        forum.save()
        return JsonResponse({'status': True, 'message': '修改成功'})


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
        token = request.COOKIES.get('token')
        forum_id = request.GET.get('forum_id')

        if not forum_id:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

        if forum.fourm_creator != user_id:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        content = {
            'forum_id': forum.forum_id,
            'forum_title': forum.forum_title,
            'forum_content': forum.forum_content,
        }
        return JsonResponse({'status': True, 'message': content})

    def post(self, request):
        token = request.COOKIES.get('token')
        forum_id = request.POST.get('forum_id')
        forum_title = request.POST.get('forum_title')
        forum_content = request.POST.get('forum_content')

        if not (forum_id and forum_title and forum_content):
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

        if forum.creator != user_id and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        if forum.forum_title == forum_title and forum.forum_content == forum_content:
            return JsonResponse({'status': False, 'message': '信息未修改'})

        forum.forum_title = forum_title
        forum.forum_content = forum_content
        forum.forum_status = '1'
        forum.save()

        content_date = {
            'forum_id': forum.forum_id,
            'forum_title': forum.forum_title,
            'forum_content': forum.forum_content,
        }
        return JsonResponse({'status': True, 'message': '修改成功', 'forum': content_date})


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
            return JsonResponse({'status': False, 'message': '信息不完全'})
        
        forum = Forum.objects.filter(forum_id=forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})

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
        return JsonResponse({'status': True, 'message': result})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        forum_id = request.POST.get('forum_id')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        if not reply_id:
            reply_id = '-1'

        if not (forum_id and reply_content):
            return JsonResponse({'status': False, 'message': '信息不完全'})

        if sensitiveWordCheck.search(reply_content):
            return JsonResponse({'status': False, 'message': '用词不文明'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

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
        
        reply_data = [{
            'reply_id': reply.reply_id,
            'forum_id': reply.forum_id,
            'reply_content': reply.reply_content,
            'reply_creator': reply.reply_creator,
            'pre_reply': reply.pre_reply,
            'create_time': reply.create_time,
            'reply_status': reply.reply_status,
            'reply_priority': reply.reply_priority,
        }]
        return JsonResponse({'status': True, 'message': '添加成功', 'reply': reply_data})


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
        token = request.COOKIES.get('token')
        reply_id = request.GET.get('reply_id')

        if not reply_id:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            return JsonResponse({'status': False, 'message': '没有这个回复'})

        if reply.creator != user_id and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})
        return JsonResponse({'status': True, 'message': reply.content})

    def post(self, request):
        token = request.COOKIES.get('token')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        if not (reply_id and reply_content):
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            return JsonResponse({'status': False, 'message': '没有这个回复'})

        if reply.creator != user_id and user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        reply.reply_content = reply_content
        reply.save()

        return JsonResponse({'status': True, 'message': '修改成功'})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        reply_id = request.POST.get('reply_id')

        if not reply_id:
            massage = {'err': '信息不完全'}
            return JsonResponse(massage, safe=False)

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        reply = Reply.objects.filter(reply_id=reply_id).first()
        if not reply:
            return JsonResponse({'status': False, 'message': '回复不存在'})

        forum = Forum.objects.filter(forum_id=reply.forum_id).first()
        if not forum:
            return JsonResponse({'status': False, 'message': '论坛不存在'})
        
        creator = []

        if forum.forum_section == '3' or forum.forum_section == '4':
            course_user = CourseUser.objects.filter(course_id=forum.section_id)
            for data in course_user:
                creator.append(data.course_user)

        if reply.reply_creator != user_id and user.user_power not in [0, 1] and reply.reply_creator not in creator:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        reply.reply_status = '1'
        reply.save()

        return JsonResponse({'status': True, 'message': '删除成功'})


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
        token = request.COOKIES.get('token')

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

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

        return JsonResponse({'status': True, 'message': reply_data})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        section_id = request.POST.get('post_id')
        section_type = request.POST.get('section_type')
        do_type = request.POST.get('do_type')

        if not (section_id and section_type and do_type):
            return JsonResponse({'status': False, 'message': '信息不完全'})

        if section_type == '1' and do_type == '1':
            return JsonResponse({'status': False, 'message': '回复不能收藏'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

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

        return JsonResponse({'status': True, 'message': '点赞或收藏成功'})


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
        token = request.COOKIES.get('token')

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

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

        return JsonResponse({'status': False, 'message': content_data})

    def post(self, request):
        token = request.COOKIES.get('token')
        collection_id = request.POST.get('collection_id')

        if not collection_id:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})

        collection = Collection.objects.filter(collection_id=collection_id).first()
        if not collection:
            return JsonResponse({'status': False, 'message': '未收藏'})
        
        collection.delete()

        return JsonResponse({'status': True, 'message': '删除成功'})


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
        token = request.COOKIES.get('token')

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})
        if user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})

        self.getWord(sensitiveWordCheck.keyword_chains, "")

        return JsonResponse({'status': True, 'message': self.keyword_chains })
    
    def post(self, request):
        token = request.COOKIES.get('token')
        word = request.POST.get('word')

        if not word:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})
        if user.user_power not in [0, 1]:
            massage = {'err': '身份不正确'}
            return JsonResponse(massage, safe=False)

        sensitiveWordCheck.add(word)
        return JsonResponse({'status': True, 'message': '添加成功'})


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
    def post(self, request):
        token = request.COOKIES.get('token')
        word = request.POST.get('word')

        if not word:
            return JsonResponse({'status': False, 'message': '信息不完全'})

        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        else:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'status': False, 'message': '用户不存在or用户信息未完善'})
        if user.user_power not in [0, 1]:
            return JsonResponse({'status': False, 'message': '用户无权限'})
        
        if sensitiveWordCheck.delete(word):
            return JsonResponse({'status': True, 'message': '删除成功'})
        else:
            return JsonResponse({'status': True, 'message': '没有这个单词'})
