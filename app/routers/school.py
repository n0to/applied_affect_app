from fastapi import APIRouter, HTTPException
from loguru import logger

from app.schemas.school import Camera
import app.utils.school as utils_school
router = APIRouter()


@router.get("/camera/{id}", response_model=Camera)
def get_camera(id: str):
    camera = utils_school.get_camera(id=id)
    if not camera:
        raise HTTPException(status_code=400, detail="No camera found")
    return camera


