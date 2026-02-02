from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        # Anyone can READ comments
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Only authenticated can TRY to comment
        return [IsAuthenticated()]

    def get_queryset(self):
        return Comment.objects.filter(
            performance__status='approved',
            is_approved=True
        )

    def perform_create(self, serializer):
        user = self.request.user
        performance = serializer.validated_data['performance']

        # 🔒 1️⃣ Allow comments only on approved performances
        if performance.status != 'approved':
            raise PermissionDenied(
                "Cannot comment on unapproved performance"
            )

        # 🔒 2️⃣ BLOCK ROLES (VERY IMPORTANT)
        blocked_roles = [
            "teacher",
            "judge",
            "school_admin",
            "admin",
            "super_admin",
        ]

        if hasattr(user, "role") and user.role in blocked_roles:
            raise PermissionDenied(
                "Your role is not allowed to participate in live chat"
            )

        # ✅ Only audience/public users reach here
        serializer.save(user=user)
