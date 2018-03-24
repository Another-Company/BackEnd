from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from album.models import Photo, Album
from album.serializers import PhotoSerializer, AlbumSerializer
from utils import ValidationException


class AlbumViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Album.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['create', 'list']:
            return AlbumSerializer
        else:
            return Serializer

    def get_queryset(self):
        if self.action == 'list':
            return Album.objects.filter(user=self.request.user)
        else:
            return self.queryset

    def create(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        if title is None:
            raise ValidationException('Title is Required')

        album = Album.objects.create(title=title, user=request.user)
        serializer = self.get_serializer(album)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        album_id = kwargs['pk']
        title = request.data.get('title', None)
        instance = get_object_or_404(Album, pk=album_id, user=request.user)
        instance.title = title
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return Photo.objects.filter(user=self.request.user)
        else:
            return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
