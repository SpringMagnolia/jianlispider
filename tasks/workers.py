from celery import Celery, platforms
from kombu import Exchange, Queue
from datetime import timedelta

broker = "redis://localhost:6379/9"
backend = "redis://localhost:6379/8"

tasks = [
    'tasks.downloader'
]

app = Celery('jobSpider', include=tasks, broker=broker, backend=backend)

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    # CELERYD_LOG_FILE=worker_log_path,
    # CELERYBEAT_LOG_FILE=beat_log_path,
    CELERY_ACCEPT_CONTENT=['pickle'],
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_RESULT_SERIALIZER='pickle',
    CELERYBEAT_SCHEDULE={
            'start_request_task': {
                'task': 'tasks.downloader.execute_start_request',
                'schedule': timedelta(minutes=2),
                'options': {'queue': 'downloader_queue', 'routing_key': 'for_downloader'}
            }
    },
    CELERY_QUEUES=(
        Queue('parse_page_list', exchange=Exchange('parse_page_list', type='direct'), routing_key='for_page_list'),

        Queue('parse_page_detail', exchange=Exchange('parse_page_detail', type='direct'), routing_key='for_page_detail'),

        Queue('downloader_queue', exchange=Exchange('downloader_queue', type='direct'), routing_key='for_download'),
        Queue('item_queue', exchange=Exchange('item_queue', type='direct'), routing_key='for_save'),
    ),

)
