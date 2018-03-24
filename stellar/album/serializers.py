from rest_framework import serializers

from album.models import Photo, Album
from utils.gps import get_gps


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('album', 'title', 'photo', 'user', 'latitude', 'longitude')
        read_only_fields = ('latitude', 'longitude', 'title', 'user')
        extra_kwargs = {
            'album': {'required': True},
            'photo': {'required': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        photo = validated_data['photo']

        latitude, longitude = get_gps(photo)
        photo_object = Photo(user=user, latitude=latitude, longitude=longitude, **validated_data)
        photo_object.save()
        return photo_object


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ('id', 'title', 'created_date', 'user_id')
