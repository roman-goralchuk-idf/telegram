import asyncio

from telegram.repository_mongo.mongo_message import MongoRepositoryMessages
from test_data.test_data_service import TestData


# Before action need unpack archives from 'test_data/full/archive' in 'test_data/full'
async def sprint():
	list_channel = [
		'seoHR_full.json'
	]
	for channel in list_channel:
		result = await MongoRepositoryMessages().saveAllDicts(await TestData.getFullData(channel))
		print(f'{channel} - {len(result.inserted_ids)}')


asyncio.run(sprint())
