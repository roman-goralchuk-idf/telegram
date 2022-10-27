import enum


class ChannelStatus(enum.Enum):
	NEW = 'new'
	IN_WORK = 'in_work'
	DISABLE = 'disable'


class Channel:

	def __init__(self, channel_id):
		self.channel_id: int = channel_id
		self.status = ChannelStatus.NEW.value
		self.message_total_count = None
		self.last_update_message_date = None
		self.last_update_message_id: int = 0

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])

