from django.urls import path

from .views import TelegramRegistration, Mongo

urlpatterns = [
	path('registration/', TelegramRegistration.as_view()),
	path('update/', Mongo.as_view()),
]
