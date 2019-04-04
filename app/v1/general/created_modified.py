from django.db import models
from datetime import datetime

class CreatedModified(models.Model):
    
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
