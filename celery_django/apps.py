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
	CELERY_result_backend = _getRedisConfig()
	CELERY_timezone = TimeService().getTimeZone()
	CELERY_task_track_started = True
	CELERY_task_time_limit = 30 * 60
