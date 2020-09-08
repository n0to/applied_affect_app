from mongoengine import DoesNotExist
from loguru import logger
import app.models.school as models_school
import app.schemas.school as schemas_school


def get_camera(id: str):
    out_camera = None
    try:
        camera = models_school.Camera.objects.get(id=id)
        out_camera = schemas_school.Camera.from_orm(camera)
    except DoesNotExist:
        logger.info("No camera exists with id: {}".format(id))
    return out_camera


def get_school(id: str):
    pass


def get_klass(id: str):
    out_klass = None
    try:
        klass = models_school.Klass.objects.get(id=id)
        out_klass = schemas_school.Klass.from_orm(klass)
    except DoesNotExist:
        logger.info("No klass exists with id: {}".format(id))
    return out_klass

