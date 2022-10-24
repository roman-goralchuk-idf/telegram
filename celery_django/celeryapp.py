import logging

from celery import Celery

_logger = logging.getLogger('custom')


# https://realpython.com/asynchronous-tasks-with-django-and-celery/

# redis-cli -h localhost -p 6379 -a pasaword
# redis://user:secret@localhost:6379/0
# python -m celery -A celery_django worker -l info

def _getCelery() -> Celery:
	_logger.debug('Celery STARTED')
	return Celery("telegram_parser")


celery_app = _getCelery()
celery_app.autodiscover_tasks()
celery_app.config_from_object('celery_django.apps.CeleryDjangoConfig', namespace='CELERY')


@celery_app.task(bind=True)
def debug_task(self):
	_logger.debug(f'Celery request: {self.request!r}')
