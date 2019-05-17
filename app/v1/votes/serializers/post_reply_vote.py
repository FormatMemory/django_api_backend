from rest_framework import serializers
from v1.votes.models.post_reply_vote import PostReplyVote 


class PostReplyVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReplyVote 
        fields = '__all__'


class PostReplyVoteSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostReplyVote 
        fields = '__all__'


class PostReplyVoteSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = PostReplyVote 
        exclude = ('post_reply', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit post reply votes from other users')
        return data
