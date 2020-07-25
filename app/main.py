from fastapi import APIRouter, FastAPI
from fastapi.logger import logger
import logging
from app.db.database import DbMgr
from app.routers import session, authentication, student, teacher

app = FastAPI()
router = APIRouter()
app.include_router(session.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(authentication.router)
logger.setLevel(logging.DEBUG)


@app.on_event("startup")
def create_db_client():
    DbMgr.connect()


@app.on_event("shutdown")
def shutdown_db_client():
    DbMgr.disconnect()


logger.info('****************** Starting Applied Affect App Backend Server *****************')
