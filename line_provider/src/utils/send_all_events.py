from src.api.events import events
from src.connectors.redis_connector import RedisManager


async def send_all_events(redis_manager: RedisManager):
    for event in events.values():
        await redis_manager.publish_event_update(event)
