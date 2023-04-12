import logging

from django.shortcuts import render

from telegram.models.model_task_delivery import TaskDeliveryStatus

_logger = logging.getLogger('custom')


def _getDeliveryStatuses() -> []:
	return [status.value for status in TaskDeliveryStatus]


def index(request):
	context = {
		"pagename": "How to start"
	}
	return render(request, "index.html", context=context)


def page_deliveries(request):
	context = {
		"pagename": "Deliveries",
		"description": """
				Delivery service are created for mass sending of messages to clients. 
				The sending speed is limited, so deliveries are created and transferred to the service for sending.
			""",
		"message_for_delivery": """
			If you click the button, all deliveries with the status "ready for delivery" will be launched.
			You can come back to this page later and check the statuses...
		""",
		"message_for_new_delivery": """
				If you click the button, you will can make a new task
			""",
	}
	return render(request, 'deliveries.html', context=context)


def page_delivery_id(request, delivery_id):
	context = {
		"pagename": f'Task {delivery_id}',
		"statuses": _getDeliveryStatuses()
	}
	print(context)
	return render(request, "delivery_id.html", context=context)


def page_delivery_new(request):
	context = {
		"pagename": f'Create new Delivery',
		"description": """
					Delivery service are created for mass sending of messages to clients. 
					The sending speed is limited (no more than 30 messages per second), so tasks are created and transferred to the service for sending.
				""",
	}
	return render(request, "delivery_new.html", context=context)


def error_404_page_not_found_view(request, exception):
	data = {
		"pagename": "404",
		"message": "Page not found!"
	}
	return render(request, "404.html", context=data)


def error_500_error_view(request):
	data = {
		"pagename": "500",
		"message": "Server error!"
	}
	return render(request, "500.html", context=data)


def error_400_bad_request_view(request, exception):
	data = {
		"pagename": "400",
		"message": "Bad request!"
	}
	return render(request, "400.html", context=data)


def error_403_permission_denied_view(request, exception):
	data = {
		"pagename": "403",
		"message": "Permission denied!"
	}
	return render(request, "403.html", context=data)
