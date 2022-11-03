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
	# LOGGING = {
	# 	'version': 1,
	# 	'disable_existing_loggers': True,
	# 	'formatters': {
	# 		'simple': {
	# 			'format': '%(levelname)s %(message)s',
	# 			'datefmt': '%y %b %d, %H:%M:%S',
	# 		},
	# 	},
	# 	'handlers': {
	# 		'console': {
	# 			'level': 'DEBUG',
	# 			'class': 'logging.StreamHandler',
	# 			'formatter': 'simple'
	# 		},
	# 		'celery': {
	# 			'level': 'DEBUG',
	# 			'class': 'logging.handlers.RotatingFileHandler',
	# 			'filename': 'celery.log',
	# 			'formatter': 'simple',
	# 			'maxBytes': 1024 * 1024 * 100,  # 100 mb
	# 		},
	# 	},
	# 	'loggers': {
	# 		'celery': {
	# 			'handlers': ['celery', 'console'],
	# 			'level': 'DEBUG',
	# 		},
	# 	}
	# }
	from logging.config import dictConfig
	from telegram_parser.settings import LOGGING
	dictConfig(LOGGING)


celery_app.autodiscover_tasks(packages=['telegram'])


@celery_app.task(bind=True)
def debug_task(self):
	_logger.debug(f'Celery request: {self.request!r}')
