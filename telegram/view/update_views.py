import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.repository_mongo.mongo import MongoRepositoryMessages


@method_decorator(csrf_exempt, name='dispatch')
class UpdateHandler(View):
	@staticmethod
	async def get(request):
		request_body = json.loads(request.body)
		limit = request_body.get('limit')
		message_id = request_body.get('message_id')
		channel_id = request_body.get('channel_id')
		result = await MongoRepositoryMessages.findAll(limit, message_id, channel_id)
		print(result)
		return JsonResponse(result, json_dumps_params={'ensure_ascii': False}, safe=False)

	@staticmethod
	async def post(request):
		data = {
			"result": "Bye"
		}
		return JsonResponse(data)
