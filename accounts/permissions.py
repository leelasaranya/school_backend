'''from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # ✅ Admin override
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            return True

        return (
            hasattr(request.user, 'profile') and
            request.user.profile.role in self.allowed_roles
        )


class IsAdmin(HasRole): allowed_roles = ['admin']
class IsSchoolAdmin(HasRole): allowed_roles = ['school_admin']
class IsTeacher(HasRole): allowed_roles = ['teacher']
class IsStudent(HasRole): allowed_roles = ['student']
class IsJudge(HasRole): allowed_roles = ['judge']
class IsPublic(HasRole): allowed_roles = ['public']
class IsTeacherOrSchoolAdmin(HasRole): allowed_roles = ['teacher', 'school_admin']
'''
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Only admin users can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsSchoolAdmin(BasePermission):
    message = "Only school admins can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "school_admin_profile")
        )


class IsTeacher(BasePermission):
    message = "Only teachers can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "teacher_profile")
        )


class IsStudent(BasePermission):
    message = "Only students can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "student_profile")
        )


class IsTeacherOrSchoolAdmin(BasePermission):
    message = "Only teachers or school admins can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                hasattr(request.user, "teacher_profile") or
                hasattr(request.user, "school_admin_profile")
            )
        )
class IsJudge(BasePermission):
    message = "Only judges can access this."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "profile") and
            request.user.profile.role == "judge")




class IsPublic(BasePermission):
    message = "Only public users can vote."

    def has_permission(self, request, view):
        user = request.user

        # 🔒 Must be logged in
        if not user or not user.is_authenticated:
            return False

        # 🔒 Block system roles
        if user.is_superuser:
            return False

        if hasattr(user, "school_admin_profile"):
            return False

        if hasattr(user, "teacher_profile"):
            return False

        if hasattr(user, "judge_profile"):
            return False

        # ✅ Public user allowed
        return True
