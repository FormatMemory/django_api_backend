from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.follows.models.follow_tag import FollowTag 
from v1.follows.serializers.follow_tag import FollowTagSerializer, FollowTagSerializerCreate, FollowTagSerializerDelete
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated


# follow_tag/{id}
class FollowTagView(APIView):

    @staticmethod
    def post(request, id):
        """
        Create follow record
        """

        serializer = FollowTagSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(FollowTagSerializerCreate(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #follow_tag/{id}?follower=0/1
    @staticmethod
    def get(request, id):
        """
        List one user's all followings tags or tags all followers
        ?follower=0/1
        """

        # paginate_by = 10
        try:
            isFollower = int(request.query_params.get('follower'))
            if isFollower == 0:
                follows = FollowTag.objects.all().filter(user_id=id)
            elif isFollower == 1:
                follows = FollowTag.objects.all().filter(follow_tag_id=id)
            else:
                Response([], status.HTTP_400_BAD_REQUEST)
        except:
            return Response([], status.HTTP_400_BAD_REQUEST)
        return Response(FollowTagSerializer(follows, many=True).data)

# follow_tag/{follow_id}
class FollowTagDetialView(APIView):

    @staticmethod
    def get(request, follow_id):
        """
        List one follow record
        """

        following = get_object_or_404(FollowTag, pk=follow_id)
        # paginate_by = 10
        return Response(FollowTagSerializer(following).data)

    @staticmethod
    def delete(request, follow_id):
        """
        Delete follow
        """

        follow = get_object_or_404(FollowTag, pk=follow_id)
        if follow.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #@staticmethod
    # @action(methods=['get'], detail=True, permission_classes=[IsAdminOrIsSelf], \
    #     url_path='change-password', url_name='change_password')