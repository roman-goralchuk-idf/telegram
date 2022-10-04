import json
import re

from DateEncoder import DateTimeEncoder


async def getChannelInfo(name, client):
	chOutsource = await client.get_entity(name)
	mess = await client.get_messages(name)
	print(f"Total messages by {chOutsource.title}: {str(mess.total)}")


async def getChannelJSONMessages(name, client, count):
	all_mess = []
	mess = await client.get_messages(name, count)
	for x in mess:
		all_mess.append(x.to_dict())
	return json.dumps(all_mess, cls=DateTimeEncoder, ensure_ascii=False)


async def getChannelShortMessages(name, client, count):
	all_mess = []
	mess = await client.get_messages(name, count)
	for x in mess:
		url = ""
		for y in x.entities:
			if re.search("MessageEntityTextUrl", str(y)):
				url = y.url
		all_mess.append(
			{
				"id": x.id,
				"channel_id": x.peer_id.channel_id,
				"date": x.date,
				"message": x.message,
				"url": url,
				"via_bot_id": x.via_bot_id
			}
		)
	return json.dumps(all_mess, cls=DateTimeEncoder, ensure_ascii=False)
