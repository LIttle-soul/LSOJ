from app.models import School, College, Class, ClassUser
from app.serializer.school_serializer import SchoolSerializer, CollegeSerializer, ClassSerializer, ClassUserSerializer
from rest_framework import generics


class SchoolList(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CollegeList(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class CollegeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class ClassList(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassUserList(generics.ListCreateAPIView):
    queryset = ClassUser.objects.all()
    serializer_class = ClassUserSerializer


class ClassUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassUser.objects.all()
    serializer_class = ClassUserSerializer
