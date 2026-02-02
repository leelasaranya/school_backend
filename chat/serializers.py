from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "username",
            "message",     # ✅ correct field
            "role",        # ✅ role-based chat
            "created_at",
        ]
        extra_kwargs = {
            "role": {"read_only": True}
        }
