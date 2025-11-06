from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = models.CharField(
        max_length=15,
        choices=(
            ('SuperAdmin', 'SuperAdmin'),
            ('Admin', 'Admin'),
            ('Student', 'Student'),
        ),
        default='Student'
    )
