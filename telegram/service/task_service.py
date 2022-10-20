import logging

from telegram.models.model_task import TaskDelivery, TasksRequest, TaskDeliveryStatus
from telegram.repository_mongo.mongo_task import MongoRepositoryTask
from telegram.service.telegram_conversation_service import ConversationService

_logger = logging.getLogger('custom')


class TaskService:

	@staticmethod
	async def startTasks(task_ids: [int]) -> []:
		request = TasksRequest(task_ids, TaskDeliveryStatus.READY_FOR_DELIVERY.name_status)
		_logger.debug(f'Request to start: {request.toDict()}')
		tasks: [TaskDelivery] = await MongoRepositoryTask().findTaskByParameters(request)
		for task in tasks:
			await ConversationService().sendAllMessages(task)
		return [(task.task_id, task.message, task.delivery_scheduled) for task in tasks]

	@staticmethod
	async def newOrUpdateTask(task: TaskDelivery):
		return await MongoRepositoryTask().upsertOneByTaskId(task)

	@staticmethod
	async def findTasks(tasks_req: TasksRequest) -> []:
		result = await MongoRepositoryTask().findTaskByParameters(tasks_req)
		return [task.toDict() for task in result]

