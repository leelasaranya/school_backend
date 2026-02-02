from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=200)
    school_code = models.CharField(max_length=50, unique=True)
    board = models.CharField(max_length=50)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    principal_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    established_year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 🔥 FIXED: ONE SCHOOL → ONE SCHOOL ADMIN
class SchoolAdmin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="school_admin_profile"
    )
    school = models.OneToOneField(   # 🔥 CHANGED FROM ForeignKey
        School,
        on_delete=models.CASCADE,
        related_name="school_admin"
    )

    def __str__(self):
        return f"{self.user.username} - {self.school.name}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="teachers"
    )
    created_by = models.ForeignKey(
        SchoolAdmin,
        on_delete=models.CASCADE,
        related_name="created_teachers"
    )

    employee_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    qualification = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="students"
    )
    created_by = models.ForeignKey(
        SchoolAdmin,
        on_delete=models.CASCADE,
        related_name="created_students"
    )

    # 🔥 NEW FIELD (IMPORTANT)
    assigned_teacher = models.ForeignKey(
    Teacher,
    on_delete=models.SET_NULL,
    null=True,        # ✅ KEEP THIS
    blank=True        # ✅ KEEP THIS
)

    admission_number = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    roll_number = models.IntegerField()

    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)

    admission_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
