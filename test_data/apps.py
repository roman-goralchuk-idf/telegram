from os.path import join

from django.apps import AppConfig

from telegram_parser.settings import BASE_DIR


class TestDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_data'


TEST_DATA_FULL = join(BASE_DIR, 'test_data/full')
