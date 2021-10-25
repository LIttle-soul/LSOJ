from django.urls import path
from app.view.contest_view import *
from app.view import sign_up
urlpatterns = [
    path('contestlist/', ContestList.as_view(), name='contest_list'),
    # path('contestproblemlist/', contestProblemList.as_view(), name='contest_problem_list'),
    path('conteststatus/', contestStatus.as_view(), name='contest_status'),
    path('contestranklist/', ContestRankList.as_view(), name='contest_rank_list'),
    path('contestranklist_oj/', contestRankList_oj.as_view(), name='contest_rank_list_oj'),
    path('conteststatistics/', contestStatistics.as_view(), name='contest_statistics'),
    path('admincontest/', Admincontest.as_view(), name='admin_contest'),
    path('changecontest/', changeContest.as_view(), name='change_contest'),
    path('deletecontest/', deleteContest.as_view(), name='delete_contest'),
    path('singleSignUp/', sign_up.SingleSignUp.as_view(), name='single_signUp'),
    path('signUpInfo/', sign_up.signUpPage.as_view(), name='signUp_Info'),
    path('teamSignUp/', sign_up.TeamSignUp.as_view(), name='team_signUp'),
    path('getlatecontest/', getLateContest.as_view(), name="get_late_contest"),
    path('teamSignUpManage/', sign_up.teamSignUpManage.as_view(), name='team_signUp_Manage'),
    path('contestproblemlist/', ContestProblemList.as_view(), name='contest_problem_list'),
    path('contestuserlist/', ContestUserList.as_view(), name='contest_user_list'),
    path('contestrank/', ContestRanks.as_view(), name='contest_rank'),
    path('ranklist/', RankList.as_view(), name='rank_list'),
    path('conteststats/', ContestStats.as_view(), name='contest_stats')
]
