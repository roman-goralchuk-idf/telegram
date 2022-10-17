import enum


class StatusChannel(enum.Enum):
	NEW = 'new'
	IN_WORK = 'in_work'
	DISABLE = 'disable'


class Channel:

	def __init__(self, channel_id):
		self.channel_id: int = channel_id
		self.name = None
		self.status = StatusChannel.NEW.value
		self.last_update = None
		self.message_count = None

	def toDict(self):
		return self.__dict__

	def fromDict(self, input_dict):
		for key in input_dict:
			setattr(self, key, input_dict[key])


class Dict2Class:

	def __init__(self, my_dict):
		for key in my_dict:
			setattr(self, key, my_dict[key])
