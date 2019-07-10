from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified


class Moderator(CreatedModified):
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sponsored_moderators', on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
