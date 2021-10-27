---
title: 编写第一个Django应用
tags: [Python, Django]
categories: [Python, Django]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2021-10-10 08:00:00
hide: false
---

## 1. 查看 Django 版本

```bash
$ python -m django --version
```

## 2. 创建项目

```bash
$ django-admin startproject mysite
```

- 文件目录

```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

## 3. 用于开发的简易服务器

```bash
$ python manage.py runserver 0:8000
```

## 4. 创建投票应用

- 创建应用

```bash
$ python manage.py startapp polls
```

- 目录结构

```
polls/
    migrations/
        __init__.py
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
```

## 5. 编写第一个视图

```python
#! polls/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

```python
#! polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

```python
#! mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin', admin.site.urls),
]
```

```
python manage.py runserver
```

- #### path() 函数

> path(route, view, kwargs=None, name=None)
>
> - route: 字符串，表示 URL 规则，与之匹配的的 URL 会执行对应的第二个参数 view
> - view: 执行与正则表达式匹配的 URL 请求。
> - kwargs: 视图使用的字典类型的参数。
> - name: 用来反向获取 URL。
