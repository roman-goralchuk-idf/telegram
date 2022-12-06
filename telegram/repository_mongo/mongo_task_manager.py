import logging

import pymongo

from configuration.configurationloader import configService
from telegram.models.model_delivery import TelegramDelivery, TasksSearchRequest
from telegram.repository_mongo.mongo_base import MongoRepository

_logger = logging.getLogger('custom')


class MongoRepositoryTaskManager(MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionTask']
		self._collection = self._database[self._collection_name]

	async def upsertOneById(self, task: TelegramDelivery):
		try:
			if task.del_id is None:
				task.del_id = await self._generateTaskId()
			query = {
				"task_id": task.del_id
			}
			value = {
				"$set": task.toDict()
			}
			result = self._collection.update_many(filter=query, update=value, upsert=True)
			operation_response = {
				"task_id": task.del_id,
				"operation_result": result.acknowledged,
				"update_count": result.modified_count
			}
			_logger.debug(operation_response)
			return operation_response
		except Exception as e:
			_logger.error(e)

	async def findById(self, task_id) -> TelegramDelivery:
		try:
			query = {
				"task_id": task_id
			}
			fields = {
				'_id': 0
			}
			task_found_dict = self._collection.find_one(query, fields)
			_logger.debug(f'Result: {task_found_dict}')
			if task_found_dict is not None:
				task: TelegramDelivery = TelegramDelivery()
				task.fromDict(task_found_dict)
				return task
		except Exception as e:
			_logger.error(e)

	async def _generateTaskId(self) -> int:
		try:
			result = self._collection.find().sort('task_id', pymongo.DESCENDING).limit(1)
			next_number: int = 1
			for i in result:
				next_number = int(i['task_id']) + 1
				print(next_number)
			return next_number
		except Exception as e:
			_logger.error(e)