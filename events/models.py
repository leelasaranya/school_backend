from django.db import models
from django.utils.timezone import now
from schools.models import Student, School


# =========================
# CHOICES
# =========================

STATUS_CHOICES = (
    ('upcoming', 'Upcoming'),
    ('live', 'Live'),
    ('completed', 'Completed'),
)

EVENT_TYPE_CHOICES = (
    ('intra', 'Intra School'),
    ('inter', 'Inter School'),
)


# =========================
# EVENT MODEL
# =========================

class Event(models.Model):
    # 🔹 HOST SCHOOL (event created by this school)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="events"
    )

    # 🔹 BASIC INFO
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    rules = models.TextField()

    # 🔹 EVENT TYPE
    event_type = models.CharField(
        max_length=10,
        choices=EVENT_TYPE_CHOICES,
        default='intra'
    )

    # 🔹 TIMING
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # 🔹 PARTICIPATION LIMIT
    max_participants = models.IntegerField()

    # 🔹 STATUS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )

    # 🔹 SYSTEM
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_status(self):
        current = now()
        if current < self.start_time:
            self.status = 'upcoming'
        elif self.start_time <= current <= self.end_time:
            self.status = 'live'
        else:
            self.status = 'completed'
        self.save(update_fields=['status'])

    def __str__(self):
        return self.title


# =========================
# STUDENT INTEREST MODEL
# (Student ONLY shows interest)
# =========================

class StudentEventInterest(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="event_interests"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="student_interests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.user.username} interested in {self.event.title}"


# =========================
# ANNOUNCEMENTS
# =========================

class Announcement(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement - {self.event.title}"
