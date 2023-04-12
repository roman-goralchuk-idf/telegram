import logging

from telegram.models.model_task_delivery import TaskDelivery, TasksSearchRequest
from telegram.repository_mongo.mongo_delivery import MongoRepositoryDelivery

_logger = logging.getLogger('custom')


class DeliveryTaskService:

	@staticmethod
	async def newOrUpdateTask(task: TaskDelivery):
		return await MongoRepositoryDelivery().upsertOneById(task)

	@staticmethod
	async def findTasks(tasks_req: TasksSearchRequest) -> [TaskDelivery]:
		result: [TaskDelivery] = await MongoRepositoryDelivery().findTasksByParameters(tasks_req)
		return result

	@staticmethod
	async def findTasksById(delivery_id) -> TaskDelivery:
		result: TaskDelivery = await MongoRepositoryDelivery().findById(delivery_id)
		return result

