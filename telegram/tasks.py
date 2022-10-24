from asyncio import sleep

from celery import shared_task

from telegram.service.telegram_tasks_start import TasksStartService


@shared_task()
async def startDeliveryTask(task_ids: [int]):
	await sleep(20)
	await TasksStartService().startDelivery(task_ids)
