from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,ValidationError
from .models import Registration
from events.models import Event
from schools.models import Student

from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Registration
from events.models import Event
from schools.models import Student
from events.models import StudentEventInterest
from .serializers import RegistrationSerializer


class RegisterStudentAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 🔐 ONLY TEACHER
        try:
            teacher = request.user.teacher_profile
        except:
            raise PermissionDenied("Only teachers can register students")

        student_id = request.data.get("student")
        event_id = request.data.get("event")

        if not student_id or not event_id:
            raise ValidationError("Student and Event are required")

        # 🔹 FETCH STUDENT
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise ValidationError("Student not found")

        # 🔹 FETCH EVENT
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")

        # 1️⃣ EVENT MUST BE UPCOMING
        if event.status != "upcoming":
            raise ValidationError(
                "Students can be registered only for upcoming events"
            )

        # 2️⃣ INTRA EVENT → SAME SCHOOL ONLY
        if event.event_type == "intra":
            if student.school != event.school:
                raise ValidationError(
                    "This is an intra-school event. Other school students are not allowed."
                )

        # 3️⃣ STUDENT MUST BE ASSIGNED TO A TEACHER
        if not student.assigned_teacher:
            raise ValidationError(
                "This student is not assigned to any teacher"
            )

        # 🔥 MAIN RULE YOU ASKED
        # 4️⃣ STUDENT MUST BELONG TO THIS TEACHER
        if student.assigned_teacher != teacher:
            raise PermissionDenied(
                "You cannot register students who are not assigned to you"
            )

        # 5️⃣ STUDENT MUST HAVE SHOWN INTEREST
        if not StudentEventInterest.objects.filter(
            student=student,
            event=event
        ).exists():
            raise ValidationError(
                "Student has not shown interest in this event"
            )

        # 6️⃣ PREVENT DUPLICATE REGISTRATION
        if Registration.objects.filter(
            student=student,
            event=event
        ).exists():
            raise ValidationError(
                "Student already registered for this event"
            )

        # ✅ CREATE REGISTRATION
        registration = Registration.objects.create(
            student=student,
            event=event,
            registered_by=teacher
        )

        return Response(
            RegistrationSerializer(registration).data,
            status=201
        )


class TeacherRegisteredStudentsForUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = request.user.teacher_profile
        event_id = request.query_params.get("event")

        if not event_id:
            return Response({"students": []})

        # event must be LIVE
        event = Event.objects.filter(id=event_id, status="live").first()
        if not event:
            return Response({"students": []})

        registrations = Registration.objects.filter(
            event=event,
            student__assigned_teacher=teacher
        ).select_related("student__user")

        students = [
            {
                "id": r.student.id,
                "full_name": r.student.user.username,
                "grade": r.student.grade,
                "section": r.student.section,
                "photo": r.student.photo.url if r.student.photo else None
            }
            for r in registrations
        ]

        return Response({"students": students})