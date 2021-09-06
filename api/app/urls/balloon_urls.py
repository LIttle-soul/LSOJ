from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import balloon_views


urlpatterns = [
    url(r'^balloon/$', balloon_views.BalloonList.as_view()),
    url(r'^balloon/(?P<pk>[0-9]+)/$', balloon_views.BalloonDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
