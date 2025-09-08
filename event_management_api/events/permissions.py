from rest_framework import permissions

class IsFacultyOrAdmin(permissions.BasePermission):
    """
    Allow only faculty or admin to create or edit events.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # For POST, PUT, DELETE must be faculty or admin
        return request.user.role in ['faculty', 'admin']


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Only the event organizer can modify or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user


class CanRegister(permissions.BasePermission):
    """
    Only students can register for events.
    """
    def has_permission(self, request, view):
        return request.user.role == 'student'