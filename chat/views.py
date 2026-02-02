from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_role(self, user):
        if hasattr(user, "teacher_profile"):
            return "teacher"

        if hasattr(user, "student_profile"):
            return "student"

        if hasattr(user, "school_admin_profile"):
            return "school_admin"

        if hasattr(user, "profile") and getattr(user.profile, "role", None) == "judge":
            return "judge"

        return "student"  # safe default

    def get(self, request):
        role = self.get_user_role(request.user)

        messages = (
            ChatMessage.objects
            .filter(role=role)
            .order_by("-created_at")[:100]
        )

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data[::-1])

    def post(self, request):
        role = self.get_user_role(request.user)

        serializer = ChatMessageSerializer(data={
            "message": request.data.get("message")
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            role=role
        )

        return Response(serializer.data)
