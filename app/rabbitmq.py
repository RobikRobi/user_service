import json
import logging
import os
from typing import Any

import aio_pika


LOGGER = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
USERS_EXCHANGE = os.getenv("USERS_EXCHANGE", "users.events")
USER_CREATED_ROUTING_KEY = "user.created"


class RabbitPublisher:
    def __init__(self) -> None:
        self.connection: Any | None = None
        self.channel: Any | None = None
        self.exchange: Any | None = None

    async def connect(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                USERS_EXCHANGE,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
        except Exception:
            LOGGER.exception("Could not connect users_service to RabbitMQ")
            await self.close()

    async def publish_user_created(self, user: dict[str, Any]) -> None:
        if self.exchange is None:
            LOGGER.warning("RabbitMQ publisher is not connected; user.created was not published")
            return

        message = aio_pika.Message(
            body=json.dumps(user).encode("utf-8"),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        try:
            await self.exchange.publish(message, routing_key=USER_CREATED_ROUTING_KEY)
        except Exception:
            LOGGER.exception("Could not publish user.created for user_id=%s", user.get("id"))

    async def close(self) -> None:
        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()
