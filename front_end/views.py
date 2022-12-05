import json
import logging

from django.shortcuts import render

from telegram.models.model_task_delivery import TaskDeliveryStatus

_logger = logging.getLogger('custom')


def _getTaskDeliveryStatuses() -> []:
	return [status.value for status in TaskDeliveryStatus]


def index(request):
	context = {
		"pagename": "How to start"
	}
	return render(request, "index.html", context=context)


def page_tasks(request):
	context = {
		"pagename": "Delivery tasks",
		"description": """
				Tasks service are created for mass sending of messages to clients. 
				The sending speed is limited, so tasks are created and transferred to the service for sending.
			""",
		"message_for_delivery": """
			If you click the button, all tasks with the status "ready for delivery" will be launched.
			You can come back to this page later and check the statuses...
		""",
		"message_for_new_task": """
				If you click the button, you will can make a new task
			""",
	}
	return render(request, 'tasks.html', context=context)


def page_task_id(request, task_id):
	context = {
		"pagename": f'Task {task_id}',
		"statuses": _getTaskDeliveryStatuses()
	}
	print(context)
	return render(request, "tasks_id.html", context=context)


def page_task_new(request):
	context = {
		"pagename": f'Create new task',
		"description": """
					Tasks service are created for mass sending of messages to clients. 
					The sending speed is limited, so tasks are created and transferred to the service for sending.
				""",
	}
	return render(request, "tasks_new.html", context=context)


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


def test(request):
	return render(request, "test.html")
