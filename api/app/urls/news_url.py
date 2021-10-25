from django.urls import path
from app.view import news_view

urlpatterns = [
    path("getnewslist/", news_view.GetNewList.as_view(), name='get_news_list'),
    path("addnews/", news_view.AddNews.as_view(), name='add_news'),
]