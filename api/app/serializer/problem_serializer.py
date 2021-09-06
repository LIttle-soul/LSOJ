from rest_framework import serializers
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.models import *


class ProblemSerializer(serializers.ModelSerializer):
    problem_accepted = serializers.SerializerMethodField()
    problem_submit = serializers.SerializerMethodField()

    def get_problem_accepted(self, obj):
        return Solution.objects.filter(Q(problem_id=obj.problem_id) & Q(run_result=4)).count()

    def get_problem_submit(self, obj):
        return Solution.objects.filter(problem_id=obj.problem_id).count()

    class Meta:
        model = Problem
        fields = '__all__'
