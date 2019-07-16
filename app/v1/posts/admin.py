from django.contrib import admin
from .models.post import Post
from .models.post_image import PostImage


admin.site.register(Post)
admin.site.register(PostImage)