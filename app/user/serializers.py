from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'groups',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new user with encrypted password and returt it"""
        groups_data = validated_data.pop('groups')
        user = get_user_model().objects.create_user(**validated_data)
        if groups_data:
            for group in groups_data:
                user.groups.add(group)

        return user


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('name', 'content_type', 'codename')


class UserDetailSerializer(serializers.ModelSerializer):

    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )

    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all()
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'groups', 'user_permissions',)
        read_only_fields = ('id',)
