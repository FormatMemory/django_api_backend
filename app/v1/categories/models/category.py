from django.db import models
from django.conf import settings
# from v1.posts.models.post import Post
from v1.general.created_modified import CreatedModified


class Category(CreatedModified):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Title", unique=True)
    # post = models.ManyToManyField(Post, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        default_related_name = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title
