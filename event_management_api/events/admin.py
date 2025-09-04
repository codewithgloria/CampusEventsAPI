from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'date_time', 'category', 'is_upcoming']
    list_filter = ['category', 'date_time', 'organizer']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date_time'

    def is_upcoming(self, obj):
        return obj.date_time > timezone.now()
    is_upcoming.boolean = True