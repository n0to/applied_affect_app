from fastapi import APIRouter, HTTPException
from loguru import logger
from app.schemas.session import Session, SessionCreate, SessionUpdate
import app.utils.session as session_utils

router = APIRouter()


@router.get("/session/{id}", response_model=Session)
def get_session(id: str):
    session = session_utils.get_session(id=id)
    if not Session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/session/{id}")
def update_session(id: str, session: SessionUpdate):
    pass


@router.post("/session")
def create_session(session: SessionCreate):
    pass


