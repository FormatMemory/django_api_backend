from rest_framework import serializers
from v1.follows.models.follow_tag import FollowTag


class FollowTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowTag
        fields = '__all__'


class FollowTagSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FollowTag
        fields = '__all__'


class FollowTagSerializerDelete(serializers.ModelSerializer):

    class Meta:
        model = FollowTag
        exclude = ('user',)

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not delete follow tag for other users')
        return data
