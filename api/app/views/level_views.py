from app.serializer.level_serializer import LevelSerializer, LevelProblemSerializer, LevelKindSerializer, PassUserSerializer
from app.models import Level, LevelKind, LevelProblem, PassUser
from rest_framework import generics


class LevelList(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelKindList(generics.ListCreateAPIView):
    queryset = LevelKind.objects.all()
    serializer_class = LevelKindSerializer


class LevelKindDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LevelKind.objects.all()
    serializer_class = LevelKindSerializer


class PassUserList(generics.ListCreateAPIView):
    queryset = PassUser.objects.all()
    serializer_class = PassUserSerializer


class PassUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PassUser.objects.all()
    serializer_class = PassUserSerializer


class LevelProblemList(generics.ListCreateAPIView):
    queryset = LevelProblem.objects.all()
    serializer_class = LevelProblemSerializer


class LevelProblemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LevelProblem.objects.all()
    serializer_class = LevelProblemSerializer
