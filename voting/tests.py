from django.test import TestCase

# Create your tests here.
from django.db import models
from performances.models import Performance
from users.models import User

class Vote(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('performance','user')