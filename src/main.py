import asyncio
from fastapi import FastAPI
import uvicorn
from api.v1.router import v1_router

from core.config import app_config

app = FastAPI()
app.include_router(v1_router)


async def main():
    server_cfg = uvicorn.Config(
        "main:app", port=app_config.server.port, log_level="info"
    )
    server = uvicorn.Server(server_cfg)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
