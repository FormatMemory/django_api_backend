from rest_framework import serializers
from v1.accounts.models.libraries import Library, LibraryItem
from v1.posts.serializers.post import PostSimpleSerializer

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
        ordering = ['-modified_time', 'name']

class LibraryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Library
        fields = '__all__'


class LibraryItemSerializer(serializers.ModelSerializer):
    post = PostSimpleSerializer()
    # library = LibrarySerializer()
    class Meta:
        model = LibraryItem
        fields = ('post', 'created_time', 'modified_time', )
        ordering = ['-created_time']

class LibraryItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = LibraryItem
        fields = '__all__'


class LibraryDetailSerializer(LibrarySerializer):

    library_item = LibraryItemSerializer(many=True)

    class Meta:
        model = Library
        fields = '__all__'

    # @staticmethod
    # def get_post_list(lib):

    #     try:
    #         library_items = LibraryItem.objects.get(library=lib)
    #     except LibraryItem.DoesNotExist:
    #         library_items = [LibraryItem.objects.create(library=lib, user=lib.user)]
    #     return LibraryItemSerializer(library_items, read_only=True, many=True).data

class LibrarySerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Library
        exclude = ('user', 'created_time', 'last_modified', )

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit library from other users')
        return data

class LibraryItemSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = LibraryItem
        exclude = ('user', 'created_time', 'last_modified', )

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit library list from other users')
        return data
