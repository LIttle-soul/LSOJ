from app.models import Balloon
from app.serializer.balloon_serializer import BalloonSerializer
from rest_framework import generics


class BalloonList(generics.ListCreateAPIView):
    queryset = Balloon.objects.all()
    serializer_class = BalloonSerializer


class BalloonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Balloon.objects.all()
    serializer_class = BalloonSerializer
