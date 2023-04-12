from django.urls import path

from telegram.view.channel_views import ChannelHandler
from telegram.view.login_views import LoginHandler
from telegram.view.delivery_views import DeliveryHandler, DeliveryStartHandler, DeliveryTaskHandler
from telegram.view.update_views import UpdateHandler

app_name = 'telegram-api'
urlpatterns = [
	path('login/', LoginHandler.as_view(), name='login'),
	path('update/', UpdateHandler.as_view(), name='update'),
	path('deliveries/', DeliveryHandler.as_view(), name='deliveries'),
	path('deliveries/<int:delivery_id>', DeliveryTaskHandler.as_view()),
	path('deliveries/start', DeliveryStartHandler.as_view(), name='deliveries_start'),
	path('channels/', ChannelHandler.as_view(), name='channels'),
]
