import json
from os.path import join

from test_data.apps import TEST_DATA_FULL


class TestData:

	@staticmethod
	async def getFullData(fileUrl) -> []:
		with open(join(TEST_DATA_FULL, fileUrl), 'r') as f:
			coll = []
			data = json.load(f)
			for i in data:
				coll.append(i)
			return coll
