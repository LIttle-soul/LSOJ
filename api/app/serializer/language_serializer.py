from rest_framework import serializers
from app.models import *


class CodeLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeLanguage
        fields = '__all__'
