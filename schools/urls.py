from rest_framework.routers import DefaultRouter
from .views import (
    AdminSchoolViewSet,
    AdminSchoolAdminViewSet,
    SchoolAdminTeacherViewSet,
    SchoolAdminStudentViewSet,
    TeacherStudentReadViewSet,
    SchoolDropdownViewSet
)

router = DefaultRouter()

router.register(r'admin/schools', AdminSchoolViewSet)
router.register(r'admin/school-admins', AdminSchoolAdminViewSet)
router.register("school-dropdown", SchoolDropdownViewSet, basename="school-dropdown")

router.register(
    r'school-admin/teachers',
    SchoolAdminTeacherViewSet,
    basename='school-admin-teachers'
)
router.register(
    r'school-admin/students',
    SchoolAdminStudentViewSet,
    basename='school-admin-students'
)
router.register(
    r'teacher/students',
    TeacherStudentReadViewSet,
    basename='teacher-students'
)

urlpatterns = router.urls
