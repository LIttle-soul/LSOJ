import datetime

from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from app.models import *
from app.RoleMethod.PublicMethod import PublicMethod
from message import consumers


publicMethod = PublicMethod()


class sendMessageByClass(View):
    """
        模块: 消息广播 发送消息给选中班级中的学生
        接口信息:
        GET:
            pass
        POST:
            token，class_str（班级id字符串，使用,分割,display推送方式，1普通推送，2弹窗提示，title消息标题，message,消息内容，type消息类型course|class，从课程中选择班级发送的应使用course，从班级模块发送信息的，应使用class
            发送信息给班级中的学生
            返回结果
    """
    def get(self,request):
        pass

    def post(self,request):
        course_id = request.POST.get('course_id',0)
        display = int(request.POST.get('display', 1))
        type = request.POST.get('type', 'class')
        title = request.POST.get('title', '')
        message = request.POST.get('message', '')
        class_str = request.POST.get('class_str', '')
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        if course_id=='' or not course_id.isdigit():
            return JsonResponse({'status': False, 'err': 'course_id is wrong','data': []})
        course_id = int(course_id)
        capacity = publicMethod.get_user_capacity(token)
        user_id = publicMethod.check_user_login(token)
        user_nick = publicMethod.get_user_nick(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission', 'data': []})
        if class_str == '' or class_str == None:
            return JsonResponse({'status': False, 'err': 'class_str is empty', 'data': []})
        if message == '' or message == None:
            return JsonResponse({'status': False, 'err': 'message content is empty', 'data': []})
        if title == '' or title == None:
            return JsonResponse({'status': False, 'err': 'message title is empty', 'data': []})
        class_list = class_str.sqlit(',')
        class_str=''
        classes = []
        for c in class_list:
            c_title = Class.objects.values('title').filter(class_id=int(c)).frist()
            classes.append(c_title['title'])
        class_str=','.join(classes)
        new_message = Message.objects.create(
            title=title,
            content=message,
            creator=user_id,
            creator_nick=user_nick,
            recipient_des="推送班级：" + class_str,
            recipient_type=type,
            recipient_id=course_id,
            display_mode=display,
        )
        message_id = new_message.message_id
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT DISTINCT(user_id) FROM class_user where class_id in (%s) AND user_type=0",
                    [class_str])
            class_users = cursor.fetchall()
            class_users = list(class_users)
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})
        user_count = class_users.count()
        result_count = 0
        try:
            for c in class_users:
                u = UserMessage.objects.create(
                    message_id=message_id,
                    user_id=c[0],
                    is_view=0
                )
                data=[]
                data.append({'title': title, 'content': message,'creator':user_id,'creator_nick':user_nick, 'display': display, 'message_id': message_id})
                consumers.send_group_msg(u.user_id,{'data':data,'haveNew':True})
                result_count += 1
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})

        return JsonResponse(
            {'status': True, 'err': 'success', 'data': {'user_count': user_count, 'send_count': result_count}})


class sendMessageByUser(View):
    """
            模块: 消息广播 发送消息给选中竞赛中的学生或者个人
            接口信息:
            GET:
                pass
            POST:
                token，user_str（用户id字符串，使用,分割,display推送方式，1普通推送，2弹窗提示，title消息标题，message,消息内容，type消息类型contest|person，发送竞赛消息则为contest，个人则为person，id_str当为竞赛时可以附上竞赛id字符串，以,分割，
                发送信息给班级中的学生
                返回结果
        """


    def get(self, request):
        pass

    def post(self, request):
        display = int(request.POST.get('display', 1))
        type = request.POST.get('type', 'person')
        title = request.POST.get('title', '')
        id_str = request.POST.get('id_str','0')
        message = request.POST.get('message', '')
        user_str = request.POST.get('user_str', '')
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        user_nick = publicMethod.get_user_nick(token)
        capacity = publicMethod.get_user_capacity(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission', 'data': []})
        if user_str == '' or user_str == None:
            return JsonResponse({'status': False, 'err': 'user_str is empty', 'data': []})
        if message == '' or message == None:
            return JsonResponse({'status': False, 'err': 'message content is empty', 'data': []})
        if title == '' or title == None:
            return JsonResponse({'status': False, 'err': 'message title is empty', 'data': []})
        #获取竞赛名称字符串字段
        id_list = id_str.sqlit(',')
        contests = []
        for c in id_list:
            c_title = Contest.objects.values('contest_title').filter(contest_id=int(c)).first()
            contests.append(c_title['title'])
        contest_str = ','.join(contests)
        new_message = Message.objects.create(
            title=title,
            content=message,
            creator=user_id,
            creator_nick=user_nick,
            recipient_des="推送给竞赛成员（id："+id_str+"）的消息" if type=='contest' else "推送给个人的消息",
            recipient_type=type,
            display_mode=display,
        )
        message_id = new_message.message_id
        send_users = user_str.sqlit(',')
        user_count = send_users.count()
        result_count = 0
        try:
            for c in send_users:
                u = UserMessage.objects.create(
                    message_id=message_id,
                    user_id=c,
                    is_view=0
                )
                #发送消息
                data = []
                data.append({'title': title, 'content': message,'creator':user_id,'creator_nick':user_nick, 'display': display, 'message_id': message_id})
                consumers.send_group_msg(u.user_id,{'data':data,'haveNew':True})
                result_count += 1
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})

        return JsonResponse(
            {'status': True, 'err': 'success', 'data': {'user_count': user_count, 'send_count': result_count}})


class sendMessageAll(View):
    """
        模块: 消息广播 发送消息给所有人
        接口信息:
        GET:
            pass
        POST:
            token，分割,display推送方式，1普通推送，2弹窗提示，title消息标题，message,消息内容，type消息类型contest|person，发送竞赛消息则为contest，个人则为person
            返回结果
    """

    def get(self,request):
        pass
    def post(self,request):
        display = int(request.POST.get('display', 1))
        title = request.POST.get('title', '')
        message = request.POST.get('message', '')
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        user_nick = publicMethod.get_user_nick(token)
        capacity = publicMethod.get_user_capacity(token)
        if capacity > 1:
            return JsonResponse({'status': False, 'err': 'No permission', 'data': []})
        if message == '' or message == None:
            return JsonResponse({'status': False, 'err': 'message content is empty', 'data': []})
        if title == '' or title == None:
            return JsonResponse({'status': False, 'err': 'message title is empty', 'data': []})

        new_message = Message.objects.create(
            title=title,
            content=message,
            creator=user_id,
            creator_nick=user_nick,
            recipient_des="推送给所有人",
            recipient_type='all',
            display_mode=display,
        )
        message_id = new_message.message_id
        send_users = User.objects.values('user_id').all()
        user_count = send_users.count()
        result_count = 0
        try:
            for c in send_users:
                u = UserMessage.objects.create(
                    message_id=message_id,
                    user_id=c,
                    is_view=0
                )
                # 发送消息
                data = []
                data.append(
                    {'title': title, 'content': message, 'creator': user_id, 'creator_nick': user_nick, 'display': display,
                     'message_id': message_id})
                consumers.send_group_msg(u.user_id, {'data': data, 'haveNew': True})
                result_count += 1
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})

        return JsonResponse(
            {'status': True, 'err': 'success', 'data': {'user_count': user_count, 'send_count': result_count}})





class getMessage(View):
    """
          模块: 消息广播 获取消息列表
          接口信息:
          GET:
              token
              获取用户的消息列表
          POST:
              token，message_id
              获取用户想要打开的消息信息
      """
    def get(self,request):
        token = request.GET.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        data = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select DISTINCT(message.message_id),message.title,message.content,message.creator,message.creator_nick,message.create_time,user_message.is_view from message LEFT JOIN user_message on message.message_id=user_message.message_id where user_message.user_id=%s and message.defunct='N' AND message.is_delete='N' ORDER BY create_time desc",
                    [user_id])
            messages = cursor.fetchall()
            messages = list(messages)
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})

        for m in messages:
            data.append({
                'message_id':m[0],
                'title':m[1],
                'content':m[2],
                'creator':m[3],
                'creator_nick':m[4],
                'create_time':m[5],
                'is_view':m[6]
            })
        return JsonResponse({'status': True, 'err': 'success', 'data': data})


    def post(self,request):
        message_id = request.POST.get('message_id',0)
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        if message_id==0 or not message_id.isdigit():
            return JsonResponse({'status': False, 'err': 'message_id wrong', 'data': []})
        message_id = int(message_id)
        data = {}
        try:
            message = Message.objects.filter(message_id=message_id,defunct='N',is_delete='N').first()
            try:
                UserMessage.objects.filter(message_id=message_id,user_id=user_id).update(
                    is_view = 1,
                    view_date = datetime.datetime.now()
                )
            except:
                pass
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})
        if message.exit():
            data['message_id'] = message_id
            data['title'] = message.title
            data['content'] = message.content
            data['create_time'] = message.create_time
            data['creator'] = message.creator
            data['creator_nick'] = message.creator_nick
            data['recipient_des'] = message.recipient_des
            return JsonResponse({'status': True, 'err': 'success', 'data': data})
        else:
            return JsonResponse({'status': False, 'err': 'No relevant records', 'data': data})



class checkMessage(View):
    """
         模块: 消息广播 检查是否有未读消息，在用户刚登陆的时候使用
         接口信息:
         GET:
             token
             获取用户的消息列表
         POST:
             token，message_id
             更新用户消息,发送是否还有未读消息
     """
    def get(self,request):
        token = request.GET.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        data = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select DISTINCT(message.message_id),user_message.user_message_id,message.title,message.content,creator,creator_nick,message.create_time,message.display_mode,user_message.is_view from message LEFT JOIN user_message on message.message_id=user_message.message_id where user_message.user_id=%s and message.defunct='N' AND message.is_delete='N' and user_message.is_view=0 ORDER BY create_time desc",
                    [user_id])
            messages = cursor.fetchall()
            messages = list(messages)
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})
        if messages.count()>0:
            data=[]
            for m in messages:
                data.append({'title': m[2], 'content': m[3],'creator':m[4],'creator_nick':m[5], 'type': m[7], 'mu_id': m[1]})
            consumers.send_group_msg(user_id,{'data':data,'haveNew':True})
            return JsonResponse({'status': True, 'err': 'success', 'haveNew': True})
        else:
            return JsonResponse({'status': True, 'err': 'success', 'haveNew': False})

    def post(self,request):
        message_id = request.POST.get('message_id',0)
        token = request.POST.get('token')
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        if message_id==0 or not message_id.isdigit():
            return JsonResponse({'status': False, 'err': 'message_id wrong', 'data': []})
        message_id = int(message_id)
        try:
            UserMessage.objects.filter(message_id=message_id,user_id=user_id).update(is_view=1)
        except:
            return JsonResponse({'status': False, 'err': 'Database connection failed', 'data': []})
        return JsonResponse({'status': True, 'err': 'success', 'data': []})


class getMessageList(View):
    """
         模块: 消息广播 管理员，老师获取消息列表，以及查看情况
         接口信息:
         GET:
             token
             获取用户的消息列表
         POST:
             pass
    """


    def get(self,request):
        token = request.GET.get('token')
        course_id = request.GET.get('course_id',0)
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        capacity = publicMethod.get_user_capacity(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission', 'data': []})
        if course_id=='' or not course_id.isdigit():
            return JsonResponse({'status': False, 'err': 'course_id is wrong', 'data': []})
        course_id = int(course_id)

        #当用户是老师的时候，只能查看她自己发送的消息
        data=[]
        if capacity == 2:
            if course_id!=0:
                pri = Course.objects.filter(course_creator=user_id,course_id=course_id,)
                if pri.exit():
                    messages = Message.objects.filter(recipient_id=course_id,is_delete='N').order_by("-create_time")
                else:
                    messages = Message.objects.filter(recipient_id=course_id,creator=user_id,is_delete='N').order_by("-create_time")
            else:
                messages = Message.objects.filter(recipient_id=0,creator=user_id,is_delete='N').order_by("-create_time")
            for m in messages:
                view_count = UserMessage.objects.filter(is_view=1,message_id=m.message_id).count()
                not_view_count = UserMessage.objects.filter(is_view=0,message_id=m.message_id).count()
                if m.creator == user_id:
                    can_delete = True
                else:
                    can_delete = False
                data.append({
                    'message_id':m.message_id,
                    'title': m.title,
                    'content' :m.content,
                    'creator' :m.creator,
                    'creator_nick' :m.creator_nick,
                    'create_time':m.create_time,
                    'display_mode' : m.display_mode,
                    'defunct':m.defunct,
                    'can_delete':can_delete,
                    'view_count':view_count,
                    'message_count':view_count+not_view_count
                })
        #当用户是管理员或者更高的时候，可以看到所有的消息
        else:
            messages = Message.objects.filter(recipient_id=course_id, is_delete='N').order_by("-create_time")
            for m in messages:
                view_count = UserMessage.objects.filter(is_view=1, message_id=m.message_id).count()
                not_view_count = UserMessage.objects.filter(is_view=0, message_id=m.message_id).count()
                data.append({
                    'message_id': m.message_id,
                    'title': m.title,
                    'content': m.content,
                    'creator': m.creator,
                    'creator_nick': m.creator_nick,
                    'create_time': m.create_time,
                    'display_mode': m.display_mode,
                    'defunct': m.defunct,
                    'can_delete': True,
                    'view_count': view_count,
                    'message_count': view_count + not_view_count
                })
        return JsonResponse({'status': True, 'err': 'success', 'data': data})
    def post(self,request):
        pass


class changeMessageStatus(View):
    """
         模块: 消息广播 管理员，老师改变消息状态
         接口信息:
         GET:
             pass
         POST:
             token,message_id,option
             返回成功与否
    """
    def get(self,request):
        pass
    def post(self,request):
        token = request.POST.get('token')
        message_id = request.POST.get('message_id', 0)
        option = request.POST.get('option', )
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        capacity = publicMethod.get_user_capacity(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission'})
        if message_id == '' or not message_id.isdigit():
            return JsonResponse({'status': False, 'err': 'course_id is wrong'})
        if option == None or option == '' or (option != 'N' and option != 'Y'):
            return JsonResponse({'status': False, 'err': 'option is wrong'})
        message_id = int(message_id)
        if capacity == 2:
            m = Message.objects.filter(message_id=message_id, creator=user_id, is_delete='N').first()
            if m.exit():
                m.update(defunct=option)
            else:
                return JsonResponse({'status': False, 'err': 'Parameter error or no permission,delete failed'})
        else:
            m = Message.objects.filter(message_id=message_id, is_delete='N').first()
            if m.exit():
                m.update(defunct=option)
            else:
                return JsonResponse({'status': False, 'err': 'Parameter error or no permission,delete failed'})
        return JsonResponse({'status': True, 'err': 'success'})



class deleteMessage(View):
    """
         模块: 消息广播 管理员，老师删除当前信息列表吧
         接口信息:
         GET:
            pass
         POST:
            token,message_id
    """
    def get(self,request):
        pass
    def post(self,request):
        token = request.POST.get('token')
        message_id = request.POST.get('message_id', 0)
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        capacity = publicMethod.get_user_capacity(token)
        if capacity > 2:
            return JsonResponse({'status': False, 'err': 'No permission'})
        if message_id == '' or not message_id.isdigit():
            return JsonResponse({'status': False, 'err': 'course_id is wrong'})
        message_id=int(message_id)
        if capacity ==2:
            m = Message.objects.filter(creator=user_id,message_id=message_id,is_delete='N').first()
            if m.exit():
                m.update(is_delete='Y')
                UserMessage.objects.filter(message_id=message_id).delete()
            else:
                return JsonResponse({'status': False, 'err': 'Parameter error or no permission,delete failed'})

        else:
            m = Message.objects.filter(message_id=message_id, is_delete='N').first().update(is_delete='Y')
            UserMessage.objects.filter(message_id=message_id).delete()
        return JsonResponse({'status': True, 'err': 'success'})

class deleteUserMessage(View):
    """
         模块: 消息广播 普通用户删除单单条记录
         接口信息:
         GET:
            pass
         POST:
            token,message_id
            执行删除用户消息记录操作
    """
    def get(self,request):
        pass
    def post(self,request):
        token = request.POST.get('token')
        message_id = request.POST.get('message_id', 0)
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        if message_id == '' or not message_id.isdigit() or message_id==0:
            return JsonResponse({'status': False, 'err': 'course_id is wrong'})
        message_id = int(message_id)
        message = UserMessage.objects.filter(message_id=message_id,user_id=user_id)
        if message.exit():
            message.delete()
        else:
            return JsonResponse({'status': False, 'err': 'not such record,fail'})
        return JsonResponse({'status': True, 'err': 'success'})

class changeViewStatus(View):
    """
         模块: 消息广播 普通用户更改消息是否已查看
         接口信息:
         GET:
            pass
         POST:
            token,message_id,option
            执行更新，用户是否更新是否已读状况
    """

    def get(self,request):
        pass
    def post(self,request):
        token = request.POST.get('token')
        message_id = request.POST.get('message_id', 0)
        option = request.POST.get('option', 0)
        if publicMethod.parse_payload(token)['status'] == False:
            return JsonResponse({'status': False, 'err': publicMethod.parse_payload(token)['error'], 'data': []})
        user_id = publicMethod.check_user_login(token)
        if message_id == '' or not message_id.isdigit() or message_id == 0:
            return JsonResponse({'status': False, 'err': 'course_id is wrong'})
        if not option.isdigit():
            return JsonResponse({'status': False, 'err': 'option is wrong'})
        message_id = int(message_id)
        option = int(option)
        message = UserMessage.objects.filter(message_id=message_id, user_id=user_id)
        if message.exit():
            message.update(is_view=option)
        else:
            return JsonResponse({'status': False, 'err': 'not such record,fail'})
        return JsonResponse({'status': True, 'err': 'success'})