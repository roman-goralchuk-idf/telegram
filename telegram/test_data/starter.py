import asyncio

from telegram.repository_mongo.mongo import MongoRepositoryMessages
from telegram.test_data.test_data_service import TestData


async def sprint():

    await MongoRepositoryMessages().saveAll(await TestData.getFullData('remoteIT_full.json'))

asyncio.run(sprint())
