import datetime
import logging

from telegram.models.model_task_delivery import TaskDelivery
from telegram.repository_mongo.mongo_delivery import MongoRepositoryDelivery
from telegram.service.delivery_task_service import DeliveryTaskService
from telegram.service.telegram_client_service import TelegramApiService
from telegram.service.telegram_conversation_service import ConversationService
from telegram.service.time_service import TimeService

_logger = logging.getLogger('custom')


class DeliveryStartingService:

	async def startDeliveries(self, deliveries_id):
		for id_delivery in deliveries_id:
			await self.startDelivery(id_delivery)

	@staticmethod
	async def startDelivery(id_delivery):
		client_telegram = TelegramApiService().getTelegramClient()
		delivery: TaskDelivery = await DeliveryTaskService.findTasksById(id_delivery)
		_logger.debug(f'Delivery #{delivery.task_id} ready to start')
		result_status = await ConversationService().sendAllMessages(delivery, client_telegram)
		delivery.status = result_status
		delivery.performed_date = datetime.datetime.now(tz=TimeService().getTimeZone())
		await MongoRepositoryDelivery().upsertOneById(delivery)
