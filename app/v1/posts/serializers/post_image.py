from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from v1.accounts.serializers.user import UserSerializer
from v1.posts.models.post import Post
from v1.posts.models.post_image import PostImage
from v1.accounts.serializers.user import UserSerializer
from v1.posts.serializers.post import PostSimpleSerializer

class PostImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSimpleSerializer()
    image = Base64ImageField(required=False)
    post_id = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = '__all__'
        ordering = ['-created_time']
        read_only_fields = ['id', 'user', 'created_time', 'last_modified']

    @staticmethod
    def get_post_id(post_image):
        return Post.objects.filter(post_image=post_image)

    def validate_user(self, user):
        """
        Validate authenticated user
        """

        if user != self.context['request'].user:
            raise serializers.ValidationError('You can not modify post image for other users')
        return user
