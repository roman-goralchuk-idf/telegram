import datetime
import logging

from celery import shared_task

from telegram.models.model_app_task import TasksSearchRequest, TaskDeliveryStatus, TaskDelivery
from telegram.repository_mongo.mongo_task import MongoRepositoryTask
from telegram.service.telegram_client_service import TelegramApiService, checkConnection
from telegram.service.telegram_conversation_service import ConversationService
from telegram.service.time_service import TimeService

_logger = logging.getLogger('custom')


class TasksStartService:
	def __init__(self):
		self._client = TelegramApiService().getTelegramClient()

	async def startDelivery(self, task_ids: [int]):
		try:
			await self._client.connect()
			await checkConnection(client=self._client)
			search_request = TasksSearchRequest(task_ids, TaskDeliveryStatus.READY_FOR_DELIVERY.name_status)
			_logger.debug(f'Search request: {search_request.toDict()}')
			tasks_found: [TaskDelivery] = await MongoRepositoryTask().findTasksByParameters(search_request)
			_logger.debug(f'Found {len(tasks_found)} tasks')
			for task in tasks_found:
				_logger.debug(f'Task #{task.task_id} ready to start')
				result_status = await ConversationService().sendAllMessages(task, self._client)
				task.status = result_status
				task.performed_date = datetime.datetime.now(tz=TimeService().getTimeZone())
				await MongoRepositoryTask().upsertOneByTaskId(task)
		finally:
			await self._client.disconnect()
			await checkConnection(client=self._client)
