# Mailing_service
 
Сервис позволяет создавать клиентов для отправки им различных рассылок. 
Сервис позволяет создавать и планировать рассылки. 
А также сервис рассылает сообщения клиентам через стороннее API и собирает
статистику по разосланным сообщениям.


## Зависимости

Сервис работает на Python 3.8 и Django 3.2.15.
Все прочие зависимости вы можете найти в файле requirements.txt.

## Установка и запуск

### 1) Установка Python, Django и прочих зависимостей из requirements.txt.
```shell
pip install -r requirements.txt
```

### 2) Установка docker и запуск в нем Redis.
Докер нужно установить самому :)
```shell
docker run -p 6379:6379 --name some-redis -d redis
```

### 3) Запуск сервиса

```shell
python manage.py runserver
```

### 4) Запуск worker celery
P.S. Делать это нужно в соседнем терминале
```shell
celery -A mailing_service worker -l info -P solo
```


### 5) Запуск flower
Данный компонент необходим для отслеживания процесса работы задач celery.
```shell
celery -A mailing_service flower
```

### 6) Запуск планировщика задач celery 
Данный компонент необходим для отслеживания процесса работы задач celery.
```shell
celery -A mailing_service beat -l info
```


## Документация

Пользовательскую документацию в запущенном сервисе в формате openapi можно получить по [ссылке](http://127.0.0.1:8000/swagger/). 
