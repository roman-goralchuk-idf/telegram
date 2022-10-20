import logging

from telegram.models.model_channel import Channel
from telegram.repository_mongo.mongo_channel import MongoRepositoryChannel

_logger = logging.getLogger('custom')


class ChannelService:

	@staticmethod
	async def deleteByArrayId(channel_ids: []) -> []:
		result = await MongoRepositoryChannel().removeById(channel_ids)
		return result

	@staticmethod
	async def saveDicts(array_dicts: []) -> []:
		result = await MongoRepositoryChannel().upsertArrayDicts(array_dicts)
		return result
	
	@staticmethod
	async def findArray(channel_ids: []) -> []:
		result = await MongoRepositoryChannel().findDictByIdOrAll(channel_ids)
		return result

	async def saveArrayId(self, channel_ids: []) -> []:
		result = await MongoRepositoryChannel().upsertArrayDicts(await self._convertIdsToChannels(channel_ids))
		return result

	@staticmethod
	async def getChannelByStatus(status) -> []:
		result = await MongoRepositoryChannel().findChannelByStatus(status)
		return result

	@staticmethod
	async def _convertIdsToChannels(channel_ids: []) -> []:
		array_channels_dict = []
		for channel_id in channel_ids:
			_logger.debug(channel_id)
			array_channels_dict.append(Channel(channel_id=channel_id).toDict())
		return array_channels_dict
