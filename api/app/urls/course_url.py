from django.urls import path
from app.view.course_view import *

urlpatterns = [
    path('wecoursehome', WeCourseHome.as_view(), name='we_course_home'),
    path('createcourse/', CreateCourse.as_view(), name='create_course'),
    path('addcoursemenu/', AddCourseMenu.as_view(), name='add_course_menu'),
    path('uploadcoursefile/', UploadCourseFile.as_view(), name='upload_course_file'),
    path('downloadcoursefile/', DownloadCourseFile.as_view(), name='download_course_file'),
    path('courseaddstudent/', CourseAddStudent.as_view(), name='course_add_student'),
    path('batchimportstudents/', BatchImportStudents.as_view(), name='batch_import_students'),
    path('coursehome/', CourseHome.as_view(), name='course_home'),
    path('joincourse/', JoinCourse.as_view(), name='join_course'),
    path('viewteachcourse/', ViewTeachCourse.as_view(), name='view_teach_course'),
    path('createclass/', CreateClass.as_view(), name='create_class'),
    path('viewcoursechapter/', ViewCourseChapter.as_view(), name='view_course_chapter'),
    path('viewjoincourse/', ViewJoinCourse.as_view(), name='view_join_course'),
    path('viewcourseassignment/', ViewCourseAssignment.as_view(), name='view_course_assignment'),
    path('viewallcourse/', ViewAllCourse.as_view(), name='view_all_course'),
    path('modifycourseintroduction/', ModifyCourseIntroduction.as_view(), name='modify_course_introduction'),
    path('viewclasslist/', ViewClassList.as_view(), name='view_class_list'),
    path('deleteclasspersonnel/', DeleteClassPersonnel.as_view(), name='delete_class_personnel'),
    path('addassistantteacher/', AddAssistantTeacher.as_view(), name='add_assistant_teacher'),
    path('deleteassistantteacher/', DeleteAssistantTeacher.as_view(), name='delete_assistant_teacher'),
    path('releasehomeworktest/', ReleaseHomeworkTest.as_view(), name='release_homework_test'),
    path('modifyhomeworktest/', ModifyHomeworkTest.as_view(), name='modify_homework_test'),
    path('viewcourseassignmentexam/', ViewCourseAssignmentExam.as_view(), name='view_course_assignment_exam'),
    path('submitjob/', SubmitJob.as_view(), name='submit_job')
]