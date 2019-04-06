from django.db import models
from django.conf import settings
from v1.follows.models.follow import Follow


class FollowUser(Follow):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    follow_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='follow_user')

    class Meta:
        default_related_name = 'user_follow_user'
        unique_together = ('user', 'follow_user')

    def __str__(self):
        return f'{self.user.id} - follows: {self.follow_user.id}'
