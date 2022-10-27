import json

from telegram.models.model_customer import CustomerStatus


class EventParserMessage:

	def __init__(self, ids_messages=None, customer_status=None):
		self.ids_messages: [str] = ids_messages
		self.customer_status: CustomerStatus = customer_status

	def prepareToSend(self):
		return json.dumps(self.__dict__)

