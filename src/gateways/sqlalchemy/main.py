from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import app_config

engine = create_async_engine(str(app_config.pg_dsn))

session_factory = async_sessionmaker(engine, expire_on_commit=False)
