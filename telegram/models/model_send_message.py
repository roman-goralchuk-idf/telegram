from datetime import datetime


class SendMessage:
	def __init__(self, telegram_id, message, delivery_scheduled):
		self.telegram_id = telegram_id
		self.message = message
		self.delivery_scheduled: datetime = delivery_scheduled

	def toDict(self):
		return self.__dict__
