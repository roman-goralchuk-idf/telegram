import asyncio
import enum
from datetime import datetime


class TaskDeliveryStatus(enum.Enum):
	def __init__(self, name_status):
		self.name_status = name_status
	DRAFT = 'draft'
	READY_FOR_DELIVERY = 'ready_for_delivery'
	COMPLETED = 'completed'


class TaskDelivery:
	def __init__(self, telegram_ids, message, description, delivery_scheduled):
		self.task_id: int = None
		self.status = TaskDeliveryStatus.DRAFT.name_status
		self.array_id: [str] = telegram_ids
		self.message: str = message
		self.description: str = description
		self._created_date: datetime = datetime.now()
		self.delivery_scheduled: datetime = delivery_scheduled
		self._performed_date: datetime = None

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])


class TasksRequest:
	def __init__(self, tasks_ids, status):
		self.task_ids: [int] = tasks_ids
		self.status = status

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])

