from django.db import models
from v1.posts.models.post import Post
from .report import Report


class PostReport(Report):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'post_reports'

    def __str__(self):
        return str(self.user.id) +" - " + self.post.title + " - " + self.status + " - "
