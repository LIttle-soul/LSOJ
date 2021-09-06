from app.models import Province, Municipality
from app.serializer.address_serializer import ProvinceSerializer, MunicipalitySerializer
from rest_framework import generics


class ProvinceList(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class ProvinceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class MunicipalityList(generics.ListCreateAPIView):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class MunicipalityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
