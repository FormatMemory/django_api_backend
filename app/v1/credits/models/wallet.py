from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified


class Wallet(CreatedModified):
    balance = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
