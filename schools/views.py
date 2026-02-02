'''from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.permissions import IsAdmin, IsSchoolAdmin, IsTeacher
from .models import School, SchoolAdmin, Teacher, Student
from .serializers import (
    SchoolSerializer,
    SchoolAdminSerializer,
    TeacherSerializer,
    StudentSerializer
)


# 🔹 ADMIN CONTROLS
class AdminSchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AdminSchoolAdminViewSet(ModelViewSet):
    queryset = SchoolAdmin.objects.all()
    serializer_class = SchoolAdminSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# 🔹 SCHOOL ADMIN CONTROLS
class SchoolAdminTeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Teacher.objects.filter(
            school=self.request.user.schooladmin.school
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.schooladmin.school
        )

    def perform_update(self, serializer):
        if self.get_object().school != self.request.user.schooladmin.school:
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.school != self.request.user.schooladmin.school:
            raise PermissionDenied("Not allowed")
        instance.delete()


class SchoolAdminStudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Student.objects.filter(
            school=self.request.user.schooladmin.school
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.schooladmin.school
        )

    def perform_update(self, serializer):
        if self.get_object().school != self.request.user.schooladmin.school:
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.school != self.request.user.schooladmin.school:
            raise PermissionDenied("Not allowed")
        instance.delete()


# 🔹 TEACHER READ ONLY
class TeacherStudentReadViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(
            school=self.request.user.teacher.school
        )
'''
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ReadOnlyModelViewSet

from accounts.permissions import IsAdmin, IsSchoolAdmin, IsTeacher
from .models import School, SchoolAdmin, Teacher, Student
from .serializers import (
    SchoolSerializer,
    SchoolAdminSerializer,
    TeacherSerializer,
    StudentSerializer,
    SchoolDropdownSerializer
)


# 🔹 ADMIN CONTROLS
class AdminSchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AdminSchoolAdminViewSet(ModelViewSet):
    queryset = SchoolAdmin.objects.all()
    serializer_class = SchoolAdminSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# 🔹 SCHOOL ADMIN CONTROLS
'''class SchoolAdminTeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Teacher.objects.filter(
            created_by=self.request.user.schooladmin
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.schooladmin.school,
            created_by=self.request.user.schooladmin
        )

'''
class SchoolAdminTeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Teacher.objects.filter(
            school=self.request.user.school_admin_profile.school
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.school_admin_profile.school,
            created_by=self.request.user.school_admin_profile
        )


'''class SchoolAdminStudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Student.objects.filter(
            created_by=self.request.user.schooladmin
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.schooladmin.school,
            created_by=self.request.user.schooladmin
        )
'''
class SchoolAdminStudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Student.objects.filter(
            created_by=self.request.user.school_admin_profile
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.school_admin_profile.school,
            created_by=self.request.user.school_admin_profile
        )


# 🔹 TEACHER READ ONLY
'''class TeacherStudentReadViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(
            school=self.request.user.teacher.school
        )
'''
class TeacherStudentReadViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(
            school=self.request.user.teacher_profile.school
        )
# schools/views.py


class SchoolDropdownViewSet(ReadOnlyModelViewSet):
    serializer_class = SchoolDropdownSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            school_admin = SchoolAdmin.objects.get(user=user)
            return School.objects.filter(id=school_admin.school.id)
        except SchoolAdmin.DoesNotExist:
            return School.objects.none()
