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


# Todo: Implement search by grade and section
def search_sessions(max_records: PositiveInt, **kwargs):
    filters = {}
    filters_klass = {}
    for k, v in kwargs.items():
        if v is not None:
            if k == "scheduled_start_time":
                filters[k] = {"$gte": v}
            elif k == "scheduled_end_time":
                filters[k] = {"$lte": v}
            elif k == "teacher":
                filters[k] = ObjectId(v)
            elif k == "grade":
                filters_klass[k] = Grade(v)
            elif k == "section" and "grade" in kwargs and kwargs["grade"] is not None:
                filters_klass[k] = Section(v)
            elif k == "subject":
                filters_klass[k] = Subject(v)
            else:
                filters[k] = v
    logger.debug("Max Records: {}".format(max_records))
    logger.bind(payload=filters).debug("session search filters:")
    logger.bind(payload=filters_klass).debug("klass search filters:")
    out_sessions = []
    try:
        # Get the klasses if the grade and section filters are populated
        # if "grade" in filters_klass or "section" in filters_klass:
        #    klasses = models_school.Klass.objects(filters_klass)
        # Get the sessions based on all the filters
        sessions = models_session.Session.objects(__raw__=filters).order_by('+scheduled_start_time').limit(max_records)
        for session in sessions:
            logger.debug("iterating")
            out = schemas_session.Session.from_orm(session)
            out_sessions.append(out)
        logger.debug("Found {} number of sessions matching criteria".format(len(out_sessions)))
    except DoesNotExist:
        logger.info("No sessions exist for given criteria")
    return out_sessions


# Todo: Implement
def create_session(session: schemas_session.SessionCreate):
    pass


# Todo: Implement
def update_session(id: str, session_update: schemas_session.SessionUpdate):
    pass


# Todo: Change to atomic update
def update_session_configuration(id: str, session_configuration: schemas_session.SessionConfiguration):
    logger.bind(payload=session_configuration.dict()).debug("Updating session {} with configuration".format(id))
    num_updated = 0
    try:
        session = models_session.Session.objects.get(id=id)
        session.configs.append(models_session.SessionConfiguration(**session_configuration.dict()))
        session.save()
        num_updated = num_updated + 1
    except DoesNotExist:
        logger.info("No session exists with id: {}".format(id))
    return num_updated


# Todo: Change to atomic update
def update_session_scenario(id: str, session_scenario: schemas_session.SessionScenario):
    logger.bind(payload=session_scenario.dict()).debug("Updating session {} with scenario".format(id))
    num_updated = 0
    try:
        session = models_session.Session.objects.get(id=id)
        session.scenarios.append(models_session.SessionScenario(**session_scenario.dict()))
        session.save()
        num_updated = num_updated + 1
    except DoesNotExist:
        logger.info("No session exists with id: {}".format(id))
    return num_updated
