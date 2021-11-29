from django.urls import path
from app.view.school_view import *

urlpatterns = [
    path('synchronizeschool/', SynchronizeSchool.as_view(), name='SynchronizeSchool'),
    path('getschool/', GetSchool.as_view(), name='GetSchool'),
    # path('putschool/', PutSchool.as_view(), name="PutSchool")
]
