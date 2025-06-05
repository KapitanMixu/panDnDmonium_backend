# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('dm', 'Dungeon Master'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
