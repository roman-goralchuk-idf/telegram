import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from telegram.service.channel_service import ChannelService
_logger = logging.getLogger('custom')


@method_decorator(csrf_exempt, name='dispatch')
class ChannelHandler(View):
	@staticmethod
	async def get(request):
		request_body = json.loads(request.body)
		channel_ids: [] = request_body.get('channel_ids')
		result = await ChannelService().findArray(channel_ids)
		data = {
			"channels": result
		}
		return JsonResponse(data)

	@staticmethod
	async def post(request):
		request_body = json.loads(request.body)
		channel_ids: [] = request_body.get('channel_ids')
		result = await ChannelService().saveArrayId(channel_ids)
		data = {
			"result": result
		}
		return JsonResponse(data)

	@staticmethod
	async def put(request):
		array_channels = json.loads(request.body)
		result = await ChannelService().saveDicts(array_channels)
		data = {
			"result": result
		}
		return JsonResponse(data)

	@staticmethod
	async def delete(request):
		request_body = json.loads(request.body)
		channel_ids: [] = request_body.get('channel_ids')
		result = await ChannelService().deleteByArrayId(channel_ids)
		data = {
			"result": result
		}
		return JsonResponse(data)
