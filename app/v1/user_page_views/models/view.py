from django.conf import settings
from django.db import models
from v1.utils import constants


class View(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=40, null=True, blank=True)
    session = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        abstract = True
