from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
]

handler404 = 'front_end.views.error_404_page_not_found_view'
handler500 = 'front_end.views.error_500_error_view'
handler403 = 'front_end.views.error_403_permission_denied_view'
handler400 = 'front_end.views.error_400_bad_request_view'
