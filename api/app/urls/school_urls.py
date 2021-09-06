from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import school_views


urlpatterns = [
    url(r'^school/$', school_views.SchoolList.as_view()),
    url(r'^school/(?P<pk>[0-9]+)/$', school_views.SchoolDetail.as_view()),
    url(r'^college/$', school_views.CollegeList.as_view()),
    url(r'^college/(?P<pk>[0-9]+)/$', school_views.CollegeDetail.as_view()),
    url(r'^class/$', school_views.ClassList.as_view()),
    url(r'^class/(?P<pk>[0-9]+)/$', school_views.ClassDetail.as_view()),
    url(r'^class_user/$', school_views.ClassUserList.as_view()),
    url(r'^class_user/(?P<pk>[0-9]+)/$', school_views.ClassUserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
