import asyncio
from urllib.parse import quote_plus

import pymongo

from test_data.TestData import getOutsourceForTest
from configuration.configurationloader import configDatabase

pymongo.version = '3.12.0'
username = configDatabase['database']['mongo']['user']
password = configDatabase['database']['mongo']['password']
host = configDatabase['database']['mongo']['host']
port = configDatabase['database']['mongo']['port']
database = configDatabase['database']['mongo']['database']
uri = "mongodb://%s:%s@%s:%s" % (quote_plus(username), quote_plus(password), host, port)
print(uri)

clientMongoDb = pymongo.MongoClient(uri)

try:
	print(clientMongoDb.server_info())
except Exception as e:
	print(e)


class MongoRepository:
	database = clientMongoDb["parser_telegram"]


async def sprint():
	collectionMessage = MongoRepository().database["messages"]

	data = await getOutsourceForTest()

	collectionMessage.insert_many(data)


# f = collectionMessage.find({}, {'id': 1})
# u = collectionMessage.find_one({'id': 500})
# print(str(u) + '\n')
#
# f = collectionMessage\
# 	.find({}, {'_id': 0, 'id': 1, 'peer_id': 1, 'channel_id': 2, 'date': 1, 'message': 1})\
# 	.limit(100)
# for g in f:
# 	print(g)


asyncio.run(sprint())
