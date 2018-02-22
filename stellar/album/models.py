import re
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from user.models import StellarUser

def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LagLat Type')

class Album(models.Model):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

class Photo(models.Model):
    album = models.ForeignKey(Album)
    photo = models.ImageField(upload_to='photo')
    owner = models.OneToOneField(StellarUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lnglat = models.CharField(max_length=50, validators=[lnglat_validator], blank=True)

