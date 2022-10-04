import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):

	def default(self, o):
		if isinstance(o, datetime):
			return o.isoformat()

		if isinstance(o, bytes):
			return list(o)

		return json.JSONEncoder.default(self, o)