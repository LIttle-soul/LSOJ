from django.urls import path
from django.views.decorators.cache import cache_page
from app import views

urlpatterns = [
    path('login/', cache_page(0)(views.Login.as_view()), name='login'),
    path('register/', cache_page(0)(views.Register.as_view()), name='register'),
    path('perfectinfo/', views.PerfectInfo.as_view(), name='perfect_info'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('changepassword/', views.PasswordModification.as_view(), name='change_password'),
    path('sendemail/', views.SendEmail.as_view(), name='send_email'),
    path('forgetpassword/', views.ForgetPassword.as_view(), name='forget_password'),
    path('getuserlist/', views.GetUserList.as_view(), name='get_user_list'),
    path('getuserstatus/', views.GetUserStatus.as_view(), name='get_user_status'),
    path('changeusercapacity/', views.ChangeUserCapacity.as_view(), name='change_user_capacity'),
    path('resettinguserpassword/', views.ResettingUserPassword.as_view(), name='resetting_user_password'),
    path('addnews/', views.AddNews.as_view(), name='add_news'),
]
