from django.urls import path
from .views import EventLeaderboardAPIView, EventWinnerAPIView,LatestLeaderboardAPIView,CurrentEventWinnerAPIView

urlpatterns = [
    path(
        'events/<int:event_id>/leaderboard/',
        EventLeaderboardAPIView.as_view(),
        name='event-leaderboard'
    ),
    path(
        'events/<int:event_id>/winner/',
        EventWinnerAPIView.as_view(),
        name='event-winner'
    ),
    path(
        'leaderboard/latest/',
        LatestLeaderboardAPIView.as_view(),
        name="latest-leaderboard"
    ),
    path("events/current/winner/", CurrentEventWinnerAPIView.as_view()),

]
