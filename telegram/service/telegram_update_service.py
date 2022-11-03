import datetime
import logging

from pymongo.results import InsertManyResult

from telegram.models.model_channel import ChannelStatus, Channel
from telegram.models.model_customer import CustomerStatus
from telegram.models.model_event import EventParserMessage
from telegram.repository_mongo.mongo_message import MongoRepositoryMessages
from telegram.service.channel_service import ChannelService
from telegram.service.event_service import EventParserMessageService
from telegram.service.telegram_client_service import TelegramApiService

_logger = logging.getLogger('custom')


# https://telethonn.readthedocs.io/en/latest/telethon.html#module-telethon.telegram_client

class TelegramUpdateService:

	def __init__(self):
		self._client = TelegramApiService().getTelegramClient()
		self._empty_list = 0

	async def updateMessages(self) -> []:
		try:
			await self._client.connect()
			array_send_message_result = []
			array_channel = await ChannelService().getChannelByStatus(ChannelStatus.IN_WORK.value)

			for channel in array_channel:
				_logger.debug(
					f'In database \"{channel.channel_id}\" last updated id is: {channel.last_update_message_id}'
				)
				last_mess_id_in_telegram = await self._getLastMessageIdInTelegram(channel)
				all_new_messages = await self._client.get_messages(
					channel.channel_id,
					min_id=int(channel.last_update_message_id),
					max_id=last_mess_id_in_telegram
				)
				mongo_ids: [str] = await self._sendMessagesInDB(all_new_messages)

				event = EventParserMessage(ids_messages=mongo_ids, customer_status=CustomerStatus.NEW.value)

				await EventParserMessageService().emit(event)
				array_send_message_result.append(mongo_ids)
				await self._updateChannelInfoInDB(last_mess_id_in_telegram, channel, all_new_messages)

			return array_send_message_result
		finally:
			await self._client.disconnect()

	async def _sendMessagesInDB(self, all_new_messages) -> [str]:
		messages_dict_to_save = await self._prepareMessagesForSave(all_new_messages)
		if len(messages_dict_to_save) is not self._empty_list:
			result: InsertManyResult = await MongoRepositoryMessages().saveAllDicts(messages_dict_to_save)
			return [str(mongo_id) for mongo_id in result.inserted_ids]

	@staticmethod
	async def _prepareMessagesForSave(all_new_messages) -> []:
		messages_dict_to_save = []
		for message in all_new_messages:
			messages_dict_to_save.append(message.to_dict())
		_logger.debug(f'Prepared to save: {len(messages_dict_to_save)} items')
		return messages_dict_to_save

	async def _getLastMessageIdInTelegram(self, channel: Channel) -> int:
		last_message = await self._client.get_messages(channel.channel_id, limit=1)
		if len(last_message) is not self._empty_list:
			# Telegram receives messages from the end! Last message -> first in array
			last_mess_id_in_telegram = last_message[0].id
			_logger.debug(f'Last message ID in Telegram: {last_mess_id_in_telegram}')
			return last_mess_id_in_telegram

	async def _updateChannelInfoInDB(self, last_mess_id_in_telegram, channel: Channel, all_new_messages):
		if last_mess_id_in_telegram != channel.last_update_message_id:
			channel.last_update_message_id = last_mess_id_in_telegram
			channel.last_update_message_date = datetime.datetime.now()
			channel.message_total_count = await self._getTotalMessagesInChannel(channel.channel_id)
			_logger.debug(f'Channel for update: {channel.toDict()}')
			result = await ChannelService().saveDicts([channel.toDict()])
			_logger.debug(f'Channel updated: {len(result)}')

	async def _getTotalMessagesInChannel(self, channel_id) -> int:
		messages = await self._client.get_messages(channel_id)
		_logger.debug(f'Total messages: {messages.total}')
		return messages.total
