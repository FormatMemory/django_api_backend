from django.db import models
from v1.posts.models.post import Post
from v1.user_page_views.models.view import View
from django.conf import settings

class UserPageView(View):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    click_link = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'page_view'
        unique_together = ('post', 'ip', 'created')

    def __str__(self):
        return f'post: {self.post.id} - ip: {self.ip} - created: {self.created}'
