from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserAuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserProfileSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
