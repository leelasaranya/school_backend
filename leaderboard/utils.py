from django.db.models import Avg
from performances.models import Performance
from evaluations.models import Evaluation
from voting.models import Vote

JURY_WEIGHT = 0.7
PUBLIC_WEIGHT = 0.3


def calculate_event_leaderboard(event):
    performances = Performance.objects.filter(
        event=event,
        status='approved'
    )

    leaderboard = []

    for perf in performances:
        jury_avg = Evaluation.objects.filter(
            performance=perf
        ).aggregate(avg=Avg('total_score'))['avg'] or 0

        votes = Vote.objects.filter(
            performance=perf
        ).count()

        final_score = (
            jury_avg * JURY_WEIGHT +
            votes * PUBLIC_WEIGHT
        )

        leaderboard.append({
            "performance": perf,
            "student": perf.student,
            "school": perf.student.school,
            "jury_avg": round(jury_avg, 2),
            "votes": votes,
            "final_score": round(final_score, 2),
        })

    leaderboard.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    for idx, item in enumerate(leaderboard, start=1):
        item["rank"] = idx

    return leaderboard
