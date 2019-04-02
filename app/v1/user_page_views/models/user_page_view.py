from django.db import models
from v1.posts.models.post import Post
from v1.user_page_views.models.view import View


class UserPageView(View):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'page_view'
        unique_together = ('post', 'user', 'start_time')

    def __str__(self):
        return f'post: {self.post.id} - user: {self.user.nick_name} - time: {self.start_time}'
