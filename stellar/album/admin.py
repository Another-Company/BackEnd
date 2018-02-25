from django.contrib import admin

from album.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Album)
admin.site.register(Photo)
