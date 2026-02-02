from rest_framework.routers import DefaultRouter
from .views import (
    JudgeEvaluationViewSet,
    SchoolAdminEvaluationViewSet,
    AdminEvaluationViewSet
)

router = DefaultRouter()

router.register(
    r'judge/evaluations',
    JudgeEvaluationViewSet,
    basename='judge-evaluations'
)
router.register(
    r'school-admin/evaluations',
    SchoolAdminEvaluationViewSet,
    basename='schooladmin-evaluations'
)
router.register(
    r'admin/evaluations',
    AdminEvaluationViewSet,
    basename='admin-evaluations'
)

urlpatterns = router.urls

