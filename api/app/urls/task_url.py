from app.view import task_view
from django.urls import path


urlpatterns = [
    path("addTask/", task_view.Task.as_view()),
    path("taskContent/", task_view.TaskContent.as_view())
]