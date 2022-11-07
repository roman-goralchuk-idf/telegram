"""telegram_parser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('telegram-api/', include('telegram.urls', namespace='telegram-api')),
    path('celery-api/', include('celery_django.urls', namespace='celery-api')),
    path('', include('front_end.urls', namespace='front')),
]

handler404 = 'front_end.views.error_404_page_not_found_view'
handler500 = 'front_end.views.error_500_error_view'
handler403 = 'front_end.views.error_403_permission_denied_view'
handler400 = 'front_end.views.error_400_bad_request_view'
