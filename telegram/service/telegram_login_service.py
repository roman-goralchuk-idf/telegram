import logging
from os.path import join

from telethon import TelegramClient

from telegram.apps import TELEGRAM_SESSION
from telegram.service.telegram_client_service import TelegramApiService, checkConnection

_logger = logging.getLogger('custom')


class LoginService:
	def __init__(self):
		self._client = TelegramApiService().getTelegramClient()
		self._phone = TelegramApiService().getPhoneNumber()

	async def checkAuthorization(self):
		try:
			await checkConnection(client=self._client)
			await self._client.connect()
			_logger.debug(f'Connection: Start')
			if not await self._client.is_user_authorized():
				_logger.debug('Authorization: False')
				await self._savePhoneHashFromResponse(self._client, self._phone)
				return 'Authorization: False -> Code sent to PM'
			else:
				_logger.debug('Authorization: True')
				return 'Authorization: True'
		finally:
			await self._client.disconnect()
			await checkConnection(client=self._client)

	async def sendReceivedCode(self, code):
		try:
			phone_code_hash = await self._getPhoneHashFromRepository()
			await self._client.connect()
			await self._client.sign_in(phone=self._phone, code=code, phone_code_hash=phone_code_hash)
			me = await self._client.get_me()
			_logger.debug(me.stringify())
			return 'Authorization is successfully'
		except TypeError as e:
			_logger.error(e)
			return 'Authorization problem'
		finally:
			await self._client.disconnect()
			await checkConnection(client=self._client)

	@staticmethod
	async def _savePhoneHashFromResponse(client: TelegramClient, phone):
		phone_hash_response = await client.send_code_request(phone)
		phone_code_hash = phone_hash_response.phone_code_hash
		with open(join(TELEGRAM_SESSION, 'phone_code_hash.txt'), 'w') as p_hash:
			p_hash.write(phone_code_hash)
		_logger.debug(f'phone hash saved: {phone_code_hash}')

	@staticmethod
	async def _getPhoneHashFromRepository() -> str:
		try:
			with open(join(TELEGRAM_SESSION, 'phone_code_hash.txt'), 'r') as p_hash:
				phone_code_hash = p_hash.read()
				_logger.debug(f'phone hash found: {phone_code_hash}')
			return phone_code_hash
		except FileNotFoundError:
			_logger.error(f'phone hash found: {phone_code_hash}')
