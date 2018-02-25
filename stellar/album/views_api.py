from rest_framework import permissions
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from album.models import Photo, Album
from album.serializers import PhotoSerializer
from utils import ValidationException


class AlbumViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    queryset = Album.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
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
        return Response(data={'id': album.id, 'title': album.title, 'user': album.user.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        album_id = kwargs['pk']
        if title is None:
            raise ValidationException('Title is Required')

        print(album_id)


class PhotoViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return Photo.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
