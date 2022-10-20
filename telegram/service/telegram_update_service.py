import datetime
import logging

from telegram.models.model_channel import StatusChannel, Channel
from telegram.repository_mongo.mongo_message import MongoRepositoryMessages
from telegram.service.channel_service import ChannelService
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
			array_response = []
			array_channel = await ChannelService().getChannelByStatus(StatusChannel.IN_WORK.value)

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
				result = await self._sendMessagesInDB(channel, last_mess_id_in_telegram, all_new_messages)
				array_response.append(result)
				await self._updateChannelInfoInDB(last_mess_id_in_telegram, channel, all_new_messages)

			return array_response
		finally:
			await self._client.disconnect()

	async def _sendMessagesInDB(self, channel: Channel, last_mess_id_in_channel, all_new_messages) -> {}:
		messages_dict_to_save = await self._prepareMessagesForSave(all_new_messages)
		result = 'not updated'
		if len(messages_dict_to_save) is not self._empty_list:
			result = await MongoRepositoryMessages().saveAllDicts(messages_dict_to_save)
		return {
				"channel_id": channel.channel_id,
				"new_messages": len(messages_dict_to_save),
				"update_result": result,
				"last_id": last_mess_id_in_channel
			}

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
