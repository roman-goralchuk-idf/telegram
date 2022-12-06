from django.apps import AppConfig

from configuration.configurationloader import configService
from telegram.service.time_service import TimeService


def getRedisConfig() -> str:
	password = configService['database']['redis']['password']
	host = configService['database']['redis']['host']
	port = configService['database']['redis']['port']
	return f'redis://:{password}@{host}:{port}'


class CeleryDjangoConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'celery_django'

	CELERY_BROKER_URL = getRedisConfig()
	CELERY_RESULT_BACKEND = getRedisConfig()
	CELERY_TIMEZONE = TimeService().getTimeZone()
	CELERY_TASK_TRACK_STARTED = True
	CELERY_TASK_TIME_LIMIT = 30 * 60
	CELERY_task_serializer = 'json'
	CELERY_result_serializer = 'json'
	CELERY_accept_content = ['json']
