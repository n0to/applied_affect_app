from datetime import datetime
from typing import Optional

from mongoengine import DoesNotExist
from loguru import logger
import app.models.session as models_session
import app.models.teacher as models_teacher
import app.schemas.session as schemas_session
import app.schemas.teacher as schemas_teacher


def get_teacher(id: str):
    logger.debug("Get teacher with id:{}".format(id))
    out_teacher = None
    try:
        teacher = models_teacher.Teacher.objects.get(id=id)
        out_teacher = schemas_teacher.Teacher.from_orm(teacher)
    except DoesNotExist:
        logger.info("No teacher exists with id: {}".format(id))
    return out_teacher
