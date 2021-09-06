from rest_framework import serializers
from app.models import Balloon


class BalloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balloon
        fields = '__all__'
