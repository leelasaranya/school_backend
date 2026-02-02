
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("school_admin", "School Admin"),
        ("judge", "Judge"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
