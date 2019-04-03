from django.conf import settings
from django.db import models
from v1.utils import constants
from datetime import datetime

class View(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:00'))
    ip = models.CharField(max_length=40, null=True, blank=True)
    session = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        abstract = True
