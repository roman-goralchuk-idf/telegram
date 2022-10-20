import logging

from configuration.configurationloader import configService
from telegram.models.model_channel import Channel
from telegram.repository_mongo.mongo_base import MongoRepository

_logger = logging.getLogger('custom')


class MongoRepositoryChannel(MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionChannel']
		self._collection = self._database[self._collection_name]
		_logger.debug(self._collection)

	async def upsertArrayDicts(self, channels_dict: []) -> []:
		try:
			array_response = []
			for data in channels_dict:
				query = {
					"channel_id": data.get('channel_id'),
					}
				value = {
					"$set": data
				}
				result = self._collection.update_many(filter=query, update=value, upsert=True)
				operation_response = {
					"channel_id": data.get('channel_id'),
					"operation_result": result.acknowledged,
					"update_count": result.modified_count
				}
				array_response.append(operation_response)
			_logger.debug(array_response)
			return array_response
		except Exception as e:
			_logger.error(e)

	async def findDictByIdOrAll(self, channel_ids: []) -> []:
		try:
			if len(channel_ids) == 0:
				query = {}
			else:
				query = {
					'channel_id': {'$in': channel_ids}
				}
			fields = {
				'_id': 0,
				}
			_logger.debug(f'For find {query}')
			result = self._collection.find(query, fields)
			array_channel = []
			for channel in result:
				array_channel.append(channel)
			return array_channel
		except Exception as e:
			_logger.error(e)

	async def removeById(self, channel_ids: []) -> []:
		try:
			query = {
				'channel_id': {'$in': channel_ids}
			}
			_logger.debug(f'For delete {query}')
			result = self._collection.delete_many(query)
			return result.deleted_count
		except Exception as e:
			_logger.error(e)

	async def findChannelByStatus(self, status) -> [Channel]:
		try:
			query = {
				'status': status
			}
			fields = {
				'_id': 0,
			}
			result = self._collection.find(query, fields)
			array_channel = []
			for channel_dict in result:
				ob = Channel(None)
				ob.fromDict(channel_dict)
				array_channel.append(ob)
			return array_channel
		except Exception as e:
			_logger.error(e)