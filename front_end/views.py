import json
import logging

import requests
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse

from front_end.forms import TaskForm

_logger = logging.getLogger('custom')


def _getDataFromLocalURL(request: HttpRequest, body, local_url, dynamic_id):
	if dynamic_id is not None:
		url = request.build_absolute_uri(reverse(local_url, kwargs={'task_id': dynamic_id}))
	else:
		url = request.build_absolute_uri(reverse(local_url))
	_logger.debug(f'URL: {url}')
	response = requests.get(url=url, data=json.dumps(body))
	response_json = response.json()
	_logger.debug(f'Receive JSON from API: {response_json}')
	return response_json


def index(request):
	data = {
		"pagename": "How to start"
	}
	return render(request, "index.html", context=data)


def page_tasks(request):
	context = {
		"pagename": "Delivery tasks",
		"description": """
				About tasks text....
			""",
		"message_for_delivery": """
			If you click the button, all tasks with the status "ready for delivery" will be launched.
			You can come back to this page later and check the statuses...
		""",
		"tasks": _getDataFromLocalURL(
			request,
			body={
				"task_ids": []
			},
			local_url='telegram-api:tasks',
			dynamic_id=None
		),
	}
	# if request.method == "GET":
	# 	task_id = request.GET.get("task_id")
	# 	print(bodys)
	return render(request, 'tasks.html', context=context)


def page_tasks_id(request, task_id):
	context = {
		"pagename": f'Task {task_id}',
		"task": _getDataFromLocalURL(
			request,
			body=None,
			local_url='telegram-api:tasks_id',
			dynamic_id=task_id
		),
	}
	return render(request, "tasks_id.html", context=context)


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
	# langs = ["Python", "JavaScript", "Java", "C#", "C++"]  # список
	# user = {"name": "Tom", "age": 23}  # словарь
	# address = ("Абрикосовая", 23, 45)  # кортеж
	# colors = {"red": "красный", "green": "зеленый", "blue":"синий"} # словарь
	# cities = [
	# 	{'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
	# 	{'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
	# 	{'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
	# 	{'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
	# 	{'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
	# ]
	# data = {
	# 	"pagename": "Test page",
	# 	"langs": langs,
	# 	"user": user,
	# 	"address": address,
	# 	"person": Person("Tom"),
	# 	"n": -5,
	# 	"colors": colors,
	# 	"cities": cities,
	# 	"my_date": datetime.now(),
	# 	"form": UserForm()
	# }
	# if request.method == "POST":
	# 	name = request.POST.get("name")
	# 	age = request.POST.get("age")
	# 	print(f'Привет, {name}, твой возраст: {age}')

	# r = requests.get(url=reverse('telegram-api:tasks'))
	# print(r)
	# postgrest_urls = f"http://localhost:3000/rpc/bucketreturn?p_stocks=%7B{symbols_unicode}%7D"
	# response = requests.get(postgrest_urls, headers={'Content-Type': 'application/json'}).json()

	context = {
		"pagename": "Test page",
		"tasks": _getDataFromLocalURL(request, local_url='telegram-api:tasks'),
		"form": TaskForm(),

	}

	if request.method == "POST":
		task_id = request.POST.get("task_id")
		status = request.POST.get("status")
		bodys = {
			'task_ids': [task_id],
			'status': status
		}
		print(bodys)

	return render(request, "test.html", context=context)
