from rest_framework import serializers
from v1.user_page_views.models.user_page_view import UserPageView 


class UserPageViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPageView 
        fields = '__all__'


class UserPageViewSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserPageView 
        fields = '__all__'


class UserPageViewSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = UserPageView
        exclude = ('post', 'user', 'created', 'ip', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit page views from other users')
        return data
