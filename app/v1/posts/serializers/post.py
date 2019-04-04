from rest_framework import serializers
from v1.accounts.serializers.user import UserSerializer
from v1.posts.models.post import Post
from v1.replies.models.post_reply import PostReply
from v1.replies.serializers.post_reply import PostReplySerializer
from v1.votes.models.post_vote import PostVote
from v1.votes.serializers.post_vote import PostVoteSerializer
from v1.user_page_views.models.user_page_view import UserPageView
from v1.user_page_views.serializers.user_page_view import UserPageViewSerializer
from v1.categories.models.category import Category

class PostCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category 
        fields = ('title',)


class PostSerializer(serializers.ModelSerializer):
    post_reply_count = serializers.SerializerMethodField()
    post_votes = PostVoteSerializer(many=True, read_only=True)
    post_upper_votes_count = serializers.SerializerMethodField()
    post_down_votes_count = serializers.SerializerMethodField()
    user_page_view_count = serializers.SerializerMethodField()
    login_user_page_view_count = serializers.SerializerMethodField()
    go_to_link = serializers.SerializerMethodField()
    login_user_go_to_link = serializers.SerializerMethodField()
    user = UserSerializer()
    category = PostCategorySerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
        ordering = ['-post_total_view', '-post_votes', '-created_time']

    @staticmethod
    def get_post_reply_count(post):
        return PostReply.objects.filter(post=post).count()

    @staticmethod
    def get_user_page_view_count(post):
        return UserPageView.objects.filter(post=post).count()

    @staticmethod
    def get_login_user_page_view_count(post):
        return UserPageView.objects.filter(post=post, user__isnull=False).count()

    @staticmethod
    def get_go_to_link(post):
        return UserPageView.objects.filter(post=post, click_link=True).count()

    @staticmethod
    def get_login_user_go_to_link(post):
        return UserPageView.objects.filter(post=post, click_link=True, user__isnull=False).count()

    @staticmethod
    def get_post_down_votes_count(post):
        return PostVote.objects.filter(post=post, value=-1).count()

    @staticmethod
    def get_post_upper_votes_count(post):
        return PostVote.objects.filter(post=post, value=1).count()

    # @staticmethod
    # def get_post_total_view = Post.objects.filter(post=post)['total_views']

class PostSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('status', 'total_views', 'created_time', 'last_modified',)

class PostSerializerFull(PostSerializer):
    post_replies = PostReplySerializer(many=True, read_only=True)


class PostSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ('user', 'created_time', 'last_modified', )

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit posts from other users')
        return data
