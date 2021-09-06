from rest_framework import serializers
from app.models import *


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'
