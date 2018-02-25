import re
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from user.models import StellarUser


def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LagLat Type')


class Album(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album)
    title = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photo')
    user = models.OneToOneField(StellarUser, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.title
