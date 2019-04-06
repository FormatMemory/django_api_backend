from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified
from v1.utils import constants

class Report(CreatedModified):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=25, default=constants.REPORT_STATUS_ACTIVE)
    description = models.CharField(max_length=255, blank=True)
    auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='auditor')
    audit_message = models.CharField(max_length=255, blank=True)
    class Meta:
        abstract = True
