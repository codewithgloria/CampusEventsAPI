from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# user roles
ROLE_CHOICES = [
    ('student', 'Student'),
    ('faculty', 'Faculty'),
    ('admin', 'Admin'),
]

class CustomUser(AbstractUser):
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )
    department = models.CharField(max_length=100, blank=True)

    objects = CustomUserManager()  # assigned custom manager

    # to fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"