from typing import Optional

from bson import ObjectId
from loguru import logger
from mongoengine import DoesNotExist
from pydantic import PositiveInt
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
from app.models.enums import Grade, Section, Subject


def get_assignment(id: str, get_qnas: bool=False):
    out_ass = None
    logger.debug("Get assignment with id {}".format(id))
    try:
        ass = models_grading.Assignment.objects.get(id=id)
        out_ass = schemas_grading.Assignment.from_orm(ass)
        if get_qnas:
            aqnas = models_grading.AssignmentQnA.objects(assignment=id)
            for aqna in aqnas:
                #Todo: Filter QnA content in aqna.qna w.r.t. requisite version in aqna.qna_version
                out_ass.qnas.append(schemas_grading.AssignmentQnA.from_orm(aqna))
    except DoesNotExist:
        logger.info("No assignment exists with id: {}".format(id))
    logger.debug("Returning output now", out_ass)
    return out_ass


def search_assignments(max_records: PositiveInt, **kwargs):
    out_asses = []
    filters = {}
    filters_klass = {}
    for k, v in kwargs.items():
        if k == "deadline":
            filters[k] = {"$gte": v}
        elif k == "teacher":
            filters["created_by"] = ObjectId(v)
        elif k == "grade":
            filters_klass[k] = Grade(v)
        elif k == "section" and "grade" in kwargs:
            filters_klass[k] = Section(v)
        elif k == "subject":
            filters[k] = Subject(v)
        else:
            filters[k] = v
    logger.bind(payload=filters).debug("Searching assignments with filters:")
    try:
        asses = models_grading.Assignment.objects(__raw__=filters).orderBy('+deadline').limit(max_records)
        for ass in asses:
            out_ass = schemas_grading.Assignment.from_orm(ass)
            out_asses.append(out_ass)
    except DoesNotExist:
        logger.info("No assignments exists for given criteria")
    return out_asses


def get_assignment_qna(get_top_answers: bool, id: Optional[str] = None, assignment: Optional[str] = None):
    out_ass_qna = []
    logger.debug("")
    try:
        pass
    except DoesNotExist:
        logger.info("No assignment qna exists with given criteria")
    return out_ass_qna
