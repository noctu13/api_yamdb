from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from api.models import Client


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('email',)

    def create(self, validated_data):
        validated_data['is_active'] = False
        validated_data['confirmation_code'] = get_random_string()
        client = super().create(validated_data)
        send_mail(
            'Yambd account activation',
            'confirmation_code: ' + client.confirmation_code,
            'admin@yambd.com',
            [client.email],
            fail_silently=False,
        )
        return client

class TokenSerializer(JSONWebTokenSerializer):
    pass

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        extra_kwargs = {
            'username': {'required': True}
        }
