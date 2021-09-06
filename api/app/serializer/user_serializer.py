from rest_framework import serializers
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.models import *


class UserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPassword
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_id.user_id', read_only=True, label='用户账号')
    registration_time = serializers.DateTimeField(source='user_id.registration_time', read_only=True, label='注册时间')

    class Meta:
        model = User
        fields = '__all__'


class UserRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRank
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginLog
        fields = '__all__'


class LimitLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = LimitLogin
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'
