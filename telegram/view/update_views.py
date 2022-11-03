import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.tasks import celeryTelegramUpdateMessagesTask


@method_decorator(csrf_exempt, name='dispatch')
class UpdateHandler(View):
	@staticmethod
	async def get(request):
		celeryTelegramUpdateMessagesTask.delay()
		response = {
			"response": "Update process started"
		}
		return HttpResponse(json.dumps(response), content_type='application/json')
