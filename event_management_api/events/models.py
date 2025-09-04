from django.db import models
from django.conf import settings
from django.utils import timezone

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('social', 'Social'),
        ('career', 'Career'),
        ('sports', 'Sports'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    # way to reference custom user
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date_time > timezone.now()
    
    class Meta:
        ordering = ['-date_time']

class Registration(models.Model):
    STATUS_CHOICES = [
        ('attending', 'Attending'),
        ('waitlist', 'Waitlist'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='attending')

    class Meta:   
        unique_together = ('user', 'event')  # prevents duplicate registrations
        ordering = ['registered_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"     