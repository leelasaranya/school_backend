from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('school_admin', 'School Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('judge', 'Judge'),
        ('public', 'Public'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100) 
    phone = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
