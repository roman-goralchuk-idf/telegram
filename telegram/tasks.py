import asyncio
import logging

from celery import shared_task

from telegram.service.telegram_delivery_start import DeliveryService
from telegram.service.telegram_update_service import TelegramUpdateService

_logger = logging.getLogger('custom')


@shared_task
def celeryStartDeliveryTask(id_delivery):
	asyncio.get_event_loop().run_until_complete(DeliveryService().startDelivery(id_delivery))


# @shared_task
# def celeryStartDeliveryTask(id_delivery):
# 	task = DeliveryService().startDelivery(id_delivery)
# 	asyncio.run(task)
# _logger.debug("TASK START:")
# _logger.debug(id_delivery)
# sec = 10
# for x in range(sec):
# 	_logger.debug(f' {multiprocessing.current_process().name} - {sec - x}')
# 	time.sleep(1)
# _logger.debug("TASK END.")


@shared_task
def celeryTelegramUpdateMessagesTask():
	asyncio.run(TelegramUpdateService().updateMessages())
