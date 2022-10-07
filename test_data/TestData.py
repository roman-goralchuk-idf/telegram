import asyncio
import json


async def getDataForTest(fileUrl) -> []:
	with open(fileUrl, 'r') as f:
		data = json.load(f)
		return data


async def getOutsourceForTest() -> []:
	with open('Outsource_full.json', 'r') as f:
		coll = []
		data = json.load(f)
		for i in data:
			coll.append(i)
		return coll
