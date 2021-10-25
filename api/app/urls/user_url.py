from django.urls import path
from django.views.decorators.cache import cache_page
from app.view.user_view import *

urlpatterns = [
    path('checktwopassword/', CheckTwoPasswords.as_view(), name='check_two_password'),
    path('login/', cache_page(0)(Login.as_view()), name='login'),
    path('register/', cache_page(0)(Register.as_view()), name='register'),
    path('getusertokeninfo/', GetUserTokenInfo.as_view(), name='get_user_token_info'),
    path('perfectinfo/', PerfectInfo.as_view(), name='perfect_info'),
    path('changepassword/', PasswordModification.as_view(), name='change_password'),
    path('sendemail/', SendEmail.as_view(), name='send_email'),
    path('forgetpassword/', ForgetPassword.as_view(), name='forget_password'),
    path('getranklist/', GetRankList.as_view(), name='get_rank_list'),
    path('getuserlist/', GetUserList.as_view(), name='get_user_list'),
    path('getuserstatus/', GetUserStatus.as_view(), name='get_user_status'),
    path('changeusercapacity/', ChangeUserCapacity.as_view(), name='change_user_capacity'),
    path('resettinguserpassword/', ResettingUserPassword.as_view(), name='resetting_user_password'),
    path('getusericon/', GetUserIcon.as_view(), name='get_user_icon'),
    path('createtesttoken/', createTestToken.as_view(), name='create_test_token'),
    path('userstatus/', UserStatus.as_view(), name='user_status'),
    path('mycontest/', MyContest.as_view(), name='my_contest'),
]
