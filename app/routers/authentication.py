from fastapi import APIRouter

router = APIRouter()


@router.get("/testing")
def read_main():
    return {"msg": "Hello World"}