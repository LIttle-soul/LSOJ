from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import language_views


urlpatterns = [
    url(r'^code_language/$', language_views.CodeLanguageList.as_view()),
    url(r'^code_language/(?P<pk>[0-9]+)/$', language_views.CodeLanguageDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
