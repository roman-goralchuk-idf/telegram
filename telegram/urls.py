from django.urls import path

from telegram.view.channel_view import ChannelHandler
from telegram.view.login_views import LoginHandler
from telegram.view.task_views import TaskHandler, TaskStartHandler
from telegram.view.update_views import UpdateHandler

urlpatterns = [
	path('login/', LoginHandler.as_view()),
	path('update/', UpdateHandler.as_view()),
	path('tasks/', TaskHandler.as_view()),
	path('tasks/start', TaskStartHandler.as_view()),
	path('channels/', ChannelHandler.as_view()),
]
