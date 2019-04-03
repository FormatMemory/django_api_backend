from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.user_page_views.models.user_page_view import UserPageView
from v1.user_page_views.serializers.user_page_view import UserPageViewSerializer, UserPageViewSerializerCreate, UserPageViewSerializerUpdate
from v1.filters.user_page_views.user_page_views import user_page_views_filter

# user_page_views
class UserPageViewView(APIView):

    @staticmethod
    def post(request):
        """
        Create user page view
        """

        serializer = UserPageViewSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(UserPageViewSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user_page_views/{user_page_view_id}
class UserPageViewDetail(APIView):

    # @staticmethod
    # def patch(request, user_page_view_id):
    #     """
    #     Update user page view
    #     """

    #     user_page_view = get_object_or_404(UserPageView, pk=user_page_view_id)
    #     if user_page_view.user != request.user:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = UserPageViewSerializerUpdate(user_page_view, data=request.data, context={'request': request}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(UserPageViewSerializer(serializer.instance).data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, user_page_view_id):
        """
        Delete user page view
        """

        user_page_view = get_object_or_404(UserPageView, pk=user_page_view_id)
        if user_page_view.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user_page_view.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get(request):
        """
        Get use view page record
        """

        user_page_views = UserPageView.objects.all()
        user_page_views = user_page_views_filter(request)

        if type(user_page_views) == Response:
            return user_page_views
        return Response(UserPageViewSerializer(user_page_views, many=True).data)