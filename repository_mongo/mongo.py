import json
import logging
from urllib.parse import quote_plus

import pymongo
from bson import json_util

from configuration.configurationloader import configService

_logger = logging.getLogger('custom')


class MongoRepository:
	_username = configService['database']['mongo']['user']
	_password = configService['database']['mongo']['password']
	_host = configService['database']['mongo']['host']
	_port = configService['database']['mongo']['port']
	_databaseName = configService['database']['mongo']['databaseName']
	_uri = "mongodb://%s:%s@%s:%s" % (quote_plus(_username), quote_plus(_password), _host, _port)

	def __init__(self):
		try:
			clientMongoDb = pymongo.MongoClient(self._uri)
			self._database = clientMongoDb[self._databaseName]
			result = clientMongoDb.server_info()
			if result is not None:
				data = json.loads(json.dumps(result))
				_logger.debug(f'Connection to {self._databaseName} successfully, mongo version is: ' + data['version'])
		except Exception as e:
			_logger.error(e)

	async def saveAll(self, data, collection):
		try:
			collection = self._database[collection]
			result = collection.insert_many(data)
			response = {
				"operation_result": result.acknowledged,
				"list_id": len(result.inserted_ids)
			}
			_logger.debug(response)
			return response
		except IOError as e:
			_logger.error(e)

	async def findAll(self, collection, limit, message_id, channel_id):
		try:
			collection = self._database[collection]
			find_parameters = {
				'id': message_id,
				'peer_id.channel_id': channel_id
			}
			fields = {
				'_id': 0,
				}
			result = collection.find(find_parameters, fields).limit(limit)
			_logger.debug(f'Found notes from collection \'{collection.name}\': {str(result.count())}')
			return json.loads(json_util.dumps(list(result)))
		except Exception as e:
			_logger.error(e)
