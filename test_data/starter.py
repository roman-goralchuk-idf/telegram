import asyncio

from telegram.repository_mongo.mongo_message import MongoRepositoryMessages
from test_data.test_data_service import TestData


async def sprint():

    list_channel = [
        'seoHR_full.json',
        'Outsource_full.json',
        'seoHR_full.json',
        'work_in_gamedev_full.json',
        'digitalHR_full.json',
        'remoteIT_full.json',
        'getITWorld_full.json',
        'habr_full.json',
        'jobinIT_full.json',
        'telegramIT_full.json',
        'workinIT_full.json'
    ]
    for channel in list_channel:
        result = await MongoRepositoryMessages().saveAllDicts(await TestData.getFullData(channel))
        print(f'{channel} - {len(result.inserted_ids)}')

asyncio.run(sprint())
