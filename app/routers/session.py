from fastapi import APIRouter
from app.schemas.session import Session, SessionCreate
import app.crud.session as session_crud

router = APIRouter()


@router.get("/session/{id}", response_model=Session)
def get_session(id: str):
    s = session_crud.get_session(session_id=id)
    #return sess


@router.put("/session/{id}")
def update_session(id: str):
    pass


@router.post("/session")
def create_session(session: SessionCreate):
    pass


