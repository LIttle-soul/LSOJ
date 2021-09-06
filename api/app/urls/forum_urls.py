from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import forum_views


urlpatterns = [
    url(r'^forum/$', forum_views.ForumList.as_view()),
    url(r'^forum/(?P<pk>[0-9]+)/$', forum_views.ForumDetail.as_view()),
    url(r'^reply/$', forum_views.ReplyList.as_view()),
    url(r'^reply/(?P<pk>[0-9]+)/$', forum_views.ReplyDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
