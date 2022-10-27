import logging

import pymongo

from configuration.configurationloader import configService
from telegram.models.model_app_task import TaskDelivery, TasksSearchRequest
from telegram.repository_mongo.mongo_base import MongoRepository

_logger = logging.getLogger('custom')


class MongoRepositoryTask(MongoRepository):

	def __init__(self):
		super().__init__()
		self._collection_name = configService['database']['mongo']['collectionTask']
		self._collection = self._database[self._collection_name]

	async def upsertOneByTaskId(self, task: TaskDelivery):
		try:
			if task.task_id is None:
				task.task_id = await self._generateTaskId()
			query = {
				"task_id": task.task_id
			}
			value = {
				"$set": task.toDict()
			}
			result = self._collection.update_many(filter=query, update=value, upsert=True)
			operation_response = {
				"task_id": task.task_id,
				"operation_result": result.acknowledged,
				"update_count": result.modified_count
			}
			_logger.debug(operation_response)
			return operation_response
		except Exception as e:
			_logger.error(e)

	async def findTaskById(self, task_id) -> TaskDelivery:
		try:
			query = {
				"task_id": task_id
			}
			task_found_dict = self._collection.find_one(query)
			task: TaskDelivery = TaskDelivery(None, None, None, None)
			task.fromDict(task_found_dict)
			_logger.debug(f'Task found: {task.task_id}')
			return task
		except Exception as e:
			_logger.error(e)

	async def findTasksByParameters(self, tasks: TasksSearchRequest) -> [TaskDelivery]:
		try:
			query = {}
			if len(tasks.task_ids) != 0:
				query['task_id'] = {'$in': tasks.task_ids}
			if tasks.status is not None:
				query['status'] = tasks.status
			fields = {
				'_id': 0
			}
			_logger.debug(f'For find {query}')
			tasks_dicts: [] = self._collection.find(query, fields)
			tasks: [TaskDelivery] = []
			for task_dict in tasks_dicts:
				task: TaskDelivery = TaskDelivery(None, None, None, None)
				task.fromDict(task_dict)
				_logger.debug(f'Task found: {task.task_id}')
				tasks.append(task)
			return tasks
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
