from django.db import models

# Create your models here.
from django.db import models
from schools.models import Student, Teacher
from events.models import Event

class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "event")
