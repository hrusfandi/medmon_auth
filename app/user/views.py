from rest_framework import generics

from user.serializers import UserSerializer, GroupSerializer, \
                             PermissionSerializer, UserDetailSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from rest_framework.permissions import IsAuthenticated


class UserView(generics.ListCreateAPIView):
    """Create a new user in the system"""
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GroupView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
