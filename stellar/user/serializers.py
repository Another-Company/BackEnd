from rest_framework import serializers

from user.models import SocialAccount, StellarUser
from utils import ValidationException
from utils.social_verification import KaKaoTalk, FaceBook


class StellarUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StellarUser
        fields = ('id', 'email', 'is_ban')


class SocialAccountSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=256, required=False)

    class Meta:
        model = SocialAccount
        fields = (
            'email',
            'email_verified',
            'provider',
            'access_token',
            'uid',
            'phone_number',
            'token'
        )
        read_only_fields = ('uid', 'phone_number', 'token')
        extra_kwargs = {
            'access_token': {'write_only': True},
            'email': {'required': False},
        }

    def create(self, validated_data):
        access_token = validated_data.get('access_token', None)
        provider = validated_data.get('provider', None)
        email = validated_data.get('email', None)
        email_verified = validated_data.get('email_verified', None)

        if email is None:
            raise ValidationException('Email Address is Missing')

        if provider == 'KT':
            if email_verified is None:
                raise ValidationException('Email Verified is Missing')
            user_verified_token = KaKaoTalk.account_verification(access_token)

            user_object, _ = StellarUser.objects.get_or_create(email=email)
            social_object, _ = SocialAccount.objects.get_or_create(uid=user_verified_token['id'],
                                                                   email=email,
                                                                   provider=provider,
                                                                   defaults={'user': user_object,
                                                                             'email_verified': email_verified if email_verified is not None else False,
                                                                             'access_token': access_token})

        elif provider == 'FB':
            # I need debug_token response data
            response_dict = FaceBook.account_verification(access_token)

            user_object, _ = StellarUser.objects.get_or_create(email=email)
            social_object, _ = SocialAccount.objects.get_or_create(uid=response_dict['data']['user_id'],
                                                                   email=email,
                                                                   provider=provider,
                                                                   defaults={'user': user_object,
                                                                             'email_verified': email_verified if email_verified is not None else False,
                                                                             'access_token': access_token})

        else:
            ValidationException('Not Allowed Providers')
            
        if social_object.access_token != access_token:
            social_object.access_token = access_token
            social_object.save()
        return social_object
