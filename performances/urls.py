from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminPerformanceViewSet,
    TeacherPerformanceUploadViewSet,
    SchoolAdminPerformanceViewSet,
    JudgePerformanceViewSet,
    PublicPerformanceViewSet,
    SchoolAdminApprovePerformanceAPIView,
    TeacherUploadStudentsAPIView,   # ✅ IMPORT THIS
)

router = DefaultRouter()

# 🔒 SUPER ADMIN
router.register(
    r'admin/performances',
    AdminPerformanceViewSet,
    basename='admin-performances'
)

# 🧑‍🏫 TEACHER → UPLOAD
router.register(
    r'teacher/performances',
    TeacherPerformanceUploadViewSet,
    basename='teacher-performances'
)

# 🏫 SCHOOL ADMIN → VIEW
router.register(
    r'school-admin/performances',
    SchoolAdminPerformanceViewSet,
    basename='school-admin-performances'
)

# ⚖️ JUDGE → VIEW APPROVED
router.register(
    r'judge/performances',
    JudgePerformanceViewSet,
    basename='judge-performances'
)

# 🌍 PUBLIC → VIEW APPROVED
router.register(
    r'public/performances',
    PublicPerformanceViewSet,
    basename='public-performances'
)

urlpatterns = router.urls + [
    # 🏫 SCHOOL ADMIN → APPROVE / REJECT
    path(
        "school-admin/performances/<int:performance_id>/action/",
        SchoolAdminApprovePerformanceAPIView.as_view(),
        name="school-admin-performance-action",
    ),

    # 🧑‍🏫 TEACHER → STUDENTS FOR UPLOAD  ✅ THIS WAS MISSING
    path(
        "teacher/upload-students/",
        TeacherUploadStudentsAPIView.as_view(),
        name="teacher-upload-students",
    ),
]
