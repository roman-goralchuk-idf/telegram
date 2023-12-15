import logging
import random
from os.path import join

from telethon import TelegramClient

from configuration.configurationloader import configTelegram, configBase
from telegram.apps import TELEGRAM_SESSION

_logger = logging.getLogger('custom')


class TelegramApiService:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if cls.__instance is None:
			cls.__instance = super().__new__(cls)
		return cls.__instance

	def __init__(self):
		self._api_id = configTelegram['telegram']['api_id']
		self._api_hash = configTelegram['telegram']['api_hash']
		self._session_name = configTelegram['telegram']['session']
		self._phone = configTelegram['telegram']['phone']
		self._account_type = configBase['telegram_account']
		_logger.debug(f'Configuration {self._account_type} account')

	def getTelegramClient(self) -> TelegramClient:
		client = TelegramClient(join(TELEGRAM_SESSION, self._session_name), self._api_id, self._api_hash)
		if self._account_type == 'account_test':
			dc = configTelegram['telegram']['dc']
			host = configTelegram['telegram']['host']
			port = configTelegram['telegram']['port']
			client.session.set_dc(dc, str(host), port)
			return client
		else:
			return TelegramClient(join(TELEGRAM_SESSION, self._session_name), self._api_id, self._api_hash)

	def getPhoneNumber(self) -> str:
		name_phone_file = 'phone_for_debugging.txt'
		if self._account_type == 'account_test':
			try:
				with open(join(TELEGRAM_SESSION, name_phone_file), 'r') as ph:
					phone = ph.read()
				return phone
			except FileNotFoundError:
				phone = f'99966{self._getDc()}{str(random.randint(0, 3)).zfill(4)}'
				with open(join(TELEGRAM_SESSION, name_phone_file), 'w') as ph:
					ph.write(phone)
				return phone
		else:
			return self._phone

	@staticmethod
	def _getDc():
		dc = configTelegram['telegram']['dc']
		return dc


async def checkConnection(client):
	x = client.is_connected()
	_logger.debug(f'Connection status: {x}')
