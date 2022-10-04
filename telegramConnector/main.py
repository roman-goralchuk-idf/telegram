import json
from datetime import datetime

from django.utils.formats import date_format
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest

import TelegramChannelsService

api_id = 19358343
api_hash = '691546d6af65c083cbadb4fa55889382'

# 💬 Origin chat
#  ├ id: -1001391347473
#  ├ title: [board] Outsource
#  ├ username: BoardOutsource (https://t.me/BoardOutsource)
#  └ type: channel

# 💬 Origin chat
#  ├ id: -1001109222536
#  ├ title: Работа в геймдеве 🍖
#  ├ username: gamedevjob (https://t.me/gamedevjob)
#  └ type: channel

# 💬 Origin chat
#  ├ id: -1001141029953
#  ├ title: Remote IT (Inflow)
#  ├ username: Remoteit (https://t.me/Remoteit)
#  └ type: channel

# 💬 Origin chat
# Работа в IT, вакансии
# t.me/itlenta

# 💬 Origin chat
# SEO HR, digital-вакансии, офис и удалёнка
# https://t.me/seohr

# 💬 Origin chat
# DigitalHR
# https://t.me/digital_hr

# 💬 Origin chat
# Job in IT&Digital
# https://t.me/geekjobs

# 💬 Origin chat
# Telegram IT Job
# https://t.me/myjobit

# 💬 Origin chat
# GetIT World!
# https://t.me/Getitrussia

# 💬 Origin chat
# Хабр Карьера
# https://t.me/habr_career

client = TelegramClient('session_name', api_id, api_hash)


async def main():
	# me = await client.get_me()
	# print(me.stringify())
	# await client.send_message('me', 'Hello, myself!')
	#
	# # await client.download_profile_photo('me')
	# dialogs = await client.get_dialogs()
	# print("Total dialogs: " + me.first_name + " " + str(dialogs.total) + "\n")
	# for x in dialogs:
	# 	print(x.name)
	# print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/BoardOutsource', client)
	# mess = await Channels.getChannelJSONMessages('t.me/BoardOutsource', client, 1)
	# print(mess)
	# print("\n")
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/BoardOutsource', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/gamedevjob', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/gamedevjob', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/Remoteit', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/Remoteit', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/itlenta', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/itlenta', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/seohr', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/seohr', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/digital_hr', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/digital_hr', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/geekjobs', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/geekjobs', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/myjobit', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/myjobit', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/Getitrussia', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/Getitrussia', client, 1)
	print(messSmall)
	print("\n")

	await TelegramChannelsService.getChannelInfo('t.me/habr_career', client)
	messSmall = await TelegramChannelsService.getChannelShortMessages('t.me/habr_career', client, 1)
	print(messSmall)
	print("\n")


with client:
	client.loop.run_until_complete(main())
