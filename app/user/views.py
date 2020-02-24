from rest_framework import generics

from user.serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer
