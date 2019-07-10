from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from v1.accounts.models.user import User
from v1.accounts.serializers.user import UserSerializerLogin


# login
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def post(request):
        """
        Get user data and API token
        """

        user = get_object_or_404(User, username=request.data.get('username'))
        user = authenticate(username=user.username, password=request.data.get('password'))
        if user:
            serializer = UserSerializerLogin(user)
            User.objects.filter(id=user.id).update(last_ip=request.META['REMOTE_ADDR'])
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
