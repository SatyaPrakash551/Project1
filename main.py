from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from src.exception.resourceNotFound import ResourceNotFoundException
from src.exception.globalExceptionHandler import resource_not_found_exception_handler, sqlAlchemy_exception_handler,unknown_exception_handler
from src.route.userRoute import router as UserRouter
from contextlib import asynccontextmanager
from src.redis_client import redis_client
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging.config import configure_logging
from src.core.logging.middleware import (request_logging_middleware)
from src.core.logging import get_logger

configure_logging()

logger = get_logger()

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("application_starting")
    await redis_client.ping()
    print("redis connected")

    yield

    logger.info("application_shutting_down")
    await redis_client.aclose()
    print("redis connection closed")

app = FastAPI(lifespan=lifespan)

app.middleware("http")(request_logging_middleware)
   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
app.add_exception_handler(SQLAlchemyError,sqlAlchemy_exception_handler)
app.add_exception_handler(Exception,unknown_exception_handler)
app.include_router(UserRouter)

