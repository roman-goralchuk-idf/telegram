from django.apps import AppConfig

from configuration.configurationloader import getRedisConfig
from telegram.service.time_service import TimeService


class CeleryDjangoConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'celery_django'

	CELERY_BROKER_URL = getRedisConfig()
	CELERY_result_backend = getRedisConfig()
	CELERY_TIMEZONE = TimeService().getTimeZone()



