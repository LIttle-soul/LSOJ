from app.models import Contest, ContestProblem, ContestUser
from app.serializer.contest_serializer import ContestSerializer, ContestProblemSerializer, ContestUserSerializer
from rest_framework import generics


class ContestList(generics.ListCreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ContestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ContestUserList(generics.ListCreateAPIView):
    queryset = ContestUser.objects.all()
    serializer_class = ContestUserSerializer


class ContestUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContestUser.objects.all()
    serializer_class = ContestUserSerializer


class ContestProblemList(generics.ListCreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestProblemSerializer


class ContestProblemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContestProblem.objects.all()
    serializer_class = ContestProblemSerializer
