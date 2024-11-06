import json

import redis.asyncio as redis

from src.shemas.events import Event


class RedisManager:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.redis: redis.Redis | None = None

    async def connect(self) -> None:
        try:
            self.redis = await redis.Redis(host=self.host, port=self.port)
        except Exception as e:
            print(e)

    async def publish_event_update(self, event: Event) -> None:
        await self.redis.rpush("events_channel", event.model_dump_json())

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()
