import app.view
"""jhcoj_api URL Configuration

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('address/', include('app.urls.address_url')),
    # path('balloon/', include('app.urls.balloon_url')),
    # path('chapter/', include('app.urls.chapter_url')),
    path('class/', include('app.urls.class_url')),
    path('contest/', include('app.urls.contest_url')),
    path('course/', include('app.urls.course_url')),
    path('forum/', include('app.urls.forum_url')),
    path('level/', include('app.urls.level_url')),
    # path('news/', include('app.urls.news_url')),
    # path('printer/', include('app.urls.printer_url')),
    path('problem/', include('app.urls.problem_url')),
    # path('question/', include('app.urls.question_url')),
    path('school/', include('app.urls.school_url')),
    path('solution/', include('app.urls.solution_url')),
    # path('task/', include('app.urls.task_url')),
    path('user/', include('app.urls.user_url')),
    path('manage/', include('app.urls.manage_url')),
    path('news/', include('app.urls.news_url')),
    url(r'files/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
