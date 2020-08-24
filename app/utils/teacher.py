from mongoengine import DoesNotExist
from loguru import logger
import app.models.session as models_session
import app.models.teacher as models_teacher
import app.schemas.session as schemas_session
import app.schemas.teacher as schemas_teacher


def get_teacher_sessions(id: str):
    logger.debug("Getting sessions for teacher with id: {}".format(id))
    out_sessions = []
    try:
        sessions = models_session.Session.objects(teacher=id).order_by('+scheduled_start_time').limit(3)
        for session in sessions:
            out = schemas_session.Session.from_orm(session)
            out_sessions.append(out)
    except DoesNotExist:
        logger.info("No sessions exist for teacher with id: {}".format(id))
    return out_sessions


def get_teacher(id: str):
    logger.debug("Get teacher with id:{}".format(id))
    out_teacher = None
    try:
        teacher = models_teacher.Teacher.objects.get(id=id)
        out_teacher = schemas_teacher.Teacher.from_orm(teacher)
    except DoesNotExist:
        logger.info("No teacher exists with id: {}".format(id))
    return out_teacher
