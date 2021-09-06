from app.models import Forum, Reply
from app.serializer.forum_serializer import ForumSerializer, ReplySerializer
from rest_framework import generics


class ForumList(generics.ListCreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class ForumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class ReplyList(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
