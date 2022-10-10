import asyncio

from repository_mongo.mongo import MongoRepository
from test_data.test_data_service import TestData


async def sprint():

    await MongoRepository().saveAll(await TestData.getFullData('work_in_gamedev_full.json'), 'messages')

asyncio.run(sprint())
