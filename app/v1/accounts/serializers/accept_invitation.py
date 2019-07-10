from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from v1.accounts.models.profile import Profile
from v1.accounts.models.user import User
from v1.credits.models.invitation import Invitation


class AcceptInvitationSerializer(serializers.Serializer):
    code = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        """
        Create user, set password, update invitation, create profile
        """

        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        Invitation.objects.filter(code=validated_data['code']).update(receiver=user)
        Profile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_code(value):
        """
        Check that invitation code exists and has not been used
        """

        if not Invitation.objects.filter(code=value, receiver__isnull=True):
            raise serializers.ValidationError('Invalid invitation code')
        return value

    @staticmethod
    def validate_username(value):
        """
        Check the username is unique
        """

        if User.objects.filter(username=value):
            raise serializers.ValidationError('username already exists')
        return value

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """

        validate_password(password)
        return password
