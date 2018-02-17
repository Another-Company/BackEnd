from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
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

    def generate_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token

    @list_route(methods=['get'])
    def social(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        social_object = serializer.save()
        token = self.generate_token(social_object.user)
        return social_object, token

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, token = self.perform_create(serializer)

        return Response(data={'user': serializer.data, 'token': str(token)}, status=status.HTTP_200_OK)
