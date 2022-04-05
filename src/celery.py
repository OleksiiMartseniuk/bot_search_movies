from celery import Celery
from celery.schedules import crontab


app = Celery('src',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['src.tasks'])

app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Kiev',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'add-every-day-morning': {
        'task': 'src.tasks.request_api_imdb',
        'schedule': crontab(hour=4, minute=30)
    },
}
