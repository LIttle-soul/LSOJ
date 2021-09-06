from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import user_views


urlpatterns = [
    path('user/', user_views.UserList.as_view()),
    path('user/<pk>/', user_views.UserDetail.as_view()),
    path('user_password/', user_views.UserPasswordList.as_view()),
    path('user_password/<pk>/', user_views.UserPasswordDetail.as_view()),
    path('user_rank/', user_views.UserRankList.as_view()),
    path('user_rank/<pk>/', user_views.UserRankDetail.as_view()),
    path('login_log/', user_views.LoginLogList.as_view()),
    path('login_log/<pk>/', user_views.LoginLogDetail.as_view()),
    path('limit_login', user_views.LimitLoginList.as_view()),
    path('limit_login/<pk>/', user_views.LimitLoginDetail.as_view()),
    path('collection/', user_views.CollectionList.as_view()),
    path('collection/<pk>/', user_views.CollectionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
