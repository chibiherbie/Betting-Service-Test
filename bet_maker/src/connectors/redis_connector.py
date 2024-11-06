import json
import time

import redis.asyncio as redis

from src.api.bets import events_cache
from src.shemas.events import Event
from src.utils.update_bets import update_bets


class RedisManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        try:
            self.redis = await redis.Redis(host=self.host, port=self.port)
        except Exception as e:
            pass

    async def listen_for_event_updates(self) -> None:
        while True:
            message = await self.redis.blpop("events_channel")

            if message:
                event_data = json.loads(message[1].decode("utf-8"))
                event = Event(**event_data)

                if event.deadline > time.time():
                    events_cache[event.event_id] = event
                elif event.event_id in events_cache:
                    del events_cache[event.event_id]

                await update_bets(event.event_id, event.state)

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()
