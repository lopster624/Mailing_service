import pytz
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class Mailing(models.Model):
    """Рассылка"""
    start_time = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    filter = models.CharField(verbose_name='Фильтр', max_length=100, blank=True)

    def __str__(self):
        return f"{self.text}: {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    """Клиент, получатель рассылки"""
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    class Validator:
        phone_regex = RegexValidator(regex=r'7\d{10}$',
                                     message="Введите корректный номер телефона формата: 7XXXXXXXXXX")

    phone_number = models.CharField(validators=[Validator.phone_regex], verbose_name='Номер телефона', max_length=11)
    operator_code = models.CharField(verbose_name='Код мобильного оператора', max_length=3, null=True)
    tag = models.CharField(verbose_name='Тег', max_length=50, blank=True)
    timezone = models.CharField(verbose_name='Часовой пояс', choices=TIMEZONES, blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.phone_number}"


class Message(models.Model):
    """Сообщение"""

    STATUSES = (
        (0, 'Отправлено'),
        (1, 'Доставлено'),
        (2, 'В процессе отправки'),
        (3, 'Не доставлено')
    )
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status = models.IntegerField(choices=STATUSES, verbose_name='Статус отправки')
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', related_name='messages', on_delete=models.SET_NULL,
                                blank=True, null=True)
    client = models.ForeignKey(Client, verbose_name='Получатель', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.create_date}: {self.client} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
