from rest_framework import serializers
from app.models import *


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LevelKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelKind
        fields = '__all__'


class PassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassUser
        fields = '__all__'


class LevelProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelProblem
        fields = '__all__'
