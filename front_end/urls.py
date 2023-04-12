from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
	path('', views.index),
	path('deliveries', views.page_deliveries, name='deliveries'),
	path('deliveries/<int:delivery_id>', views.page_delivery_id),
	path('deliveries/new', views.page_delivery_new, name='new_deliveries'),
]
