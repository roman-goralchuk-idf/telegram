import logging

from telegram.repository_mongo.models import Channel
from telegram.repository_mongo.mongo import MongoRepositoryChannel

_logger = logging.getLogger('custom')


class ChannelService:

	@staticmethod
	async def deleteByArrayId(channel_ids: []) -> []:
		result = await MongoRepositoryChannel().removeById(channel_ids)
		return result

	@staticmethod
	async def addArrayDict(array_dicts: []) -> []:
		result = await MongoRepositoryChannel().upsertArray(array_dicts)
		return result
	
	@staticmethod
	async def findArray(channel_ids: []) -> []:
		result = await MongoRepositoryChannel().findByIdOrAll(channel_ids)
		return result

	async def addArrayId(self, channel_ids: []) -> []:
		result = await MongoRepositoryChannel().upsertArray(await self._convertIdsToChannels(channel_ids))
		return result

	@staticmethod
	async def _convertIdsToChannels(channel_ids: []) -> []:
		array_channels_dict = []
		for channel_id in channel_ids:
			_logger.debug(channel_id)
			array_channels_dict.append(Channel(channel_id=channel_id).toDict())
		return array_channels_dict
