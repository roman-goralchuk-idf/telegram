import json
import logging
from urllib.parse import quote_plus

import pymongo
from bson import json_util

from configuration.configurationloader import configService

_logger = logging.getLogger('custom')


class _MongoRepository:

	def __init__(self):
		self._collection = None
		self._username = configService['database']['mongo']['user']
		self._password = configService['database']['mongo']['password']
		self._host = configService['database']['mongo']['host']
		self._port = configService['database']['mongo']['port']
		self._databaseName = configService['database']['mongo']['databaseName']
		self._uri = "mongodb://%s:%s@%s:%s" % (quote_plus(self._username), quote_plus(self._password), self._host, self._port)
		try:
			clientMongoDb = pymongo.MongoClient(self._uri)
			result = clientMongoDb.server_info()
			if result is not None:
				data = json.loads(json.dumps(result))
				_logger.debug(f'Connection to \'{self._databaseName}\' is successfully, mongo version is: {data["version"]}')
			self._database = clientMongoDb[self._databaseName]
		except Exception as e:
			_logger.error(e)

	async def saveOne(self, object_dict):
		try:
			result = self._collection.insert_one(object_dict)
			response = {
				"operation_result": result.acknowledged,
				"_id": result.inserted_id
			}
			_logger.debug(response)
			return response
		except IOError as e:
			_logger.error(e)

	async def saveAll(self, array_dict):
		try:
			result = self._collection.insert_many(array_dict)
			response = {
				"operation_result": result.acknowledged,
				"list_id": len(result.inserted_ids)
			}
			print(response)
			_logger.debug(response)
			return response
		except IOError as e:
			_logger.error(e)


class MongoRepositoryMessages(_MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionMessage']
		self._collection = self._database[self._collection_name]

	async def findAll(self, limit, message_id, channel_id):
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


class MongoRepositoryChannel(_MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionChannel']
		self._collection = self._database[self._collection_name]
		_logger.debug(self._collection)

	async def upsertArray(self, channels_dict: []) -> []:
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

	async def findByIdOrAll(self, channel_ids: []) -> []:
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
			array = []
			for channel in result:
				array.append(channel)
			return array
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
