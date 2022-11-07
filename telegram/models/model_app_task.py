import asyncio
import enum
from datetime import datetime

from telegram.service.time_service import TimeService


class TaskDeliveryStatus(enum.Enum):
	def __init__(self, name_status):
		self.name_status = name_status

	DRAFT = 'draft'
	READY_FOR_DELIVERY = 'ready_for_delivery'
	PENDING = 'pending'
	IN_PROGRESS = 'in_progress'
	COMPLETED = 'completed'
	PARTLY_COMPLETED = 'partly_completed'
	ERROR = 'error'


class TaskDelivery:
	def __init__(
			self,
			task_id=None,
			status=TaskDeliveryStatus.DRAFT.name_status,
			telegram_ids=None,
			message=None,
			description=None,
			created_date=datetime.now(tz=TimeService().getTimeZone()),
			delivery_scheduled=None,
			performed_date=None
	):
		self.task_id: int = task_id
		self.status = status
		self.telegram_ids: [str] = telegram_ids
		self.message: str = message
		self.description: str = description
		self.created_date: datetime = created_date
		self.delivery_scheduled: datetime = delivery_scheduled
		self.performed_date: datetime = performed_date

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])


class TasksSearchRequest:
	def __init__(self, tasks_ids=None, status=TaskDeliveryStatus.DRAFT.name_status):
		self.task_ids: [int] = tasks_ids
		self.status: str = status

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])
