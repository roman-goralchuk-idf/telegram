import logging

from telegram.models.model_app_task import TaskDelivery, TasksSearchRequest
from telegram.repository_mongo.mongo_task import MongoRepositoryTask

_logger = logging.getLogger('custom')


class TaskService:

	@staticmethod
	async def newOrUpdateTask(task: TaskDelivery):
		return await MongoRepositoryTask().upsertOneByTaskId(task)

	@staticmethod
	async def findTasks(tasks_req: TasksSearchRequest) -> [TaskDelivery]:
		result: [TaskDelivery] = await MongoRepositoryTask().findTasksByParameters(tasks_req)
		return result

	@staticmethod
	async def findTasksById(task_id) -> TaskDelivery:
		result: TaskDelivery = await MongoRepositoryTask().findTaskById(task_id)
		return result

