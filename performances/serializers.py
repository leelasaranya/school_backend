from rest_framework import serializers
from .models import Performance
from schools.models import Student
from events.models import Event


class PerformanceSerializer(serializers.ModelSerializer):
    # 🔹 READ-ONLY DISPLAY FIELDS
    student_name = serializers.CharField(
        source='student.user.username',
        read_only=True
    )
    school_name = serializers.CharField(
        source='student.school.name',
        read_only=True
    )
    event_title = serializers.CharField(
        source='event.title',
        read_only=True
    )

    # 🔹 WRITE-ONLY INPUT FIELDS (Teacher upload)
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True
    )
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        write_only=True
    )

    class Meta:
        model = Performance
        fields = [
            'id',

            # input
            'student',
            'event',

            # output
            'student_name',
            'school_name',
            'event_title',

            # common
            'title',
            'description',
            "photo",
            'video',
            'duration_seconds',
            'status',
            'submitted_at',
        ]

        read_only_fields = [
            'status',
            'submitted_at',
        ]
