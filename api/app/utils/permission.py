from app.models import *
from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
SUBMIT_METHODS = ('POST',)


class IsLogin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.auth
        )


class IsPerfect(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user_id == request.user.user_id
        )


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.user_power in [0]
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.user_power in [0, 1]
        )


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.user_power in [0, 1, 2]
        )


class IsVolunteer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.user_power in [0, 1, 3]
        )
