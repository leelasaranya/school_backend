from django.utils.timezone import now

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,ValidationError
from rest_framework.decorators import api_view, permission_classes

from accounts.permissions import (
    IsSchoolAdmin,
    IsStudent,
    IsTeacher
)

from .models import Event, StudentEventInterest, Announcement
from .serializers import EventSerializer
from performances.models import Performance


# =========================
# STATUS SYNC
# =========================
def sync_event_status():
    current = now()

    Event.objects.filter(
        start_time__gt=current
    ).exclude(status='upcoming').update(status='upcoming')

    Event.objects.filter(
        start_time__lte=current,
        end_time__gte=current
    ).exclude(status='live').update(status='live')

    Event.objects.filter(
        end_time__lt=current
    ).exclude(status='completed').update(status='completed')


# =========================
# SCHOOL ADMIN → EVENT CRUD
# =========================
class SchoolAdminEventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        sync_event_status()
        return Event.objects.filter(
            school=self.request.user.school_admin_profile.school,
            is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.school_admin_profile.school
        )

    def perform_update(self, serializer):
        event = self.get_object()
        if event.school != self.request.user.school_admin_profile.school:
            raise PermissionDenied("You can update only your school events")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.school != self.request.user.school_admin_profile.school:
            raise PermissionDenied("You can delete only your school events")
        instance.delete()


# =========================
# PUBLIC EVENT LISTS
# =========================
class AllEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sync_event_status()
        events = Event.objects.filter(is_active=True)
        return Response(EventSerializer(events, many=True).data)


class UpcomingEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sync_event_status()
        events = Event.objects.filter(status='upcoming', is_active=True)
        return Response(EventSerializer(events, many=True).data)


class LiveEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sync_event_status()
        events = Event.objects.filter(status='live', is_active=True)
        return Response(EventSerializer(events, many=True).data)


class CompletedEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sync_event_status()
        events = Event.objects.filter(status='completed', is_active=True)
        return Response(EventSerializer(events, many=True).data)


# =========================
# STUDENT → INTEREST ONLY
# =========================

class StudentEventInterestAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")

        student = request.user.student_profile

        # ✅ 1️⃣ INTRA EVENT → SAME SCHOOL ONLY (FIRST)
        if event.event_type == "intra":
            if student.school != event.school:
                raise PermissionDenied(
                    "You are not eligible for this event"
                )

        # ✅ 2️⃣ ALREADY SUBMITTED (SECOND)
        if StudentEventInterest.objects.filter(
            student=student,
            event=event
        ).exists():
            raise ValidationError("Already submitted")

        # ✅ 3️⃣ CREATE INTEREST
        StudentEventInterest.objects.create(
            student=student,
            event=event
        )

        return Response(
            {"message": "Interest submitted successfully"},
            status=201
        )

# TEACHER → VIEW INTERESTED STUDENTS
# =========================
class TeacherInterestedStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, event_id):
        teacher = request.user.teacher_profile

        interests = StudentEventInterest.objects.filter(
            event_id=event_id,
            student__school=teacher.school,
        )

        data = [
            {
                "student_id": i.student.id,
                "student_name": i.student.user.username,
                "grade": i.student.grade,
                "section": i.student.section
            }
            for i in interests
        ]

        return Response({
            "event_id": event_id,
            "total_students": len(data),
            "students": data
        })


# =========================
# ANNOUNCEMENTS (PUBLIC)
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def live_announcements(request, event_id):
    announcements = Announcement.objects.filter(
        event_id=event_id
    ).order_by("-created_at")[:10]

    return Response([
        {
            "user": "System",
            "message": a.message,
            "time": a.created_at.strftime("%H:%M")
        }
        for a in announcements
    ])
