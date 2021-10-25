from django.urls import path
from django.views.decorators.cache import cache_page
from app.view.level_view import *

urlpatterns = [
    path('addlevel/', addLevel.as_view(), name='add_level'),
    path('editlevel/', editLevel.as_view(), name='edit_level'),
    path('deletelevel/', deleteLevel.as_view(), name='delete_level'),
    path('getlevellist/', getLevelList.as_view(), name='get_level_list'),
    path('openclass/', openClass.as_view(), name='open_class'),
    path('levelcompletion/', levelCompletion.as_view(), name='level_completion'),
]