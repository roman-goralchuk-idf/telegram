import datetime
import logging

from telegram.models.model_task_delivery import TasksSearchRequest, TaskDeliveryStatus, TaskDelivery
from telegram.repository_mongo.mongo_task import MongoRepositoryTask
from telegram.service.delivery_task_service import DeliveryTaskService
from telegram.service.telegram_client_service import TelegramApiService, checkConnection
from telegram.service.telegram_conversation_service import ConversationService
from telegram.service.time_service import TimeService

_logger = logging.getLogger('custom')


class DeliveryService:
	def __init__(self):
		self._client = TelegramApiService().getTelegramClient()

	async def startDelivery(self, id_delivery):
		try:
			await self._client.connect()
			# await checkConnection(client=self._client)
			task = await DeliveryTaskService.findTasksById(id_delivery)
			_logger.debug(f'Task #{task.task_id} ready to start')
			result_status = await ConversationService().sendAllMessages(task, self._client)
			task.status = result_status
			task.performed_date = datetime.datetime.now(tz=TimeService().getTimeZone())
			await MongoRepositoryTask().upsertOneByTaskId(task)
		finally:
			await self._client.disconnect()
			# await checkConnection(client=self._client)
