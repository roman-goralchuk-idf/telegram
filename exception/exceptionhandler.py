from django.views.debug import ExceptionReporter


class CustomExceptionReporter(ExceptionReporter):

	def technical_500_response(self, exc_value, tb, status_code=500):
		return "dsfdsfdsfdsfds"
