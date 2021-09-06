from rest_framework import serializers
from app.models import *


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = College
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = '__all__'


class ClassUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassUser
        fields = '__all__'
