from django.urls import path

from telegram.view.channel_views import ChannelHandler
from telegram.view.login_views import LoginHandler
from telegram.view.delivery_views import DeliveryHandler, DeliveryStartHandler, DeliveryByIdHandler
from telegram.view.update_views import UpdateHandler

app_name = 'telegram-api'
urlpatterns = [
	path('login/', LoginHandler.as_view(), name='login'),
	path('update/', UpdateHandler.as_view(), name='update'),
	path('tasks/', DeliveryHandler.as_view(), name='tasks'),
	path('tasks/<int:task_id>', DeliveryByIdHandler.as_view(), name='tasks_id'),
	path('tasks/start', DeliveryStartHandler.as_view(), name='tasks_start'),
	path('channels/', ChannelHandler.as_view(), name='channels'),
]
