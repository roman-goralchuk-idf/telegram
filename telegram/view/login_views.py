import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.service.login_service import LoginService

_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class LoginHandler(View):
	@staticmethod
	async def get(request):
		result = await LoginService().checkAuthorization()
		data = {
			"login": result
		}
		return JsonResponse(data)

	@staticmethod
	async def post(request):
		request_body = json.loads(request.body)
		code = request_body.get('code')
		result = await LoginService().sendReceivedCode(code)
		data = {
			"result": result
		}
		return JsonResponse(data)
