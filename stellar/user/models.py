from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from fernet_fields import EncryptedCharField

from core import choices
from stellar import settings


class StellarUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_ban = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email


class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    provider = models.CharField(max_length=30, choices=choices.PROVIDER_CHOICES)
    access_token = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    phone_number = EncryptedCharField(max_length=128, blank=True)

    class Meta:
        unique_together = (('email', 'provider', 'uid', 'access_token'),)
