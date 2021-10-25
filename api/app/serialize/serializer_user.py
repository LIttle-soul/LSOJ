from rest_framework import serializers
from django.db.models import Q, F, Avg, Max, Min, Count, Sum
from app.models import *


class UserDataSerializer(serializers.ModelSerializer):
    user_school = serializers.SerializerMethodField()
    user_class = serializers.SerializerMethodField()
    user_team = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    registration_time = serializers.SerializerMethodField()
    user_solution_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'user_id',
            'user_name',
            'user_nick',
            'user_introduce',
            'user_power',
            'user_score',
            'user_sex',
            'user_telephone',
            'user_email',
            'user_birthday',
            'user_school',
            'user_class',
            'user_team',
            'user_address',
            'registration_time',
            'user_solution_data'
        )

    def get_user_school(self, obj):
        user = obj
        user_school = School.objects.filter(school_id=user.user_school)
        if user_school.exists():
            return user_school.values().first()
        else:
            return None

    def get_user_class(self, obj):
        user = obj
        user_class = Class.objects.filter(class_id=user.user_class)
        if user_class.exists():
            return user_class.values().first()
        else:
            return None

    def get_user_team(self, obj):
        user = obj
        user_team = Class.objects.filter(class_id=user.user_team)
        if user_team.exists():
            return user_team.values().first()
        else:
            return None

    def get_user_address(self, obj):
        user = obj
        user_address = Municipality.objects.filter(municipality_id=user.user_address)
        if user_address.exists():
            return user_address.values().first()
        else:
            return None

    def get_registration_time(self, obj):
        user = obj
        registration_time = Password.objects.filter(user_id=user.user_id)
        if registration_time.exists():
            return registration_time.first().registration_time
        else:
            return None

    def get_user_solution_data(self, obj):
        solution_data = {
            'user_solved': [],
            'user_submit': 0,
            'user_accurate': 0,
            'format_error': 0,
            'wrong_answer': 0,
            'time_over': 0,
            'memory_over': 0,
            'output_over': 0,
            'runtime_error': 0,
            'compile_error': 0
        }
        user = obj
        solution_data_submit = Solution.objects.filter(user_id=user.user_id)
        solution_data['user_submit'] = len(solution_data_submit)
        if solution_data_submit.exists():
            solution_data['user_solved'] = list(solution_data_submit.filter(run_result=4).values('problem_id').annotate(number=Count('user_id')))
            solution_data['user_accurate'] = solution_data_submit.filter(run_result=4).count()
            solution_data['format_error'] = solution_data_submit.filter(run_result=5).count()
            solution_data['wrong_answer'] = solution_data_submit.filter(run_result=6).count()
            solution_data['time_over'] = solution_data_submit.filter(run_result=7).count()
            solution_data['memory_over'] = solution_data_submit.filter(run_result=8).count()
            solution_data['output_over'] = solution_data_submit.filter(run_result=9).count()
            solution_data['runtime_error'] = solution_data_submit.filter(run_result=10).count()
            solution_data['compile_error'] = solution_data_submit.filter(run_result=11).count()
        return solution_data