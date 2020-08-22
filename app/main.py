import logging
import sys
from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import get_settings, Settings
from app.custom_logging import InterceptHandler, format_record
from app.db.database import DbMgr
from app.routers import session, auth, student, teacher, pulse, school


def create_app() -> FastAPI:
    app = FastAPI(title='Applied Affect Backend', Debug=True)
    router = APIRouter()
    app.include_router(session.router)
    app.include_router(student.router)
    app.include_router(teacher.router)
    app.include_router(pulse.router)
    app.include_router(school.router)
    app.include_router(auth.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    configure_logger()
    return app


def configure_logger():
    settings = get_settings()
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": settings.logging_level, "format": format_record}]
    )


app = create_app()


@app.on_event("startup")
def start_svc():
    settings = get_settings()
    DbMgr.connect(settings.mongo_dbname,
                  settings.mongo_username,
                  settings.mongo_password,
                  settings.mongo_host)


@app.on_event("shutdown")
def shutdown_svc():
    DbMgr.disconnect()


@app.get("/info")
def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "logging_level": settings.logging_level,
        "algorithm": settings.algorithm,
        "mongodb_url": settings.mongo_host,
        "access_token_expire_minutes": settings.access_token_expire_seconds
    }