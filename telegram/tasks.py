import asyncio
import logging
import time

from celery import shared_task

from telegram.service.telegram_tasks_start import TasksStartService
from telegram.service.telegram_update_service import TelegramUpdateService

_logger = logging.getLogger('custom')


@shared_task
def celeryStartDeliveryTask(task_ids: [int]):
	asyncio.run(TasksStartService().startDelivery(task_ids))


@shared_task
def celeryTelegramUpdateMessagesTask():
	asyncio.run(TelegramUpdateService().updateMessages())


async def testTask():
	_logger.debug("TASK START:")
	sec = 5
	for x in range(sec):
		_logger.debug(f' o - {sec - x}')
		time.sleep(1)
	_logger.debug("TASK END.")
	return "STOP"
