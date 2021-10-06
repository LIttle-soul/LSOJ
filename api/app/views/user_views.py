from app.serializer.user_serializer import *
from rest_framework import generics, exceptions
from rest_framework import permissions, response
from django.core.cache import cache
from app.utils.auth import UserInfo
from app.utils.permission import *
import uuid

from app.utils.method import Method

method = Method()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (UserInfo,)
    # permission_classes = (IsOwnerOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.auth)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (UserInfo,)
    # permission_classes = (IsOwnerOrReadOnly,)


class UserPasswordList(generics.ListCreateAPIView):
    queryset = UserPassword.objects.all()
    serializer_class = UserPasswordSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'register':
            return self.create(request, *args, **kwargs)
        elif action == 'login':
            user_id = request.data.get('user_id')
            user_password = request.data.get('user_password')
            obj = UserPassword.objects.filter(user_id=user_id)
            if obj.exists():
                if method.check_password(
                    password_new=user_password,
                    password_old=obj.first().user_password
                ):
                    token = uuid.uuid4().hex
                    cache.set(token, user_id, 1200)
                    data = {
                        'msg': '登陆成功',
                        'status': 200,
                        'token': token
                    }
                    message = response.Response(data)
                    message.set_cookie('token', token, 1200)
                    return message
                else:
                    raise exceptions.AuthenticationFailed
            else:
                raise exceptions.NotFound
        else:
            raise exceptions.ValidationError

    def perform_create(self, serializer):
        serializer.save(user_password=method.reg_pass(self.request.data.get('user_password')))


class UserPasswordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPassword.objects.all()
    serializer_class = UserPasswordSerializer
    authentication_classes = (UserInfo,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_update(self, serializer):
        serializer.save(user_password=method.reg_pass(self.request.data.get('user_password')))


class UserRankList(generics.ListCreateAPIView):
    queryset = UserRank.objects.all()
    serializer_class = UserRankSerializer
    authentication_classes = (UserInfo,)


class UserRankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRank.objects.all()
    serializer_class = UserRankSerializer
    authentication_classes = (UserInfo,)


class LoginLogList(generics.ListCreateAPIView):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    authentication_classes = (UserInfo,)


class LoginLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    authentication_classes = (UserInfo,)


class LimitLoginList(generics.ListCreateAPIView):
    queryset = LimitLogin.objects.all()
    serializer_class = LimitLoginSerializer
    authentication_classes = (UserInfo,)


class LimitLoginDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LimitLogin.objects.all()
    serializer_class = LimitLoginSerializer
    authentication_classes = (UserInfo,)


class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = (UserInfo,)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = (UserInfo,)
