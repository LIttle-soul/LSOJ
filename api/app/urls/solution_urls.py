from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import solution_views


urlpatterns = [
    url(r'^solution/$', solution_views.SolutionList.as_view()),
    url(r'^solution/(?P<pk>[0-9]+)/$', solution_views.SolutionDetail.as_view()),
    url(r'^sim/$', solution_views.SimList.as_view()),
    url(r'^sim/(?P<pk>[0-9]+)/$', solution_views.SimDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
