import asyncio
import logging
import multiprocessing
import time

from celery import shared_task

from telegram.service.telegram_delivery_start import DeliveryService
from telegram.service.telegram_update_service import TelegramUpdateService

_logger = logging.getLogger('custom')


@shared_task
def celeryStartDeliveryTask():
	# asyncio.run(DeliveryService().startDelivery())
	_logger.debug("TASK START:")
	sec = 10
	for x in range(sec):
		_logger.debug(f' {multiprocessing.current_process().name} - {sec - x}')
		time.sleep(1)
	_logger.debug("TASK END.")


@shared_task
def celeryTelegramUpdateMessagesTask():
	asyncio.run(TelegramUpdateService().updateMessages())
