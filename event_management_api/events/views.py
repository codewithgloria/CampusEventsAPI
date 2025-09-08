from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from users.models import CustomUser
from .permissions import IsFacultyOrAdmin, IsOrganizerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date_time')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location', 'organizer']
    search_fields = ['title', 'description']
    ordering_fields = ['date_time', 'created_at']

    def get_queryset(self):
        queryset = Event.objects.all()
        upcoming = self.request.query_params.get('upcoming')
        if upcoming == 'true':
            queryset = queryset.filter(date_time__gt=timezone.now())
        elif upcoming == 'false':
            queryset = queryset.filter(date_time__lt=timezone.now())
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsFacultyOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOrganizerOrReadOnly]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Prevent double registration
        if Registration.objects.filter(user=user, event=event).exists():
            return Response(
                {'error': 'You are already registered for this event.'},
                status=400
            )

        # Create registration
        registration = Registration.objects.create(user=user, event=event)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['get'], url_path='registrations')
    def list_registrations(self, request, pk=None):
        event = self.get_object()
        registrations = event.registrations.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class MyEventsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)