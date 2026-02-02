from django.urls import path
from .views import RegisterStudentAPIView,TeacherRegisteredStudentsForUploadAPIView

urlpatterns = [
    path("registrations/", RegisterStudentAPIView.as_view()),
    path(
        "teacher/upload-students/",
        TeacherRegisteredStudentsForUploadAPIView.as_view()
    ),
]
