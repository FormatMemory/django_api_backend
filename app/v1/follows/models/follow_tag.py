from django.db import models
from v1.posts.models.post import Post
from django.conf import settings
from v1.follows.models.follow import Follow
from taggit.models import Tag

class FollowTag(Follow):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,  on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'user_follow_tag'
        unique_together = ('user', 'tag')

    def __str__(self):
        return f'user: {self.user.id} - tag: {self.tag.name}'
