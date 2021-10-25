from django.urls import path
from app.view.problem_view import *

urlpatterns = [
    path('getproblemlist/', GetProblemList.as_view(), name='get_problem_list'),
    # path('getproblemInfo/', GetProblemInfo.as_view(), name='get_problem_info'),
    path('addproblem/', AddProblem.as_view(), name='add_problem'),
    path('changeproblem/', ChangeProblem.as_view(), name='change_problem'),
    # path('deleteproblem/', DeleteProblem.as_view(), name='delete_problem'),
    path('reprimandproblem/', ReprimandProblem.as_view(), name='reprimand_problem'),
    path('getproblemtag/', GetProblemTag.as_view(), name='get_problem_tag'),
    path('upimage/', UpImage.as_view(), name='up_image'),
    path('imagelist/', ImageList.as_view(), name='image_list'),
    path('problemsample/', ProblemSample.as_view(), name='problem_sample')
]

