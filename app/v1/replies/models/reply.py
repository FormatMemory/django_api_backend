from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified


class Reply(CreatedModified):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body = models.TextField()

    class Meta:
        abstract = True
