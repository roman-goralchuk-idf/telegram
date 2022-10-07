from . import TelegramChannelsService
from .TelegramConnectorService import Client


# api_id = configBase['telegram']['api_id']
# api_hash = configBase['telegram']['api_hash']
# phone = configBase['telegram']['phone']
# name = configBase['telegram']['name_connection']
# password = configBase['telegram']['password']
#
# client = TelegramClient(name, api_id, api_hash)


async def checkConnection():
	return await Client().checkConnection()


async def sendCode(code):
	return await Client().sendCode(code)


async def getAllMessage(channels):
	return await TelegramChannelsService.getChannelShortMessages('t.me/Remoteit', client, 1)


# async def main():
# 	print(await TelegramConnectorService.checkConnection(client, phone))
#
# 	auth = await client.is_user_authorized()
# 	if not auth:
# 		await client.send_code_request(phone)
# 		try:
# 			await client.sign_in(phone, input('Enter the code: '))
# 		except SessionPasswordNeededError:
# 			await client.sign_in(password=input('Password: '))
# 	else:
# 		print('auth OK')
#
# 	await TelegramChannelsService.getChannelInfo('t.me/BoardOutsource', client)
# 	# mess = await Channels.getChannelJSONMessages('t.me/BoardOutsource', client, 1)
# 	# print(mess)
# 	# print("\n")
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/BoardOutsource', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/gamedevjob', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/gamedevjob', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/Remoteit', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/Remoteit', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/itlenta', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/itlenta', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/seohr', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/seohr', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/digital_hr', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/digital_hr', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/geekjobs', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/geekjobs', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/myjobit', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/myjobit', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/Getitrussia', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/Getitrussia', client, 1)
# 	print(messSmall)
# 	print("\n")
#
# 	await TelegramChannelsService.getChannelInfo('t.me/habr_career', client)
# 	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/habr_career', client, 1)
# 	print(messSmall)
# 	print("\n")
#
#
# with client:
# 	client.loop.run_until_complete(main())
