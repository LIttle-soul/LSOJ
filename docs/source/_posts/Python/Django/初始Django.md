---
title: 初识Django
tags: [Python, Django]
categories: [Python, Django]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2020-10-10 08:00:00
hide: false
---

## 1. 模型设计

```python
#! mysite/news/models.py

from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name


class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
```

## 2. 应用数据模型

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3. Django 模板
