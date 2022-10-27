from asyncio import sleep

from celery import shared_task

from telegram.service.telegram_tasks_start import TasksStartService


@shared_task()
async def celeryStartDeliveryTask(task_ids: [int]):
	await TasksStartService().startDelivery(task_ids)
