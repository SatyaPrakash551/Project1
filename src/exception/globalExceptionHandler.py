from sqlalchemy.exc import SQLAlchemyError
from fastapi import Request
from fastapi.responses import JSONResponse
from src.exception.resourceNotFound import ResourceNotFoundException
from src.core.logging.logger import get_logger

logger = get_logger(__name__)

def resource_not_found_exception_handler(request:Request,exc:ResourceNotFoundException):
    return JSONResponse(status_code=404,content={"error":"not Found","message":exc.message})

def sqlAlchemy_exception_handler(request : Request,exc : SQLAlchemyError ):
    return JSONResponse(status_code=500,content={"error":"database Error","message":str(exc)})

def unknown_exception_handler(request : Request , exc : Exception):
    logger.exception("unhandled_application_exception",path = request.url.path,method = request.method)
    return JSONResponse(status_code=500,content={"error":"internal server Error", "message":str(exc)})
