from rest_framework import serializers
from app.models import *


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'


class ContestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestProblem
        fields = '__all__'


class ContestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestUser
        fields = '__all__'
