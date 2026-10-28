import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import books

logger = logging.getLogger(__name__)

app = FastAPI(title="Book Management System")
app.include_router(books.router)


@app.exception_handler(psycopg.OperationalError)
async def db_connection_error(request: Request, exc: psycopg.OperationalError):
    logger.error("Database connection error", exc_info=exc)
    return JSONResponse(status_code=503, content={"detail": "Service temporarily unavailable"})


@app.exception_handler(psycopg.Error)
async def db_error(request: Request, exc: psycopg.Error):
    logger.error("Database error", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})