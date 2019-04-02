from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified
from v1.utils import constants


class Post(CreatedModified):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(blank=True)
    link = models.URLField(blank=True)
    date_expire = models.DateTimeField(null=True, blank=True)
    date_posted = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)
    status = models.CharField(max_length=50, default=constants.POST_STATUS_ACTIVE)
    total_views = models.IntegerField(default = 0)

    class Meta:
        default_related_name = 'posts'
        ordering = ['date_posted']

    def __str__(self):
        return self.title