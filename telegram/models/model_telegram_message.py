class TelegramMessageUpdateResult:

	def __init__(self, channel_id=None, count_messages=0, acknowledged=False, last_id=None):
		self.channel_id: str = channel_id
		self.count_messages: int = count_messages
		self.update_result: bool = acknowledged
		self.last_id: int = last_id

	def toDict(self):
		return self.__dict__
