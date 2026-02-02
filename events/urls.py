from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SchoolAdminEventViewSet,
    AllEventsAPIView,
    UpcomingEventsAPIView,
    LiveEventsAPIView,
    CompletedEventsAPIView,
    StudentEventInterestAPIView,
    TeacherInterestedStudentsAPIView,
    live_announcements,
)

router = DefaultRouter()

# 🏫 SCHOOL ADMIN → EVENT CRUD
router.register(
    r'events',
    SchoolAdminEventViewSet,
    basename='events-admin'
)

urlpatterns = [
    # 🌍 PUBLIC EVENTS
    path('events/all/', AllEventsAPIView.as_view()),
    path('events/upcoming/', UpcomingEventsAPIView.as_view()),
    path('events/live/', LiveEventsAPIView.as_view()),
    path('events/completed/', CompletedEventsAPIView.as_view()),

    # 🎓 STUDENT → INTEREST ONLY
    path(
        'events/<int:event_id>/interest/',
        StudentEventInterestAPIView.as_view(),
        name='event-interest'
    ),

    # 🧑‍🏫 TEACHER → VIEW INTERESTED STUDENTS
    path(
        'events/<int:event_id>/interested-students/',
        TeacherInterestedStudentsAPIView.as_view(),
        name='event-interested-students'
    ),

    # 📢 ANNOUNCEMENTS
    path(
        'events/<int:event_id>/announcements/',
        live_announcements,
        name='event-announcements'
    ),
    
]

urlpatterns += router.urls
