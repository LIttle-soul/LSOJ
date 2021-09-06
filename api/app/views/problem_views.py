from app.models import Problem
from app.serializer.problem_serializer import ProblemSerializer
from rest_framework import generics


class ProblemList(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
