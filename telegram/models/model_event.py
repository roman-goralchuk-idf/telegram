import json

from telegram.models.model_customer import CustomerStatus


class EventParserMessage:

	def __init__(self, customer_status=None, ids_messages=None):
		self.status: CustomerStatus = customer_status
		self.objectIds: [str] = ids_messages

	def prepareToSend(self):
		return json.dumps(self.__dict__)

