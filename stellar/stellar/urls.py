from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from user import views_api as user_views_api
from album import views_api as album_views_api

router = DefaultRouter()
router.register(r'users', user_views_api.StellarUserViewSet, base_name='user')
router.register(r'albums', album_views_api.AlbumViewSet, base_name='album')
router.register(r'photos', album_views_api.PhotoViewSet, base_name='photo')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls'))
]
