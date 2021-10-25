from django.urls import path
from app.view.forum_view import *

urlpatterns = [
    path('createforum/', CreateForum.as_view(), name='create_forum'),
    path('getforumlist', GetForumList.as_view(), name='get_forum_list'),
    path('getforumpage/', GetForumPage.as_view(), name='get_forum_page'),
    path('getmyforum/', GetMyForum.as_view(), name='get_my_forum'),
    path('deleteforum/', DeleteForum.as_view(), name='delete_forum'),
    # path('undeleteforum/', UndeleteForum.as_view(), name='undelete_forum'),
    path('modifyforum/', ModifyForum.as_view(), name='modify_forum'),
    path('getreplypage/', GetReplyPage.as_view(), name='get_reply_page'),
    path('addreply/', AddReply.as_view(), name='add_reply'),
    # path('modifyreply/', ModifyReply.as_view(), name='modify_reply'),
    path('deletereply/', DeleteReply.as_view(), name='delete_reply'),
    path('getmyreply/', GetMyReply.as_view(), name='get_my_reply'),
    path('likeCollection/', LikeCollection.as_view(), name='like_collection'),
    path('getforumcollect/', GetForumCollect.as_view(), name='get_forum_collect'),
    path('addword/', AddWord.as_view(), name='add_word'),
    path('deleteword/', DeleteWord.as_view(), name='delete_word'),
]