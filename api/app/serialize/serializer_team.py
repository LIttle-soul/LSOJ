from rest_framework import serializers
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app import models


class UserDataSerializer(serializers.ModelSerializer):
    # 序列化返回的字段
    team_school = serializers.SerializerMethodField()
    team_class = serializers.SerializerMethodField()
    team_member = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    registration_time = serializers.SerializerMethodField()
    user_solution_data = serializers.SerializerMethodField()

    # class Meta:
    #     model = Team
    #     fields = [
    #
    #     ]

