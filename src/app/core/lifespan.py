from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI
from psycopg.errors import CannotConnectNow
from sqlalchemy.exc import InterfaceError, OperationalError

from .database import asyncio_engine, init_db
from .logging import setup_logger

logger = setup_logger(__name__)

DB_STARTUP_TIMEOUT = 60
DB_RETRY_INTERVAL = 2
DB_CONNECT_ERRORS = (OSError, OperationalError, InterfaceError, CannotConnectNow)


async def init_db_with_retry() -> None:
    with anyio.move_on_after(DB_STARTUP_TIMEOUT) as scope:
        while True:
            try:
                await init_db()
                return
            except DB_CONNECT_ERRORS as exc:
                # Log the exception type only: its message can include the URL.
                logger.warning(
                    "Database not reachable yet (%s); retrying in %ss",
                    type(exc).__name__,
                    DB_RETRY_INTERVAL,
                )
                await anyio.sleep(DB_RETRY_INTERVAL)
    if scope.cancelled_caught:
        raise RuntimeError(
            f"Database not reachable after {DB_STARTUP_TIMEOUT}s; giving up"
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):

    try:
        logger.info("Initializing Application Startup")

        # Initialize database tables, waiting for a database that is still booting
        await init_db_with_retry()

        logger.info("Successfully Completed Application Startup")
        yield
    finally:
        # Dispose the engine on shutdown and on failed startup alike
        await asyncio_engine.dispose()
        logger.info("DB engine disposed.")

        logger.info("Application shutdown")
