from django.core.mail import send_mail

from rest_framework import serializers

from api.models import Client

def send_confirmation_mail(client):
    send_mail(
        'Yambd account activation',
        'confirmation_code: ' + str(client.confirmation_code),
        'admin@yambd.com',
        [client.email],
        fail_silently=False,
    )

class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('email',)

    def create(self, validated_data):
        validated_data['is_active'] = False
        client = super().create(validated_data)
        send_confirmation_mail(client)
        return client

    #проверка confirmation_code?

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': True}
        }
