import json
import logging
from typing import Any

import aio_pika
from aio_pika import Channel, Connection

from src.config import settings

logger = logging.getLogger(__name__)

_connection: Connection | None = None
_channel: Channel | None = None


async def get_connection() -> Connection:
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    return _connection


async def get_channel() -> Channel:
    global _channel
    connection = await get_connection()
    if _channel is None or _channel.is_closed:
        _channel = await connection.channel()
        await _channel.set_qos(prefetch_count=10)
    return _channel


async def publish(exchange_name: str, routing_key: str, payload: dict[str, Any]) -> None:
    channel = await get_channel()
    exchange = await channel.declare_exchange(
        exchange_name,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )
    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        content_type="application/json",
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )
    await exchange.publish(message, routing_key=routing_key)
    logger.info("Published event %s to %s", routing_key, exchange_name)


async def close_rabbitmq() -> None:
    global _connection, _channel
    if _channel and not _channel.is_closed:
        await _channel.close()
        _channel = None
    if _connection and not _connection.is_closed:
        await _connection.close()
        _connection = None
