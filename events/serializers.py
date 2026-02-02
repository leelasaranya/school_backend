from rest_framework import serializers
from .models import Event, StudentEventInterest

class EventSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)
    is_interested = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "category",
            "rules",
            "event_type",
            "start_time",
            "end_time",
            "max_participants",
            "status",
            "school_name",
            "is_interested",   # ✅
        ]

    def get_is_interested(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        if hasattr(request.user, "student_profile"):
            return StudentEventInterest.objects.filter(
                student=request.user.student_profile,
                event=obj
            ).exists()

        return False
