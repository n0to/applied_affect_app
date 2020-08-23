from fastapi import APIRouter
from loguru import logger

from app.schemas.school import Camera
import app.utils.school as utils_school
router = APIRouter()


@router.get("/camera/{id}", response_model=Camera)
def get_camera(id: str):
    return utils_school.get_camera(id)
