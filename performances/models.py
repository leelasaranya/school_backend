from django.db import models
from schools.models import Student, SchoolAdmin, Teacher
from events.models import Event

class Performance(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='performance_photos/',
        null=True,
        blank=True
    )

    video = models.FileField(upload_to='performances/')
    duration_seconds = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 🔥 NEW (IMPORTANT)
    uploaded_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_performances"
    )

    approved_by = models.ForeignKey(
        SchoolAdmin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.user.username} - {self.event.title}"
