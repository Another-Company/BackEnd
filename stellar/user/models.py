from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from fernet_fields import EncryptedCharField

from core import choices
from stellar import settings


class StellarUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class StellarUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_ban = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_username(self):
        return self.email

    objects = StellarUserManager()


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
