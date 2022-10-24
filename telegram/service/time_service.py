import pytz

from configuration.configurationloader import configBase


class TimeService:
	def __init__(self):
		self._timezone_name = configBase['time_zone']

	def getTimeZone(self):
		return pytz.timezone(self._timezone_name)

	@staticmethod
	def getAllTimeZones():
		return pytz.all_timezones
