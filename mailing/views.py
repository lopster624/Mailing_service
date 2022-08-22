from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, serializers

from mailing.models import Client, Mailing
from mailing.serializers import ClientSerializer, MailingSerializer
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
