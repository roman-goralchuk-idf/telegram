import logging

from celery import shared_task

from telegram import client_telegram
from telegram.service.telegram_delivery_start import DeliveryStartingService
from telegram.service.telegram_update_service import TelegramUpdateService

_logger = logging.getLogger('custom')


@shared_task
def celeryStartDelivery(deliveries_id):
	with client_telegram:
		client_telegram.loop.run_until_complete(DeliveryStartingService().startDeliveries(deliveries_id))


@shared_task
def celeryTelegramUpdateMessages():
	with client_telegram:
		client_telegram.loop.run_until_complete(TelegramUpdateService().updateMessages())

# @shared_task
# def celeryStartDeliveryTask(id_delivery):
# _logger.debug("TASK START:")
# _logger.debug(id_delivery)
# sec = 10
# for x in range(sec):
# 	_logger.debug(f' {multiprocessing.current_process().name} - {sec - x}')
# 	time.sleep(1)
# _logger.debug("TASK END.")
