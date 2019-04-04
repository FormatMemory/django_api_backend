from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified


class Profile(CreatedModified):
    gender = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=125, blank=True)
    language = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=250, blank=True)
    image = models.ImageField(blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
