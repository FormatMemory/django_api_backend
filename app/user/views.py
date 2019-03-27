from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
# from django.core.serializers import serialize
# from django.core.serializers.json import DjangoJSONEncoder

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
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

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


# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, User):
#             return str(obj)
#         return super().default(obj)


# class UserListView(APIView):
#     """
#     List all users in the system

#     * Need token autherized
#     * Only admin can access this
#     """
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)

#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         # users_base_info = [str(user) for user in User.objects.all()]
#         users_base_info = serialize(
#                                     'json',
#                                     User.objects.all(),
#                                     cls=LazyEncoder
#                                 )
#         return Response(
#                         users_base_info,
#                         status=status.HTTP_200_OK
#                         )

class UserListView(GenericViewSet, ListModelMixin):
    """
    List all users in the system

    * Need token autherized
    * Only admin can access this
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Return objects for current user"""
        queryset = self.queryset
        if self.request.query_params:
            for para in self.request.query_params:
                if para not in ["email", "pk", "name"]:
                    return None
            if "email" in self.request.query_params:
                queryset = queryset.filter(
                    email=self.request.query_params.get("email")
                ).order_by('-name')
            elif "pk" in self.request.query_params:
                try:
                    pk_val = int(self.request.query_params.get("pk"))
                    queryset = queryset.filter(
                            pk=pk_val
                        ).order_by('-name')
                except Exception:
                    # raise(ValueError, _("pk Value is invalid"))
                    return None
            elif "name" in self.request.query_params:
                queryset = queryset.filter(
                            name=self.request.query_params.get("name")
                        ).order_by('-name')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as err:
            return Response("Error: " + err, status=status.HTTP_200_OK)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
