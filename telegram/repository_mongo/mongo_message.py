import json
import logging

from bson import json_util

from configuration.configurationloader import configService
from telegram.repository_mongo.mongo_base import MongoRepository

_logger = logging.getLogger('custom')


class MongoRepositoryMessages(MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionMessage']
		self._collection = self._database[self._collection_name]

	async def findDictAll(self, limit, message_id, channel_id):
		try:
			query = {
				'id': message_id,
				'peer_id.channel_id': channel_id
			}
			fields = {
				'_id': 0,
				}
			result = self._collection.find(query, fields).limit(limit)
			_logger.debug(f'Found notes from collection \'{self._collection.name}\': {str(result.count())}')
			return json.loads(json_util.dumps(list(result)))
		except Exception as e:
			_logger.error(e)