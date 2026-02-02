from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.permissions import IsAdmin, IsSchoolAdmin
from rest_framework.permissions import AllowAny
from accounts.models import Profile


from .serializers import (
    PublicRegisterSerializer,
    AdminCreateUserSerializer,
    SchoolAdminCreateUserSerializer,
    ProfileSerializer,
    SchoolAdminUserListSerializer
)
from accounts.permissions import IsAdmin
class PublicRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PublicRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Public user registered successfully"})
class AdminCreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created successfully"})
class SchoolAdminCreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def post(self, request):
        serializer = SchoolAdminCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created successfully"})

class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)



class SchoolAdminUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        # 🔥 only users created by this school admin
        users = Profile.objects.filter(
            role__in=["student", "teacher"]
        ).order_by("-id")

        serializer = SchoolAdminUserListSerializer(users, many=True)
        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from schools.models import SchoolAdmin
from accounts.permissions import IsAdmin

class SchoolAdminAssignAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    # 🔹 GET → list all school_admin users with assign status
    def get(self, request):
        admins = User.objects.filter(profile__role="school_admin")

        assigned_admins = set(
            SchoolAdmin.objects.values_list("user_id", flat=True)
        )

        data = []
        for u in admins:
            data.append({
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_assigned": u.id in assigned_admins
            })

        return Response(data)

    # 🔹 POST → assign school admin
    def post(self, request):
        school_id = request.data.get("school")
        user_id = request.data.get("user")

        if not school_id or not user_id:
            return Response(
                {"detail": "School and user are required"},
                status=400
            )

        if SchoolAdmin.objects.filter(user_id=user_id).exists():
            return Response(
                {"detail": "This admin is already assigned"},
                status=400
            )

        if SchoolAdmin.objects.filter(school_id=school_id).exists():
            return Response(
                {"detail": "This school already has an admin"},
                status=400
            )

        SchoolAdmin.objects.create(
            school_id=school_id,
            user_id=user_id
        )

        return Response({"message": "School admin assigned successfully"})
