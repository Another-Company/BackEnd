from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from user import views_api

router = DefaultRouter()
router.register(r'users', views_api.StellarUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls'))
]
