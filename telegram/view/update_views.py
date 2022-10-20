from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.service.telegram_update_service import TelegramUpdateService


@method_decorator(csrf_exempt, name='dispatch')
class UpdateHandler(View):
	@staticmethod
	async def get(request):
		result = await TelegramUpdateService().updateMessages()
		data = {
			"update_result": result
		}
		return JsonResponse(data)
