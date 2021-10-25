from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import sessions
from django.views.generic import View
from django.utils import timezone
from app.RoleMethod.PublicMethod import PublicMethod
from django.views import View
from app.serialize.serializer_user import *
from django.core.cache import cache

"""
获取新闻列表
发布新闻
修改新闻
查看新闻
"""


class GetNewList(View):
    """
    新闻后台管理列表
    接口信息：
        get:
            获取数据库中记录，返回数据库中的内容
    返账信息：
        get：
            返回前端数据

    """
    def get(self, request):
        news = News.objects.all()
        info = []
        for new in news:
            info.append({
                "news_id": new.news_id,
                "news_title": new.news_title,
                "news_introduce": new.news_introduce,
                "news_creator": new.news_creator,
                "create_time": new.creator_time,
                "news_type": new.news_type,
                "news_importance": new.news_importance,
            })
        return JsonResponse({'status': True, "message": info})


class AddNews(View):
    """
    模块: 新闻管理
    接口信息：
        post：
        put：
    返账信息：
        post：
        put：
    """
    def post(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        if capacity > 2:
            return JsonResponse({'status': False, 'message': '权限不足'})
        news_introduce = request.POST.get("news_introduce")
        news_title = request.POST.get("news_title")
        news_type = request.POST.get("news_type")
        news_importance = request.POST.get('news_importance')
        News.objects.create(
            news_title=news_title,
            news_introduce=news_introduce,
            news_creator=user_id,
            creator_time=timezone.now(),
            news_importance=news_importance,
            news_type=news_type
        )
        return JsonResponse({'status': True, 'message': '新闻创建成功'})

    def put(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        news_id = request.GET.get('news_id')
        news = News.objects.filter(news_id=news_id).first()
        if not news:
            return JsonResponse({'status': False, 'message': '此新闻不存在'})
        if capacity > 2 or (capacity == 2 and news.news_creator != user_id):
            return JsonResponse({'status': False, 'message': '权限不足'})
        news_title = request.GET.get("news_title")
        if news_title is not None:
            news.news_title = news_title
        news_introduce = request.GET.get("news_introduce")
        if news_introduce is not None:
            news.news_introduce = news_introduce
        news_importance = request.GET.get('news_importance')
        if news_importance is not None:
            news.news_importance = news_importance
        news_type = request.GET.get("news_type")
        if news_type is not None:
            news.news_type = news_type
        news.save()
        return JsonResponse({'status': True, 'message': '修改成功'})

    def delete(self, request):
        token = request.COOKIES.get("token")
        user_id = cache.get(token)
        if not user_id:
            return JsonResponse({'status': False, 'message': '未登录'})
        capacity = User.objects.filter(user_id=user_id).first().user_power
        news_id = request.GET.get('news_id')
        news = News.objects.filter(news_id=news_id).first()
        if not news:
            return JsonResponse({'status': False, 'message': '此新闻不存在'})
        if capacity > 2 or (capacity == 2 and news.news_creator != user_id):
            return JsonResponse({'status': False, 'message': '权限不足'})
        news.delete()
        return JsonResponse({'status': True, 'message': '删除成功'})
