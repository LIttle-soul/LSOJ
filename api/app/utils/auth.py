from app.models import *
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication


class UserInfo(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('token')
        u_id = cache.get(token)
        if u_id:
            password_obj = UserPassword.objects.filter(user_id=u_id)
            if password_obj.exists():
                password = password_obj.first()
                user_obj = User.objects.filter(user_id=password)
                if user_obj.exists():
                    cache.touch(token, 3600)
                    return user_obj.first(), password
                else:
                    return False, password
        else:
            return False, False
