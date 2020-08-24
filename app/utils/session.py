from mongoengine import DoesNotExist
import app.models.session as models_session
import app.schemas.session as schemas_session
from loguru import logger


def get_session(id: str):
    logger.debug("Get session with id: {}".format(id))
    out_session = None
    try:
        session = models_session.Session.objects.get(id=id)
        out_session = schemas_session.Session.from_orm(session)
    except DoesNotExist:
        logger.info("No session exists with id: {}".format(id))
    return out_session


def create_session(session: schemas_session.SessionCreate):
    pass


def update_session(session: schemas_session.SessionUpdate):
    pass