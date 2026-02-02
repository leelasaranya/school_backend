from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound

from events.models import Event
from .utils import calculate_event_leaderboard
from .serializers import LeaderboardSerializer


class EventWinnerAPIView(APIView):
    permission_classes = [AllowAny]   # ✅ PUBLIC ACCESS

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise NotFound("Event not found")

        # 🔐 IMPORTANT RULE
        if event.status != 'completed':
            raise PermissionDenied(
                "Winner will be announced after event completion"
            )

        leaderboard = calculate_event_leaderboard(event)

        if not leaderboard:
            return Response({"message": "No performances available"})

        winner = leaderboard[0]

        data = {
            "rank": 1,
            "student": winner["student"].user.username,
            "school": winner["school"].name,
            "performance_id": winner["performance"].id,

            "performance_title": winner["performance"].title,
            "jury_avg": winner["jury_avg"],
            "votes": winner["votes"],
            "final_score": winner["final_score"],
        }

        return Response(data)
class EventLeaderboardAPIView(APIView):
    permission_classes = [AllowAny]   # ✅ PUBLIC

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise NotFound("Event not found")

        # 🔐 Show leaderboard only after completion
        if event.status != 'completed':
            raise PermissionDenied(
                "Leaderboard will be available after event completion"
            )

        leaderboard = calculate_event_leaderboard(event)

        response = []
        for item in leaderboard:
            response.append({
                "rank": item["rank"],
                "student": item["student"].user.username,
                "school": item["school"].name,
                "performance_id": item["performance"].id,

                "performance_title": item["performance"].title,
                "jury_avg": item["jury_avg"],
                "votes": item["votes"],
                "final_score": item["final_score"],
            })

        return Response(response)
class LatestLeaderboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        event = (
            Event.objects
            .filter(status="completed")   # ✅ remove is_active
            .order_by("-end_time")
            .first()
        )

        if not event:
            raise NotFound("No completed events found")

        leaderboard = calculate_event_leaderboard(event)

        data = [
            {
                "rank": item["rank"],
                "student": item["student"].user.username,
                "school": item["school"].name,
                "performance_id": item["performance"].id,
                "performance_title": item["performance"].title,
                "jury_avg": item["jury_avg"],
                "votes": item["votes"],
                "final_score": item["final_score"],
            }
            for item in leaderboard
        ]

        return Response({
            "event_title": event.title,
            "leaderboard": data
        })

class CurrentEventWinnerAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 🔥 Latest completed + active event
        event = (
            Event.objects.filter(
                status="completed",
                is_active=True
            )
            .order_by("-end_time")
            .first()
        )

        if not event:
            raise NotFound("No completed active event found")

        leaderboard = calculate_event_leaderboard(event)

        if not leaderboard:
            return Response({"message": "No performances available"})

        winner = leaderboard[0]

        data = {
            "event_title": event.title,
            "rank": 1,
            "student": winner["student"].user.username,
            "school": winner["school"].name,
            "performance_id": winner["performance"].id,

            "performance_title": winner["performance"].title,
            "jury_avg": winner["jury_avg"],
            "votes": winner["votes"],
            "final_score": winner["final_score"],
            "photo": (
                request.build_absolute_uri(winner["performance"].photo.url)
                if winner["performance"].photo
                else None
            ),

        }

        return Response(data)
