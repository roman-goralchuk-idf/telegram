from os.path import join

from django.apps import AppConfig

from telegram_parser.settings import BASE_DIR


class ConfigurationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configuration'


SETTING_DIR = join(BASE_DIR, 'setting')
