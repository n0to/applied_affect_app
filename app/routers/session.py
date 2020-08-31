from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import PositiveInt

from app.models.enums import SessionState, Grade, Section, Subject
from app.schemas.session import Session, SessionCreate, SessionUpdate
import app.utils.session as utils_session

router = APIRouter()


@router.get("/session/{id}", response_model=Session)
def get_session(id: str):
    session = utils_session.get_session(id=id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("session/search", response_model=List[Session])
def get_sessions(state: Optional[SessionState] = None,
                 grade: Optional[Grade] = None,
                 section: Optional[Section] = None,
                 subject: Optional[Subject] = None,
                 scheduled_end_time: Optional[datetime] = None,
                 teacher: Optional[str] = None,
                 scheduled_start_time: Optional[datetime] = datetime.now(),
                 max_records: Optional[PositiveInt] = 3):
    sessions = utils_session.search_sessions(state=state,
                                             scheduled_start_time=scheduled_start_time,
                                             scheduled_end_time=scheduled_end_time,
                                             max_records=max_records,
                                             grade=grade,
                                             section=section,
                                             subject=subject,
                                             teacher=teacher)
    if not len(sessions):
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions


@router.put("/session/{id}")
def update_session(id: str, session: SessionUpdate):
    pass


@router.post("/session")
def create_session(session: SessionCreate):
    pass
