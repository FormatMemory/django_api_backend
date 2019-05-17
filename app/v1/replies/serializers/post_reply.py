from rest_framework import serializers
from v1.accounts.serializers.user import UserSerializer
from v1.replies.models.post_reply import PostReply
from v1.votes.models.post_reply_vote import PostReplyVote


class PostReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post_reply_upper_votes_count = serializers.SerializerMethodField()
    post_reply_down_votes_count = serializers.SerializerMethodField()

    class Meta:
        model = PostReply
        fields = '__all__'

    @staticmethod
    def get_post_reply_down_votes_count(post_reply):
        return PostReplyVote.objects.filter(post_reply=post_reply, value=-1).count()

    @staticmethod
    def get_post_reply_upper_votes_count(post_reply):
        return PostReplyVote.objects.filter(post_reply=post_reply, value=1).count()

class PostReplySerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = PostReply
        fields = '__all__'

    def validate_user(self, user):
        """
        Validate authenticated user
        """

        if user != self.context['request'].user:
            raise serializers.ValidationError('You can not create post replies for other users')
        return user


class PostReplySerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = PostReply
        exclude = ('post', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit post replies from other users')
        return data
