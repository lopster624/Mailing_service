from rest_framework import serializers

from mailing.models import Client, Mailing


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор клиента"""

    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {'operator_code': {'read_only': True}}


class MailingSerializer(serializers.ModelSerializer):
    """Сериализатор рассылки"""

    class Meta:
        model = Mailing
        fields = '__all__'
