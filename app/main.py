from fastapi import APIRouter, FastAPI, Depends
from fastapi.logger import logger
from app.db.database import DbMgr
from app.routers import session, authentication, student, teacher, pulse, school
from app.config import get_settings, Settings


app = FastAPI()
router = APIRouter()
app.include_router(session.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(pulse.router)
app.include_router(school.router)
app.include_router(authentication.router)


@app.on_event("startup")
def start_svc():
    settings = get_settings()
    logger.setLevel(settings.logging_level)
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
        "logging_level": settings.logging_level
    }


logger.info('****************** Starting Applied Affect App Backend Server *****************')
