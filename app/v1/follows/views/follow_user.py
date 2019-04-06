from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.follows.models.follow_user import FollowUser
from v1.follows.serializers.follow_user import FollowUserSerializer, FollowUserSerializerCreate, FollowUserSerializerDelete
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated


# follow_user/{user_id}
class FollowUserView(APIView):
    
    @staticmethod
    def post(request, user_id):
        """
        Create follow record
        """

        serializer = FollowUserSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(FollowUserSerializerCreate(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #follow_user/{user_id}?follower=0/1
    def get(self, request, user_id):
        """
        List one user's all followings or followers
        ?follower=0/1
        """

        # paginate_by = 10
        try:
            isFollower = int(request.query_params.get('follower'))
            if isFollower == 0:
                follows = FollowUser.objects.all().filter(user_id=user_id)
            elif isFollower == 1:
                follows = FollowUser.objects.all().filter(follow_user_id=user_id)
            else:
                Response([], status.HTTP_400_BAD_REQUEST)
        except:
            return Response([], status.HTTP_400_BAD_REQUEST)
        return Response(FollowUserSerializer(follows, many=True).data)


# follow_user/detail/{follow_id}
class FollowUserDetailView(APIView):

    @staticmethod
    def get(request, follow_id):
        """
        List one follow record
        """

        following = get_object_or_404(FollowUser, pk=follow_id)
        # paginate_by = 10
        return Response(FollowUserSerializer(following).data)

    @staticmethod
    def delete(request, follow_id):
        """
        Delete follow
        """

        follow = get_object_or_404(FollowUser, pk=follow_id)
        if follow.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
