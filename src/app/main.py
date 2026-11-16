from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api.router import router
from .core.config import get_settings
from .core.exceptions import AppError
from .core.logging import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Initializing Application Startup")
    logger.info("Successfully Completed Application Startup")

    yield
    logger.info("Application shutdown")


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.include_router(router)


# Error handlers
@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError):
    """Generic Exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
):
    """Custom RequestValidationError handler"""
    errors = []

    for error in exc.errors():
        location = error["loc"]
        errors.append(
            {
                "source": str(location[0]),
                "field": ".".join(map(str, location[1:])),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    logger.warning("Request validation failed: %s", errors)

    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": "Request validation failed. ",
            "errors": errors,
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, _exc: Exception):
    """Exception handler for unexpected errors"""
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
