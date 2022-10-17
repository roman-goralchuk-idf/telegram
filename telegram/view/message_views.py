from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class MessageHandler(View):
	@staticmethod
	async def get(request):
		data = {
			"result": "hello"
		}
		return JsonResponse(data)

	@staticmethod
	async def post(request):
		data = {
			"result": "bye"
		}
		return JsonResponse(data)
