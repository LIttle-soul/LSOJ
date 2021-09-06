from rest_framework import serializers
from app.models import Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'
