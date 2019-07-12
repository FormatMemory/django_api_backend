from django.db import models
from django.conf import settings
from v1.posts.models.post import Post
from v1.general.created_modified import CreatedModifie
from v1.general.image_validator import validate_image
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)

class PostImage(CreatedModifie):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, Null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    image = models.ImageField(blank=True, upload_to=get_file_path, validators=[validate_image])

    class Meta:
        default_related_name = 'post_images'

    def __str__(self):
        return str(id) + ": " + str(self.post) + " Image"
