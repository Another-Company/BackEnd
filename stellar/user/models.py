from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from core import choices
from stellar import settings


class StellarUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    email = models.EmailField('email address', blank=True, unique=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_ban = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    objects = UserManager()

    def __str__(self):
        return '%s: %s' % (self.pk, self.email)


class StellarSocialUser(models.Model):
    uid = models.CharField(max_length=256, unique=True)
    provider = models.CharField(max_length=10, choices=choices.PROVIDER_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
