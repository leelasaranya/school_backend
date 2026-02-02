from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Vote
from .serializers import VoteSerializer


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        performance = serializer.validated_data["performance"]

        # 🚫 BLOCK NON-PUBLIC USERS
        if hasattr(user, "student_profile"):
            raise PermissionDenied("Students are not allowed to vote")

        if hasattr(user, "teacher_profile"):
            raise PermissionDenied("Teachers are not allowed to vote")

        if hasattr(user, "judge_profile"):
            raise PermissionDenied("Judges are not allowed to vote")

        if hasattr(user, "school_admin_profile"):
            raise PermissionDenied("School admins are not allowed to vote")

        if hasattr(user, "admin_profile"):
            raise PermissionDenied("Admins are not allowed to vote")

        # ✅ ONLY APPROVED PERFORMANCES
        if performance.status != "approved":
            raise ValidationError(
                "Voting allowed only on approved performances"
            )

        # 🔒 ONE USER → ONE VOTE (IMPORTANT PART)
        if Vote.objects.filter(
            user=user,
            performance=performance
        ).exists():
            raise ValidationError("You have already voted")

        serializer.save(user=user)
