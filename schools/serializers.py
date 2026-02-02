from rest_framework import serializers
from .models import School, SchoolAdmin, Teacher, Student


# =========================
# SCHOOL
# =========================
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


# =========================
# SCHOOL ADMIN
# =========================
class SchoolAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAdmin
        fields = "__all__"


# =========================
# SCHOOL DROPDOWN
# =========================
class SchoolDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name"]


# =========================
# TEACHER
# =========================
class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    school = serializers.CharField(
        source="school.name",
        read_only=True
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "user",
            "username",
            "school",
            "employee_id",
            "department",
            "subject",
            "qualification",
            "experience_years",
        ]
        extra_kwargs = {
            "user": {"write_only": True}
        }

    def validate_user(self, user):
        # ONLY on CREATE
        if self.instance is None:
            if Teacher.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    "This user is already linked to a teacher."
                )
        return user


# =========================
# STUDENT  ✅ FIXED
# =========================


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    school = serializers.CharField(
        source="school.name",
        read_only=True
    )

    assigned_teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        required=False,
        allow_null=True
    )

    # 🔥 THIS FIX IS REQUIRED
    assigned_teacher_name = serializers.CharField(
        source="assigned_teacher.user.username",
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "username",
            "school",
            "assigned_teacher",
            "assigned_teacher_name",   # 🔥 MUST BE INCLUDED
            "admission_number",
            "grade",
            "section",
            "roll_number",
            "guardian_name",
            "guardian_phone",
            "admission_date",
            "is_active",
        ]
        extra_kwargs = {
            "user": {"write_only": True}
        }

    def validate_user(self, user):
        if self.instance is None:
            if Student.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    "User already linked to student"
                )
        return user
