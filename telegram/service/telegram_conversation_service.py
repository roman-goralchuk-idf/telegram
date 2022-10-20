import asyncio

from configuration.configurationloader import configTelegram
from telegram.models.model_send_message import SendMessage
from telegram.models.model_task import TaskDelivery
from telegram.service.telegram_client_service import TelegramApiService


# https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.send_message
# https://core.telegram.org/bots/api#sendmessage


class ConversationService:
	def __init__(self):
		self._client = TelegramApiService().getTelegramClient()
		self._parse_mode = configTelegram['telegram']['parse_mode']
		self._waiting_between_messages_sec = configTelegram['telegram']['waiting_between_messages_sec']

	async def sendAllMessages(self, task: TaskDelivery):
		for telegram_id in task.array_id:
			send_message = SendMessage(telegram_id, task.message, task.delivery_scheduled)
			await self.sendMessageToUser(send_message)
			await asyncio.sleep(self._waiting_between_messages_sec)

	async def sendMessageToUser(self, send_message: SendMessage):
		await self._client.send_message(
			send_message.telegram_id,
			send_message.message,
			schedule=send_message.delivery_scheduled,
			parse_mode=self._parse_mode)
