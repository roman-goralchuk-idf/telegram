from django.urls import path

from telegram.view.channel_view import ChannelHandler
from telegram.view.login_views import LoginHandler
from telegram.view.task_delivery_views import TasksDeliveryHandler, TaskStartHandler, TaskByIdDeliveryHandler
from telegram.view.update_views import UpdateHandler

app_name = 'telegram-api'
urlpatterns = [
	path('login/', LoginHandler.as_view(), name='login'),
	path('update/', UpdateHandler.as_view(), name='update_data'),
	path('tasks/', TasksDeliveryHandler.as_view(), name='tasks'),
	path('tasks/<int:task_id>', TaskByIdDeliveryHandler.as_view(), name='tasks_id'),
	path('tasks/start', TaskStartHandler.as_view(), name='tasks_start'),
	path('channels/', ChannelHandler.as_view(), name='channels'),
]
