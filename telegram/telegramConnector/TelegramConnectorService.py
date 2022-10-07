
import os

from django_telethon_session.sessions import DjangoSession
from telethon import TelegramClient

from configuration.configurationloader import configBase

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class Client:
	api_id = configBase['telegram']['api_id']
	api_hash = configBase['telegram']['api_hash']
	phone = configBase['telegram']['phone']
	name = configBase['telegram']['name_connection']
	password = configBase['telegram']['password']

	proxy_type = configBase['telegram']['proxy']['proxy_type']
	proxy_addr = configBase['telegram']['proxy']['addr']
	proxy_port = configBase['telegram']['proxy']['port']
	proxy_username = configBase['telegram']['proxy']['username']
	proxy_password = configBase['telegram']['proxy']['password']
	proxy_rdns = configBase['telegram']['proxy']['rdns']

	client = TelegramClient(
		DjangoSession(name),
		api_id,
		api_hash,
		# proxy=(
		# 	proxy_type,
		# 	proxy_addr,
		# 	proxy_port,
		# )
	)

	async def checkConnection(self):
		await self.client.connect()
		if not await self.client.is_user_authorized():
			phone_code_hash = await self.client.send_code_request(self.phone)
			with open("phone_code_hash.txt", "w") as file:
				file.write(str(phone_code_hash.phone_code_hash))
		# await self.client.disconnect()
		return 'Not connection. You must verify your account to connect. Code sent in private message'

	async def sendCode(self, code):
		with open("phone_code_hash.txt", "r") as file:
			phone_code_hash = file.readline()
		await self.client.connect()
		# if not await self.client.is_user_authorized():
		# 	await self.client.sign_in(self.phone, code, phone_code_hash=phone_code_hash)
		await self.client.send_message('me', phone_code_hash)
		await self.client.disconnect()
		return phone_code_hash
