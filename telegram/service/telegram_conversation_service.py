import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import FloodError

from configuration.configurationloader import configTelegram
from telegram.models.model_send_message import SendMessage
from telegram.models.model_task_delivery import TaskDelivery, TaskDeliveryStatus

_logger = logging.getLogger('custom')


# https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.send_message
# https://core.telegram.org/bots/api#sendmessage


class ConversationService:
	def __init__(self):
		self._parse_mode = configTelegram['telegram']['parse_mode']
		self._waiting_between_messages_sec = configTelegram['telegram']['waiting_between_messages_sec']

	async def sendAllMessages(self, task: TaskDelivery, client: TelegramClient):
		try:
			completed_delivery = []
			_logger.debug(f'Found Telegram ids for delivery: {task.telegram_ids}')
			for telegram_id in task.telegram_ids:
				_logger.debug(f'Sending message starts for id: [{telegram_id}] in task #{task.task_id}')
				send_message = SendMessage(telegram_id, task.message, task.delivery_scheduled)
				message_id = await self.sendMessageToUser(send_message, client)
				_logger.debug(f'Message with id #{message_id} delivered')
				completed_delivery.append(message_id)
			_logger.debug(f'Completed delivery message count: {len(completed_delivery)}')
			if len(task.telegram_ids) != len(completed_delivery):
				return TaskDeliveryStatus.PARTLY_COMPLETED.name_status
			else:
				return TaskDeliveryStatus.COMPLETED.name_status
		except FloodError as flood:
			_logger.error(flood)
			return TaskDeliveryStatus.ERROR.name_status
		except TypeError as e:
			_logger.error(e)

	async def sendMessageToUser(self, send_message: SendMessage, client: TelegramClient):
		await asyncio.sleep(self._waiting_between_messages_sec)
		result = await client.send_message(
			send_message.telegram_id,
			send_message.message,
			schedule=send_message.delivery_scheduled,
			parse_mode=self._parse_mode)
		return result.id
