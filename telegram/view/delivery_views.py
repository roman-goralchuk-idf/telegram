import json
import logging

from celery.result import AsyncResult
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from celery_django import celery_app
from celery_django.celeryapp import get_celery_life
from telegram.models.model_app_task import TasksSearchRequest, TaskDelivery
from telegram.models.model_error_response import ErrorResponse
from telegram.service.task_service import TaskService
from telegram.service.time_service import DateTimeEncoder
from telegram.tasks import celeryStartDeliveryTask, celeryTelegramUpdateMessagesTask

_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryHandler(View):
	@staticmethod
	async def get(request):
		request_body = json.loads(request.body)
		tasks_req = TasksSearchRequest(None, None)
		tasks_req.fromDict(request_body)
		result = await TaskService().findTasks(tasks_req)
		result_dicts = [i.toDict() for i in result]
		response = json.dumps(result_dicts, cls=DateTimeEncoder)
		return HttpResponse(response, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryByIdHandler(View):

	@staticmethod
	async def get(request, task_id):
		result: TaskDelivery = await TaskService().findTasksById(task_id)
		if result is not None:
			result_dicts = result.toDict()
			_logger.debug(result_dicts)
			response = json.dumps(result_dicts, cls=DateTimeEncoder)
			return HttpResponse(response, content_type='application/json')
		else:
			error_response = json.dumps(ErrorResponse(f'Task with id \'{task_id}\' not found').__dict__)
			return HttpResponse(error_response, content_type='application/json')

	@staticmethod
	async def post(request):
		request_body = json.loads(request.body)
		task: TaskDelivery = TaskDelivery(None, None, None, None)
		task.fromDict(request_body)
		result = await TaskService().newOrUpdateTask(task)
		response = {
			"result": result
		}
		return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryStartHandler(View):
	@staticmethod
	def post(request):

		result = celeryStartDeliveryTask.delay()
		_logger.debug(f'Result: {result}')
		id_task = result.task_id
		celery_task = AsyncResult(id_task)
		result_status = celery_task.state
		_logger.debug(result_status)
		data = {
			"response": "Delivery messages started",
			"task_process": get_celery_life()
		}
		return HttpResponse(json.dumps(data), content_type='application/json')


