from os.path import join

from django.apps import AppConfig

from telegram_parser.settings import BASE_DIR


class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram'


TEST_DATA_FULL = join(BASE_DIR, 'test_data/full')
TELEGRAM_SESSION = join(BASE_DIR, 'telegram/telegram_session')
