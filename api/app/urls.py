from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('perfectinfo/', views.PerfectInfo.as_view(), name='perfect_info'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('addnews/', views.AddNews.as_view(), name='add_news'),
]
