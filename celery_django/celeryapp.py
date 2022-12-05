import logging

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings  # noqa

_logger = logging.getLogger('custom')


# https://realpython.com/asynchronous-tasks-with-django-and-celery/

# redis-cli -h localhost -p 6379 -a pasaword
# redis://user:secret@localhost:6379/0
# python3 -m celery -A celery_django worker -l info <- this command needs to start Celery!!!

def _getCelery() -> Celery:
	_logger.debug('Celery STARTED')
	return Celery("telegram_parser")


celery_app = _getCelery()
celery_app.config_from_object('celery_django.apps.CeleryDjangoConfig', namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
	from logging.config import dictConfig
	from telegram_parser.settings import LOGGING
	dictConfig(LOGGING)


celery_app.autodiscover_tasks(packages=['telegram'])


@celery_app.task(bind=True)
def debug_task(self):
	_logger.debug(f'Celery request: {self.request!r}')


def get_celery_worker_status():
	inspect = celery_app.control.inspect()
	availability = inspect.ping()
	stats = inspect.stats()
	registered_tasks = inspect.registered()
	active_tasks = inspect.active()
	scheduled_tasks = inspect.scheduled()
	result = {
		'availability': availability,
		'stats': stats,
		'registered_tasks': registered_tasks,
		'active_tasks': active_tasks,
		'scheduled_tasks': scheduled_tasks
	}
	return result


def get_celery_life():
	inspect = celery_app.control.inspect()
	availability = inspect.ping()
	if availability is not None:
		return 'Task server started. The current task has been sent to the server for execution.'
	else:
		return 'Task server is not running. The current task has been queued and is waiting for the server to start.'
