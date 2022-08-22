import datetime

from django.db.models import Q

from mailing.models import Mailing, Client, Message


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
    return Client.objects.filter(Q(tag__in=filter_list) | Q(operator_code__in=filter_list))


def send_message(client_id, mailing_id, text):
    """
    Отправить сообщению получателю.
    При отправке создать запись в бд для отправленного сообщения со статусом "отправлено".
    При успешном ответе от сервера изменить статус сообщения на "доставлено".
    """
    import requests
    address = 'https://probe.fbrq.cloud/v1/send'
    client = Client.objects.filter(id=client_id).first()
    mailing = Mailing.objects.filter(id=mailing_id).first()
    if not client or not mailing:
        return
    message = Message.objects.create(status=0, mailing=mailing, client=client)
    data = {'id': message.id, 'phone': client.phone_number,'text': text}
    response = requests.post(address, data=data)
    if response.status_code == 200:
        message.status = 1
        message.save(update_fields='status')


def run_mailings():
    """Получить список активных рассылок на текущий момент и отправить сообщения получателям."""
    live_mailings = get_live_mailings()
    for mailing in live_mailings:
        clients = get_filter_clients(mailing.filter.split())
        for client in clients:
            send_message(client.id, mailing.id, mailing.text)