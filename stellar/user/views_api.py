from firebase_admin import auth
from firebase_admin.auth import AuthError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import StellarUser, StellarSocialUser
from utils import ValidationException


class StellarUserViewSet(CreateModelMixin, GenericViewSet):

    def create(self, request, *args, **kwargs):
        uid = request.data.get('uid', None)

        if uid is None:
            raise ValidationException('UID is Required')
        try:
            user = auth.get_user(uid)
        except AuthError:
            raise ValidationException('Invalid UID Please Check the UID')

        email = user.email
        email_verified = user.email_verified
        username = user.display_name
        provider = user.provider_data[0].provider_id.split('.')[0]

        if email is None:
            raise ValidationException('Email Address is Required')

        user_object, _ = StellarUser.objects.get_or_create(email=email,
                                                           defaults={'email_verified': email_verified,
                                                                     'username': username})

        social_object, _ = StellarSocialUser.objects.get_or_create(uid=uid,
                                                                   defaults={'provider': provider,
                                                                             'user': user_object})
        token, _ = Token.objects.get_or_create(user=user_object)
        return Response(data={'uid': uid, 'token': str(token)}, status=status.HTTP_201_CREATED)

