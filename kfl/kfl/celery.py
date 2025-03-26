from celery import Celery
from celery.schedules import crontab

app = Celery('kfl')

app.conf.beat_schedule = {
    'update_match_status_every_5_minutes': {
        'task': 'your_app.tasks.update_match_status',
        'schedule': crontab(minute='*/5'),  # Задача будет запускаться каждые 5 минут
    },
}
