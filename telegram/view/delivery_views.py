import asyncio
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from celery_django.celeryapp import get_celery_life
from telegram.models.model_error_response import ErrorResponse
from telegram.models.model_task_delivery import TaskDelivery, TasksSearchRequest, TaskDeliveryStatus
from telegram.service.delivery_task_service import DeliveryTaskService
from telegram.service.time_service import DateTimeEncoder
from telegram.tasks import celeryStartDelivery

_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryHandler(View):
	@staticmethod
	def post(request):
		request_body = json.loads(request.body)
		tasks_req = TasksSearchRequest(None, None)
		tasks_req.fromDict(request_body)
		result = asyncio.run(DeliveryTaskService().findTasks(tasks_req))
		result_dicts = [i.toDict() for i in result]
		response = json.dumps(result_dicts, cls=DateTimeEncoder)
		return HttpResponse(response, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryTaskHandler(View):

	@staticmethod
	async def get(request, delivery_id):
		result: TaskDelivery = await DeliveryTaskService().findTasksById(delivery_id)
		if result is not None:
			result_dicts = result.toDict()
			_logger.debug(result_dicts)
			response = json.dumps(result_dicts, cls=DateTimeEncoder)
			return HttpResponse(response, content_type='application/json')
		else:
			error_response = json.dumps(ErrorResponse(f'Delivery with id \'{delivery_id}\' not found').__dict__)
			return HttpResponse(error_response, content_type='application/json')

	@staticmethod
	async def post(request):
		request_body = json.loads(request.body)
		delivery: TaskDelivery = TaskDelivery(None, None, None, None)
		delivery.fromDict(request_body)
		result = await DeliveryTaskService().newOrUpdateTask(delivery)
		response = {
			"result": result
		}
		return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryStartHandler(View):
	@staticmethod
	async def post(request):
		search_request = TasksSearchRequest(status=TaskDeliveryStatus.READY_FOR_DELIVERY.name_status)
		_logger.debug(f'Search request: {search_request.toDict()}')
		deliveries_found: [TaskDelivery] = await DeliveryTaskService.findTasks(search_request)
		if deliveries_found is not None and len(deliveries_found) != 0:
			_logger.debug(f'Found {len(deliveries_found)} tasks')
			deliveries_id = [i.task_id for i in deliveries_found]
			celeryStartDelivery.delay(deliveries_id)
			data = {
				"response": "Delivery messages started",
				"task_process": f'Process is {get_celery_life()}'
			}
		else:
			data = {
				"response": "Not found tasks for delivery",
				"task_process": f'Process is {get_celery_life()}'
			}
		return HttpResponse(json.dumps(data), content_type='application/json')
