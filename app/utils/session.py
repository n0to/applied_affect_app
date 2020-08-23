from mongoengine import DoesNotExist
import app.models.session as models_session
import app.schemas.session as schemas_session
from loguru import logger


def get_session(id: str):
    try:
        session = models_session.Session.objects.get(id=id)
        logger.debug("session from db: {}".format(session.to_mongo()))
        session_out = schemas_session.Session.from_orm(session)
    except DoesNotExist:
        return None
    return session_out


def create_session(session: schemas_session.SessionCreate):
    pass


def update_session(session: schemas_session.SessionUpdate):
    pass