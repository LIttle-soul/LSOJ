"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from app.urls import \
    address_urls, \
    contest_urls, \
    level_urls, \
    problem_urls, \
    school_urls, \
    language_urls, \
    user_urls, \
    solution_urls, \
    forum_urls, \
    news_urls, \
    balloon_urls, \
    printer_urls


urlpatterns = [
    path('docs/', include_docs_urls(title='接口文档')),
    path('admin/', admin.site.urls),
    url(r'files/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('address/', include(address_urls)),
    path('contest/', include(contest_urls)),
    path('level/', include(level_urls)),
    path('problem/', include(problem_urls)),
    path('school/', include(school_urls)),
    path('solution/', include(solution_urls)),
    path('user/', include(user_urls)),
    path('language/', include(language_urls)),
    path('forum/', include(forum_urls)),
    path('news/', include(news_urls)),
    path('balloon/', include(balloon_urls)),
    path('printer/', include(printer_urls)),
    # url(r'^api-auth/', include('rest_framework.urls',
    #                            namespace='rest_framework')),
]
