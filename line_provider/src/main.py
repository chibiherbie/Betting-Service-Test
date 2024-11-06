import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.send_all_events import send_all_events
from src.config import settings
from src.init import redis_manager
from src.api.events import router as router_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    await send_all_events(redis_manager)
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_events)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=settings.BACKEND_PORT_1, reload=True)
