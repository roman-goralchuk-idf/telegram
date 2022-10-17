import logging
from os.path import join

from telethon import TelegramClient

from telegram.apps import TELEGRAM_SESSION
from telegram.service.telegram_service import TelegramApiService

_logger = logging.getLogger('custom')


class LoginService:
	async def checkAuthorization(self):
		client = await TelegramApiService().getTelegramClient()
		phone = await TelegramApiService().getPhoneNumber()

		x = client.is_connected()
		_logger.debug(f'Connection: {x}')

		await client.connect()
		_logger.debug(f'Connection: Start')
		if not await client.is_user_authorized():
			_logger.debug('Authorization: False')
			await self._savePhoneHashFromResponse(client, phone)
			await client.disconnect()
			x = client.is_connected()
			_logger.debug(f'Connection: {x}')
			return 'Connection: False -> Code sent to PM'
		else:
			_logger.debug('Authorization: True')
			return 'Connection: True'

	async def sendReceivedCode(self, code):
		client = await TelegramApiService().getTelegramClient()
		phone = await TelegramApiService().getPhoneNumber()
		phone_code_hash = await self._getPhoneHashFromRepository()

		await client.connect()
		try:
			await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
			me = await client.get_me()
			_logger.debug(me.stringify())
			return 'Authorization is successfully'
		except TypeError as e:
			_logger.error(e)
			return 'Authorization problem'

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