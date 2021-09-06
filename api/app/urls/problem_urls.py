from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import problem_views


urlpatterns = [
    url(r'^problem/$', problem_views.ProblemList.as_view()),
    url(r'^problem/(?P<pk>[0-9]+)/$', problem_views.ProblemDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
