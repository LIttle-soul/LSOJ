from django.urls import path
from app.view.solution_view import *

urlpatterns = [
    path('problemSubmission/', ProblemSubmission.as_view(), name='problem_submission'),
    path('statussubmit/', StatusSubmit.as_view(), name='status_submit'),
    path('onesolutionstatus/', OneSolutionStatus.as_view(), name='one_solution_status')
]
