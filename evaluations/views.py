from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.permissions import (
    IsJudge,
    IsSchoolAdmin,
    IsAdmin
)
from .models import Evaluation
from .serializers import EvaluationSerializer


# 🧑‍⚖️ JUDGE → WRITE SCORE
class JudgeEvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated, IsJudge]

    def get_queryset(self):
        return Evaluation.objects.filter(
            judge=self.request.user
        )

    def perform_create(self, serializer):
        performance = serializer.validated_data['performance']

        if performance.status != 'approved':
            raise PermissionDenied(
                "Only approved performances can be evaluated"
            )
        if Evaluation.objects.filter(
        performance=performance,
        judge=self.request.user
        ).exists():
            raise PermissionDenied(
                "You already evaluated this performance"
            )
        serializer.save(judge=self.request.user)


# 🏫 SCHOOL ADMIN → SEE ALL SCORES (OWN EVENTS)
class SchoolAdminEvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]
    http_method_names = ['get']

    def get_queryset(self):
        return Evaluation.objects.filter(
            performance__event__school=
            self.request.user.school_admin_profile.school
        )


# 👑 ADMIN → READ-ONLY (AUDIT)
class AdminEvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ['get']
