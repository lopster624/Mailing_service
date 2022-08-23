import datetime

from django.db.models import Q

from mailing.models import Mailing, Client


def calculate_operator_code(phone_number):
    """Вернуть код оператора"""
    if phone_number:
        return phone_number[1:4]


def get_live_mailings():
    """Получить рассылки, которые работаю в текущее время."""
    current_datetime = datetime.datetime.now()
    return Mailing.objects.filter(start_time__lte=current_datetime, end_time__gte=current_datetime)


def get_filter_clients(filter_list):
    """Получить отфильтрованных клиентов"""
    if not filter_list:
        return Client.objects.filter(tag='')
    return Client.objects.filter(Q(tag__in=filter_list) | Q(operator_code__in=filter_list))


