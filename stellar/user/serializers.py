from rest_framework import serializers


class StellarUserSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    email_verified = serializers.BooleanField(default=False, read_only=True)
    username = serializers.CharField(max_length=50, read_only=True)
    provider = serializers.CharField(max_length=20, read_only=True)
