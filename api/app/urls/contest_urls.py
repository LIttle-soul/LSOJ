from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import contest_views


urlpatterns = [
    url(r'^contest/$', contest_views.ContestList.as_view()),
    url(r'^contest/(?P<pk>[0-9]+)/$', contest_views.ContestDetail.as_view()),
    url(r'^contest_user/$', contest_views.ContestUserList.as_view()),
    url(r'^contest_user/(?P<pk>[0-9]+)/$', contest_views.ContestUserDetail.as_view()),
    url(r'^contest_problem/$', contest_views.ContestProblemList.as_view()),
    url(r'^contest_problem/(?P<pk>[0-9]+)/$', contest_views.ContestProblemDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
