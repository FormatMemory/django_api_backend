from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _


from core.models import User

class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """
        Retrive and return authenticated user
        """
        return self.request.user

class DeleteTokenView(APIView):
    """
    Logout user, delete token
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def logout(self, request):
            try:
                request.user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):
                pass

            # logout(request)
            return Response({"success": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
    def get(self, request):
        """
        Delete user token
        """
        return self.logout(request)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return str(obj)
        return super().default(obj)


class UserListView(APIView):
    """
    List all users in the system

    * Need token autherized
    * Only admin can access this
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        #users_base_info = [str(user) for user in User.objects.all()]
        users_base_info = serialize('json', User.objects.all(), cls=LazyEncoder)
        return Response(
                        users_base_info,
                        status=status.HTTP_200_OK    
                        )