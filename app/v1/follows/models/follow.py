from django.conf import settings
from django.db import models
from v1.utils import constants
from v1.general.created_modified import CreatedModified


class Follow(CreatedModified):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
