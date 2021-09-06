from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import news_views


urlpatterns = [
    url(r'^news/$', news_views.NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)/$', news_views.NewsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
