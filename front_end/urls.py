from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
	path('', views.index),
	path('test', views.test),
	path('tasks', views.page_tasks, name='tasks'),
	path('tasks/<int:task_id>', views.page_task_id),
	path('tasks/new', views.page_task_new, name='new_task'),
]
