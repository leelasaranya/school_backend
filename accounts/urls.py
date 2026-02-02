from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    PublicRegisterAPIView,
    AdminCreateUserAPIView,
    SchoolAdminCreateUserAPIView,
    MyProfileAPIView,
    SchoolAdminUsersAPIView,
    SchoolAdminAssignAPIView
)

urlpatterns = [

    # 🔐 LOGIN (ALL ROLES)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # 🔄 TOKEN REFRESH
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 📝 REGISTER (PUBLIC USERS ONLY)
    path('register/', PublicRegisterAPIView.as_view(), name='public_register'),

    # 👑 ADMIN CREATES USERS (student / teacher / judge / school_admin)
    path('create-user/', AdminCreateUserAPIView.as_view(), name='admin_create_user'),
    path(
    'school-admin/create-user/',
    SchoolAdminCreateUserAPIView.as_view(),
    name='school_admin_create_user'
),
 path(
        "school-admin/users/",
        SchoolAdminUsersAPIView.as_view(),
        name="school_admin_users"
    ),

    # 👤 LOGGED-IN USER DETAILS (ROLE CHECK)
    path('me/', MyProfileAPIView.as_view(), name='my_profile'),
    path(
    "admin/school-admins/",
    SchoolAdminAssignAPIView.as_view()
)

]
