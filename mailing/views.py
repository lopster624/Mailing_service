from django.db.models import Count, F, Q
from rest_framework import viewsets, serializers

from mailing.models import Client, Mailing, Message
from mailing.serializers import ClientSerializer, MailingSerializer, MailingDetailSerializer
from mailing.utils import calculate_operator_code


class ClientViewSet(viewsets.ModelViewSet):
    """CRUD для клиета."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        operator_code = calculate_operator_code(serializer.validated_data.get('phone_number', None))
        if not operator_code:
            raise serializers.ValidationError(f"Номер телефона не был указан!")
        serializer.save(operator_code=operator_code)


class MailingViewSet(viewsets.ModelViewSet):
    """CRUD для рассылки."""
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Подробная ститистика по рассылкам.
    Помимо полей модели Mailing содержит словарь со сгруппированными количествами сообщений по их статусам.
    messages statistic: {
        status: n,
    } - в словаре хранятся статусы сообщений и количество сообщений, подходящих статусу
    """

    serializer_class = MailingDetailSerializer

    def get_queryset(self):
        """Добавить количество отправленных сообщений и сгруппировать по их статусам."""
        queryset = Mailing.objects.all().prefetch_related('messages').annotate(
            **{status[1]: Count(
                F("messages"),
                filter=Q(messages__status=status[0]),
                distinct=True,
            ) for status in Message.STATUSES}
        )
        return queryset
