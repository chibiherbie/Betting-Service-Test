import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI


sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings
from src.init import redis_manager
from src.api.bets import router as router_bets


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    asyncio.create_task(redis_manager.listen_for_event_updates())
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_bets)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=settings.BACKEND_PORT_2, reload=True)
