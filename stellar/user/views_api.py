from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import StellarUser, SocialAccount
from user.serializers import SocialAccountSerializer, StellarUserSerializer


class StellarUserViewSet(ModelViewSet):
    queryset = SocialAccount.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SocialAccountSerializer

    def get_queryset(self):
        if self.action == 'list':
            return StellarUser.objects.all()
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return StellarUserSerializer
        else:
            return self.serializer_class

    @list_route(methods=['get'])
    def social(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
