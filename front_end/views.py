import logging

from django import forms
from django.shortcuts import render

_logger = logging.getLogger('custom')


class UserForm(forms.Form):
	name = forms.CharField()
	age = forms.IntegerField()


def index(request):
	user_form = UserForm()
	data = {"first_name": "Adrian", "last_name": "Paul", "form": user_form}
	return render(request, "index.html", data)


def error_404_page_not_found_view(request, exception):
	return render(request, "404.html")


def error_500_error_view(request):
	return render(request, "500.html")


def error_400_bad_request_view(request, exception):
	return render(request, "400.html")


def error_403_permission_denied_view(request, exception):
	return render(request, "403.html")
