from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.votes.models.post_reply_vote import PostReplyVote
from v1.votes.serializers.post_reply_vote import PostReplyVoteSerializer, PostReplyVoteSerializerCreate, PostReplyVoteSerializerUpdate


# reply_votes
class PostReplyVoteView(APIView):

    @staticmethod
    def post(request):
        """
        Create reply vote
        """

        serializer = PostReplyVoteSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(PostReplyVoteSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reply_votes/{reply_vote_id}
class PostReplyVoteDetail(APIView):

    @staticmethod
    def patch(request, reply_vote_id):
        """
        Update reply vote
        """

        post_reply_vote = get_object_or_404(PostReplyVote, pk=reply_vote_id)
        serializer = PostReplyVoteSerializerUpdate(post_reply_vote, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostReplyVoteSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, reply_vote_id):
        """
        Delete reply vote
        """

        post_reply_vote = get_object_or_404(PostReplyVote, pk=reply_vote_id)
        if post_reply_vote.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_reply_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
