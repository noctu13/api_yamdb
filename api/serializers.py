from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from api.models import Client


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('email',)

class TokenSerializer(JSONWebTokenSerializer):
    #спцефичный header -> Authorization: JWT token

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        self.fields['password'].required = False

    def validate(self, attrs):
        field = 'confirmation_code'
        credentials = {
            self.username_field: attrs.get(self.username_field),
            field: attrs.get(field)
        }
        if all(credentials.values()):
            try:
                user = Client.objects.get(
                    email=credentials[self.username_field],
                    confirmation_code=credentials[field]
                )
            except Client.DoesNotExist:
                user = None
            if user:
                payload = jwt_payload_handler(user)
                user.is_active = True
                user.save()
                return {
                    'token': jwt_encode_handler(payload)
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "{field}".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

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
