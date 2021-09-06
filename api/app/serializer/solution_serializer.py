from rest_framework import serializers
from app.models import *


class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = '__all__'


class SimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sim
        fields = '__all__'
