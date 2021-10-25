from django.urls import path
from app.view.class_view import *

urlpatterns = [
    path('getselfclass/', getSelfClass.as_view(), name='get_self_class'),
    path('classusers/', ClassUsers.as_view(), name='class_users'),
    path('createTeam/', CreateTeam.as_view(), name='create_team'),
]
