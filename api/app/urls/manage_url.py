from app.view import sign_up

from django.urls import path

urlpatterns = [
    path("singleSignUp/", sign_up.singleSignUpManage.as_view()),
    path("teamSignUp/", sign_up.teamSignUpManage.as_view()),
    path("teamModify/", sign_up.teamSignUpModify.as_view()),
]