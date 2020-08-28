from mongoengine import DoesNotExist
from pydantic import PositiveInt
from bson.objectid import ObjectId
import app.models.session as models_session
import app.schemas.session as schemas_session
import app.models.school as models_school
from loguru import logger

from app.models.enums import Grade, Section, Subject


def get_session(id: str):
    logger.debug("Get session with id: {}".format(id))
    out_session = None
    try:
        session = models_session.Session.objects.get(id=id)
        out_session = schemas_session.Session.from_orm(session)
    except DoesNotExist:
        logger.info("No session exists with id: {}".format(id))
    return out_session


def search_sessions(max_records: PositiveInt, **kwargs):
    filters = {}
    filters_klass = {}
    for k, v in kwargs.items():
        if v is not None:
            if k == "scheduled_start_time":
                filters["scheduled_start_time"] = {"$gte": v}
            elif k == "scheduled_end_time":
                filters["scheduled_end_time"] = {"$lte": v}
            elif k == "teacher":
                filters["teacher"] = ObjectId(v)
            elif k == "grade" or k == "section":
                filters_klass[k] = Grade(v)
            elif k == "section":
                filters_klass[k] = Section(v)
            elif k == "subject":
                filters_klass[k] = Subject(v)
            else:
                filters[k] = v
    logger.debug("Max Records: {}".format(max_records))
    logger.bind(payload=filters).debug("session search filters:")
    for k, v in filters.items():
        logger.debug("{} -> {}".format(k, v))
    logger.bind(payload=filters).debug("klass search filters:")
    for k, v in filters_klass.items():
        logger.debug("{} -> {}".format(k, v))
    out_sessions = []
    try:
        # Get the klasses if the grade and section filters are populated
        #if "grade" in filters_klass or "section" in filters_klass:
        #    klasses = models_school.Klass.objects(filters_klass)
        # Get the sessions based on all the filters
        sessions = models_session.Session.objects(__raw__=filters).order_by('+scheduled_start_time').limit(max_records)
        for session in sessions:
            out = schemas_session.Session.from_orm(session)
            logger
            out_sessions.append(out)
    except DoesNotExist:
        logger.info("No sessions exist for given criteria")
    return out_sessions


def create_session(session: schemas_session.SessionCreate):
    pass


def update_session(session: schemas_session.SessionUpdate):
    pass
