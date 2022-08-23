import json
import requests
from celery import shared_task

from mailing.models import Client, Message, Mailing
from mailing.utils import get_filter_clients, get_live_mailings
from mailing_service.settings import AUTH_API_TOKEN
from django.utils import timezone


@shared_task(bind=True, default_retry_delay=300, max_retries=5)
def send_message(self, client_id, mailing_id, text):
    """
    Отправить сообщению получателю.
    При отправке создать запись в бд для отправленного сообщения со статусом "отправлено".
    При успешном ответе от сервера изменить статус сообщения на "доставлено".
    """
    address = 'https://probe.fbrq.cloud/v1/send/'
    if Message.objects.filter(mailing_id=mailing_id, client_id=client_id, status=1).exists():
        return
    client = Client.objects.filter(id=client_id).first()
    mailing = Mailing.objects.filter(id=mailing_id).first()
    if not client or not mailing:
        return
    if timezone.now() < mailing.end_time:
        message = Message.objects.create(status=0, mailing=mailing, client=client)
        try:
            response = requests.post(address + f'{message.id}',
                                     data=json.dumps({'id': message.id, 'phone': client.phone_number, 'text': text}),
                                     headers={'Authorization': f'Bearer {AUTH_API_TOKEN}'})
            if response.status_code == 200:
                message.status = 1
                message.save(update_fields=['status'])
        except Exception:
            self.retry(countdown=5)


@shared_task
def run_mailings():
    """Разослать сообщения получателям всех активных рассылок."""
    for mailing in get_live_mailings():
        clients = get_filter_clients(mailing.filter.split())
        for client in clients:
            send_message.delay(client.id, mailing.id, mailing.text)


