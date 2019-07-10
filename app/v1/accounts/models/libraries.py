from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified
from v1.posts.models.post import Post
from v1.utils import constants


class Library(CreatedModified):
    name = models.CharField(max_length=50, default='MyLibrary')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, default=constants.LIBRARY_STATUS_PUBLIC)

    class Meta:
        default_related_name = 'library'

    def __str__(self):
        return self.user.username +" - "+ self.name

class LibraryItem(CreatedModified):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        default_related_name = 'library_item'

    def __str__(self):
        return self.library.name + " - " + self.post.title
