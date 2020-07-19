from fastapi import APIRouter, FastAPI
from .database import DbMgr
from .routers import session, authentication

app = FastAPI()
router = APIRouter()
app.include_router(session.router)
app.include_router(authentication.router)


@app.on_event("startup")
def create_db_client():
    DbMgr.connect()


@app.on_event("shutdown")
def shutdown_db_client():
    DbMgr.disconnect()


