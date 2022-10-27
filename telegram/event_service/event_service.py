import logging
from abc import ABC

import pika

from configuration.configurationloader import configService
from telegram.models.model_event import EventParserMessage

_logger = logging.getLogger('custom')


# https://www.rabbitmq.com/tutorials/tutorial-one-python.html


class EventService(ABC):

	def __init__(self):
		self._exchange = configService['rabbitmq']['exchange']
		self._queue = configService['rabbitmq']['queue']

	@staticmethod
	def _getRabbitMqConfig() -> str:
		username = configService['rabbitmq']['user']
		password = configService['rabbitmq']['password']
		host = configService['rabbitmq']['host']
		port = configService['rabbitmq']['portApp']
		return f'amqp://{username}:{password}@{host}:{port}'


class EventParserMessageService(EventService):

	def __init__(self):
		super().__init__()
		self._routing_key = configService['rabbitmq']['parserMessageRoutingKey']

	async def emit(self, event: EventParserMessage):
		eventToSend = event.prepareToSend()
		connection = pika.BlockingConnection(pika.URLParameters(self._getRabbitMqConfig()))
		channel = connection.channel()
		channel.exchange_declare(exchange=self._exchange, exchange_type='direct')
		channel.queue_declare(queue=self._queue, exclusive=False)
		channel.queue_bind(exchange=self._exchange, queue=self._queue, routing_key=self._routing_key)
		channel.basic_publish(
			exchange=self._exchange,
			routing_key=self._routing_key,
			body=eventToSend
		)
		_logger.debug(f'Message sent: {eventToSend}')
		connection.close()
