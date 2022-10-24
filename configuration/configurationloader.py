import logging
from os.path import join

import yaml

from configuration.apps import SETTING_DIR

_logger = logging.getLogger('custom')


def _loader(filename):
	try:
		with open(join(SETTING_DIR, filename)) as config:
			result = yaml.load(config, Loader=yaml.FullLoader)
			_logger.debug(filename + ' - loaded successfully')
			return result
	except IOError as e:
		_logger.error(e)


def getRedisConfig() -> str:
	password = configService['database']['redis']['password']
	host = configService['database']['redis']['host']
	port = configService['database']['redis']['port']
	return f'redis://:{password}@{host}:{port}'


configBase = _loader('config_app.yaml')
configService = _loader('config_services.yaml')[configBase['environment']]
configResponse = _loader('config_response.yaml')
configTelegram = _loader('config_telegram.yaml')[configBase['telegram_account']]
