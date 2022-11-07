from django.urls import path

from celery_django.views import CeleryStatusHandler

app_name = 'celery-api'
urlpatterns = [
	path('status/<str:task_id>', CeleryStatusHandler.as_view(), name='status')
]
