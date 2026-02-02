from django.db import models
from django.contrib.auth.models import User
from performances.models import Performance

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'performance')

    def __str__(self):
        return f"{self.user.username} → {self.performance.id}"
