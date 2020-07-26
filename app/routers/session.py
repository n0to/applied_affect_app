from fastapi import APIRouter
from app.schemas.session import Session, SessionCreate

router = APIRouter()


@router.get("/session/{id}", response_model=Session)
def get_session(id: str):
    pass


@router.put("/session/{id}")
def update_session(id: str):
    pass


@router.post("/session")
def create_session(session: SessionCreate):
    pass


