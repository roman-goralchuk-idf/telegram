import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.models.model_task import TasksRequest, TaskDelivery
from telegram.service.task_service import TaskService

_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class TaskHandler(View):
	@staticmethod
	async def get(request):
		request_body = json.loads(request.body)
		tasks_req = TasksRequest(None, None)
		tasks_req.fromDict(request_body)
		result = await TaskService().findTasks(tasks_req)
		response = {
			"result": result
		}
		return JsonResponse(response)

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
class TaskStartHandler(View):
	@staticmethod
	async def post(request):
		request_body = json.loads(request.body)
		ids: [int] = request_body.get('ids_to_start')
		result = await TaskService().startTasks(ids)
		_logger.debug(f'Tasks started: {result}')
		response = {
			"start_tasks": result
		}
		return JsonResponse(response)