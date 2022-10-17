import json
import logging
from os.path import join

from telegram.apps import TEST_DATA_FULL

_logger = logging.getLogger('custom')


class TestData:

	@staticmethod
	async def getFullData(fileUrl) -> []:
		try:
			with open(join(TEST_DATA_FULL, fileUrl), 'r') as f:
				data = json.load(f)
				array = []
				for i in data:
					array.append(i)
				print(f'Found {len(array)} elements from file {fileUrl}')
				return array
		except FileNotFoundError as e:
			print(e)
			_logger.error(e)
