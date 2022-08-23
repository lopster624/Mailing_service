from rest_framework import serializers

from mailing.models import Client, Mailing, Message


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


class MailingDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор статистики по рассылке
    Помимо полей модели Mailing содержит словарь со сгруппированными количествами сообщений по их статусам.
    messages statistic: {
        status: n,
    } - в словаре хранятся статусы сообщений и количество сообщений, подходящих статусу

    """

    def to_representation(self, instance):
        """Добавить в вывод объекта статистику по сообщениям."""
        res = super().to_representation(instance)
        res.update({'messages statistic': {
            status[1]: getattr(instance, status[1]) for status in Message.STATUSES if status[1] in dir(instance)
        }})
        return res

    class Meta:
        model = Mailing
        fields = '__all__'
