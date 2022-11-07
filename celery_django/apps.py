import os

from django.apps import AppConfig

from configuration.configurationloader import configService
from telegram.service.time_service import TimeService


def _getRedisConfig() -> str:
	password = configService['database']['redis']['password']
	host = configService['database']['redis']['host']
	port = configService['database']['redis']['port']
	return f'redis://:{password}@{host}:{port}'


class CeleryDjangoConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'celery_django'

	CELERY_BROKER_URL = _getRedisConfig()
	CELERY_RESULT_BACKEND = _getRedisConfig()
	CELERY_TIMEZONE = TimeService().getTimeZone()
	CELERY_TASK_TRACK_STARTED = True
	CELERY_TASK_TIME_LIMIT = 30 * 60
