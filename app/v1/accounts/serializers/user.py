from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from v1.accounts.models.profile import Profile
from v1.accounts.models.user import User
from v1.utils import constants
from v1.utils.permissions import is_administrator, is_moderator
from v1.accounts.serializers.profile import ProfileSerializer

class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'status',)

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    # libraries = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'status', 'profile', 'role', )

    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """

        profile, created = Profile.objects.get_or_create(user=user)
        return ProfileSerializer(profile, read_only=True).data

    @staticmethod
    def get_role(user):
        """
        Get user role
        """

        if is_administrator(user):
            return constants.USER_ROLE_ADMINISTRATOR
        if is_moderator(user):
            return constants.USER_ROLE_MODERATOR


class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        """
        Administrator permissions needed
        """
        if User.objects.get(username=data.username).exist():
            raise serializers.ValidationError(constants.USER_OR_NICKNAME_EXIST)

        ## enable everyone to create user
        # if not is_administrator(self.context['request'].user):
        #     raise serializers.ValidationError(constants.PERMISSION_ADMINISTRATOR_REQUIRED)
        
        return data

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """

        validate_password(password)
        return password


class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile', 'role', 'token', 'status')


class UserSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)
