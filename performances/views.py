from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from schools.models import Student
from events.models import Event
from registrations.models import Registration   # ✅ REQUIRED
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import (
    IsTeacher, IsSchoolAdmin, IsJudge, IsAdmin
)

from .models import Performance
from .serializers import PerformanceSerializer


# =========================
# TEACHER → UPLOAD PERFORMANCE
# =========================
class TeacherPerformanceUploadViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        teacher = self.request.user.teacher_profile
        return Performance.objects.filter(
            uploaded_by=teacher
        )

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        event = serializer.validated_data["event"]
        student = serializer.validated_data["student"]

        # 🔒 Event must be LIVE
        if event.status != "live":
            raise PermissionDenied("Upload allowed only during LIVE event")

        # 🔒 Student must be same school
        if student.school != teacher.school:
            raise PermissionDenied("Other school student")

        # 🔒 Assigned teacher only
        if student.assigned_teacher != teacher:
            raise PermissionDenied("You are not assigned teacher")

        # 🔒 One upload per student per event
        if Performance.objects.filter(student=student, event=event).exists():
            raise PermissionDenied("Already uploaded for this event")

        serializer.save(
            uploaded_by=teacher,
            status="pending"
        )

# =========================
# SCHOOL ADMIN → VIEW PERFORMANCES
# =========================
class SchoolAdminPerformanceViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]
    http_method_names = ['get']

    def get_queryset(self):
        return Performance.objects.filter(
            event__school=self.request.user.school_admin_profile.school
        )


# =========================
# SCHOOL ADMIN → APPROVE / REJECT
# =========================
class SchoolAdminApprovePerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def post(self, request, performance_id):
        try:
            performance = Performance.objects.get(id=performance_id)
        except Performance.DoesNotExist:
            return Response({"error": "Performance not found"}, status=404)

        if performance.event.school != request.user.school_admin_profile.school:
            raise PermissionDenied("Not your event")

        action = request.data.get("action")

        if action == 'approve':
            performance.status = 'approved'
            performance.approved_by = request.user.school_admin_profile
        elif action == 'reject':
            performance.status = 'rejected'
            performance.approved_by = None
        else:
            return Response({"error": "Invalid action"}, status=400)

        performance.save()
        return Response({"message": f"Performance {performance.status}"})


# =========================
# JUDGE → VIEW APPROVED
# =========================
class JudgePerformanceViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, IsJudge]
    http_method_names = ['get']

    def get_queryset(self):
        return Performance.objects.filter(
            status='approved',
            event__status='live'
        )


# =========================
# PUBLIC → VIEW APPROVED
# =========================
class PublicPerformanceViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Performance.objects.filter(status='approved')
        event_id = self.request.query_params.get("event")
        if event_id:
            qs = qs.filter(event_id=event_id)
        return qs


# =========================
# SUPER ADMIN → ALL
# =========================
class AdminPerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
class TeacherUploadStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = request.user.teacher_profile
        event_id = request.query_params.get("event")

        if not event_id:
            return Response({"students": []})

        # 🔹 EVENT MUST BE LIVE
        try:
            event = Event.objects.get(id=event_id, status="live")
        except Event.DoesNotExist:
            return Response({"students": []})

        # 🔹 ONLY REGISTERED + ASSIGNED STUDENTS
        registrations = Registration.objects.filter(
            event=event,
            student__assigned_teacher=teacher,
            student__school=teacher.school
        ).select_related("student__user")

        data = []
        for r in registrations:
            s = r.student
            data.append({
                "id": s.id,
                "full_name": s.user.get_full_name() or s.user.username,
                "photo": s.user.photo.url if hasattr(s.user, "photo") and s.user.photo else None,

                "class_name": f"{s.grade} {s.section}",
            })

        return Response({"students": data})