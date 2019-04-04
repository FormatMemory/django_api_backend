from rest_framework import serializers
from v1.categories.models.category import Category
from v1.utils.permissions import is_administrator
from v1.utils import constants
from v1.posts.models.post import Post
from v1.posts.serializers.post import PostSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'


class CategoryFullSerializer(CategorySerializer):
    category_posts = serializers.SerializerMethodField()
    category_posts_count =  serializers.SerializerMethodField()
    class Meta:
        model = Category 
        fields = '__all__'

    @staticmethod
    def get_category_posts(cate):
        return PostSerializer(Post.objects.filter(category__id__contains=cate.id), many=True).data

    @staticmethod
    def get_category_posts_count(cate):
        return Post.objects.filter(category__id__contains=cate.id).count()


class CategorySerializerCreate(CategorySerializer):

    class Meta:
        model = Category 
        fields = '__all__'
        exclude = ('post', )

    def validate(self, data):
        """
        Administrator permissions needed
        """
        if not is_administrator(self.context['request'].user):
            raise serializers.ValidationError(constants.PERMISSION_ADMINISTRATOR_REQUIRED)
        
        return data


class CategorySerializerUpdate(CategorySerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        """
        administrator permissions needed
        """
        if not is_administrator(self.context['request'].user):
            raise serializers.ValidationError(constants.PERMISSION_ADMINISTRATOR_REQUIRED)
        
        return data
