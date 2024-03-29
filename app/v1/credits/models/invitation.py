import uuid
from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified


class Invitation(CreatedModified):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_invitations', on_delete=models.PROTECT)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, default=None, null=True, related_name='received_invitations', on_delete=models.PROTECT)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        default_related_name = 'invitations'

    def __str__(self):
        return f'{self.code}'
