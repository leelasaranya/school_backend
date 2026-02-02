from django.db import models
from performances.models import Performance
from django.contrib.auth.models import User


class Evaluation(models.Model):
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='evaluations'
    )
    judge = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_scores'
    )

    creativity = models.IntegerField()
    technique = models.IntegerField()
    presentation = models.IntegerField()

    total_score = models.IntegerField()
    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('performance', 'judge')

    def save(self, *args, **kwargs):
        self.total_score = (
            self.creativity +
            self.technique +
            self.presentation
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.performance} - {self.judge.username}"
