import json
import logging

from celery.result import AsyncResult
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.service.time_service import DateTimeEncoder

_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class CeleryStatusHandler(View):
	@staticmethod
	async def get(request, task_id):
		task = AsyncResult(task_id)

		if task.state == 'FAILURE' or task.state == 'PENDING':
			response = {
				'task_id': task_id,
				'state': task.state,
				'progression': "None",
				'info': task.info
			}
			return HttpResponse(response, content_type='application/json', status=200)
		response = {
			'task_id': task_id,
			'state': task.state,
			'progression': task.date_done,
			'info': "None"
		}
		return HttpResponse(json.dumps(response, cls=DateTimeEncoder), content_type='application/json', status=200)
