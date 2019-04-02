from django.conf import settings
from django.db import models
from v1.utils import constants


class View(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(choices=constants.USER_VIEW_CHOICES)
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
