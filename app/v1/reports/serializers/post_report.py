from rest_framework import serializers
from v1.accounts.serializers.user import UserSimpleSerializer
from v1.posts.serializers.post import PostSimpleSerializer
from v1.reports.models.post_report import PostReport
from v1.utils.permissions import is_administrator, is_moderator


class PostReportSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    post = PostSimpleSerializer()
    class Meta:
        model = PostReport
        fields = '__all__'
        ordering = ['status', 'created_time', ]

class PostReportSerializerCreate(PostReportSerializer):

    class Meta:
        model = PostReport
        exclude = ('status', 'auditor', 'created_time', 'last_modified', 'audit_message',)

    def validate_user(self, user):
        """
        Validate authenticated user
        """

        if user != self.context['request'].user:
            raise serializers.ValidationError('You can not create post replies for other users')
        return user

    def validate_description(self, description):
        """
        Validate description
        """

        if not len(self.context['request'].description):
            raise serializers.ValidationError('Report description cannot be empty')
        return description

class PostReportSerializerUpdate(serializers.ModelSerializer):
    auditor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PostReport
        exclude = ('post', 'user', 'created_time', 'auditor')

    def validate(self, data):
        """
        Validate administrator or moderator can update report
        """

        if self.instance.user != self.context['request'].user and \
            not is_administrator(self.context['request'].user) and \
            not is_moderator(self.context['request'].user):
            raise serializers.ValidationError('You can not edit post replies from other users')
        return data
