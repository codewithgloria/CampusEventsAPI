from rest_framework import serializers
from .models import Event, Registration
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer']

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        event = validated_data['event']

        # Check if event is full
        if event.registrations.count() >= event.capacity:
            validated_data['status'] = 'waitlist'

        return super().create(validated_data)