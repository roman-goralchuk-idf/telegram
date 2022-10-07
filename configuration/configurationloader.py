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


configBase = _loader('config.yaml')
configDatabase = _loader('config_db.yaml')
configResponse = _loader('config_response.yaml')
