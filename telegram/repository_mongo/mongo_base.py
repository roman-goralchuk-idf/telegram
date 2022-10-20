import json
import logging
from abc import ABC
from urllib.parse import quote_plus

import pymongo
from bson import json_util

from configuration.configurationloader import configService

_logger = logging.getLogger('custom')


class MongoRepository(ABC):

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

	async def saveOneDict(self, object_dict):
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

	async def saveAllDicts(self, array_dict):
		try:
			result = self._collection.insert_many(array_dict)
			_logger.debug(f'Inserted: {result.inserted_ids}')
			return result.acknowledged
		except IOError as e:
			_logger.error(e)

	async def findAllDictsBase(self):
		try:
			fields = {
				'_id': 0,
			}
			result = self._collection.find({}, fields)
			_logger.debug(f'Found notes from collection \'{self._collection.name}\': {str(result.count())}')
			return json.loads(json_util.dumps(list(result)))
		except Exception as e:
			_logger.error(e)
