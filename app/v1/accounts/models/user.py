import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from django.db import models
from v1.accounts.managers.user_manager import UserManager
from v1.utils import constants


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, blank=True, default="")
    username = models.CharField(max_length=50, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(choices=constants.USER_STATUS_CHOICES, default=constants.STATUS_ACTIVE, max_length=30)
    last_modified = models.DateTimeField(auto_now=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    signup_ip = models.GenericIPAddressField(null=True, blank=True)
    signup_location = models.CharField(max_length=50, null=True, blank=True)
    last_location = models.CharField(max_length=50, null=True, blank=True)
    # date_joined    # groups¶

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        app_label = 'accounts'
        ordering = ['id']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = str(uuid.uuid4()).replace('-', '')
        super(User, self).save(*args, **kwargs)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        if self.email:
            send_mail(subject, message, from_email, [self.email], **kwargs)
