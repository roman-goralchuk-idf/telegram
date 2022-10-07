import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.telegramConnector import TelegramHandler


@method_decorator(csrf_exempt, name='dispatch')
class TelegramRegistration(View):
	@staticmethod
	async def get(request):
		data = {
			"result": await TelegramHandler.checkConnection()
		}
		return JsonResponse(data)

	@staticmethod
	async def post(request):
		post_body = json.loads(request.body)
		code = post_body.get('code')
		data = {
			"result": await TelegramHandler.sendCode(code)
		}
		return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class Mongo(View):
	@staticmethod
	async def get(request):
		print(x)
		data = {
			"result": "Hello"
		}
		return JsonResponse(data)

	@staticmethod
	async def post(request):
		data = {
			"result": "Bye"
		}
		return JsonResponse(data)
