from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import level_views


urlpatterns = [
    url(r'^level/$', level_views.LevelList.as_view()),
    url(r'^level/(?P<pk>[0-9]+)/$', level_views.LevelDetail.as_view()),
    url(r'^level_kind/$', level_views.LevelKindList.as_view()),
    url(r'^level_kind/(?P<pk>[0-9]+)/$', level_views.LevelKindDetail.as_view()),
    url(r'^level_problem/$', level_views.LevelProblemList.as_view()),
    url(r'^level_problem/(?P<pk>[0-9]+)/$', level_views.LevelProblemDetail.as_view()),
    url(r'^pass_user/$', level_views.PassUserList.as_view()),
    url(r'^pass_user/(?P<pk>[0-9]+)/$', level_views.PassUserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
