from django.urls import path
from app.view.team_view import *

urlpatterns = [
    path('getteamlist/', GetTeamList.as_view(), name='get_team_list'),
    path('createcode/', CreateCode.as_view(), name='create_code'),
    path('jointeam/', JoinTeam.as_view(), name='join_team'),
]
