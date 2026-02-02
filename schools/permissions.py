from rest_framework.permissions import BasePermission


class HasProfileRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'profile'):
            return False

        return request.user.profile.role in self.allowed_roles


class IsAdmin(HasProfileRole):
    allowed_roles = ['admin']


class IsSchoolAdmin(HasProfileRole):
    allowed_roles = ['school_admin']


class IsTeacher(HasProfileRole):
    allowed_roles = ['teacher']


class IsStudent(HasProfileRole):
    allowed_roles = ['student']


class IsJudge(HasProfileRole):
    allowed_roles = ['judge']


class IsTeacherOrSchoolAdmin(HasProfileRole):
    allowed_roles = ['teacher', 'school_admin']
