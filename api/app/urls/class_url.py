from django.urls import path
from app.view.class_view import *

urlpatterns = [
    path('createclass/', CreateClass.as_view(), name='create_team'),
]
