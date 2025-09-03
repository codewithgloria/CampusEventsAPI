from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('education', 'Education'),
        ('social', 'Social'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date_time > timezone.now()