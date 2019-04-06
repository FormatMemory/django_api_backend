from rest_framework import serializers
from v1.follows.models.follow_user import FollowUser
from v1.accounts.serializers.user import UserSimpleSerializer


class FollowUserSerializer(serializers.ModelSerializer):

    user = UserSimpleSerializer()
    follow_user = UserSimpleSerializer() 
    class Meta:
        model = FollowUser
        fields = ('user', 'follow_user', 'created_time')


class FollowUserSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FollowUser
        fields = '__all__'

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].follow_user:
            raise serializers.ValidationError('You can not follow yourself')
        return data

class FollowUserSerializerDelete(serializers.ModelSerializer):

    class Meta:
        model = FollowUser
        exclude = ('user',)

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not delete follow for other users')
        return data
