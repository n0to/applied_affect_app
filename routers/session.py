from fastapi import APIRouter

router = APIRouter()


@router.get("/session/{session_id")
def get_session():
    print("Reached")
    pass


@router.put("/session/{session_id}")
def update_session():
    pass
