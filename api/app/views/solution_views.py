from app.models import Solution, Sim
from app.serializer.solution_serializer import SolutionSerializer, SimSerializer
from rest_framework import generics


class SolutionList(generics.ListCreateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SolutionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SimList(generics.ListCreateAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer


class SimDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
