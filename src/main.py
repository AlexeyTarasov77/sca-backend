import asyncio
from fastapi import FastAPI
import uvicorn

from core.config import app_config

app = FastAPI()


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
