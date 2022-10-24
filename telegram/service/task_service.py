import logging

from telegram.models.model_task import TaskDelivery, TasksSearchRequest
from telegram.repository_mongo.mongo_task import MongoRepositoryTask

_logger = logging.getLogger('custom')


class TaskService:

	@staticmethod
	async def newOrUpdateTask(task: TaskDelivery):
		return await MongoRepositoryTask().upsertOneByTaskId(task)

	@staticmethod
	async def findTasks(tasks_req: TasksSearchRequest) -> []:
		result = await MongoRepositoryTask().findTasksByParameters(tasks_req)
		return [task.toDict() for task in result]

