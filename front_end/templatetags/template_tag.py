import logging
from datetime import datetime

from django import template

from configuration.configurationloader import configBase

_logger = logging.getLogger('custom')

register = template.Library()


# @register.simple_tag(name='current_time')
# def currentTime(format_string):
# 	return datetime.now().strftime(format_string)
#
#
# @register.simple_tag(name='date_converter')
# def convertStringIsoToDate(context):
# 	if context is not None:
# 		_logger.debug(f'IN: {context}')
# 		result = datetime.fromisoformat(context)
# 		_logger.debug(f'OUT: {result}')
# 		return result


@register.simple_tag(name='app_name')
def convertStringIsoToDate():
	return configBase['appName']
