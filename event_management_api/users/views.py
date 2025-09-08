from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.views import APIView
from users.models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # extract username from response data
        username = response.data['username']

        # get the user from the database
        User = get_user_model()
        user = User.objects.get(username=username)
     
        # token created for user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': response.data,
            'token': token.key
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user