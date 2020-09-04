from typing import Optional, List, Any

from bson import ObjectId
from loguru import logger
from mongoengine import DoesNotExist, DynamicField
from pydantic import PositiveInt
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
import app.models.school as models_school
from app.models.enums import Grade, Section, Subject, AssignmentState


def get_assignment(id: str, get_qnas: bool = False):
    out_ass = None
    logger.debug("Get assignment with id {}".format(id))
    try:
        ass = models_grading.Assignment.objects.get(id=id)
        out_ass = schemas_grading.Assignment.from_orm(ass)
        if get_qnas:
            aqnas = models_grading.AssignmentQnA.objects(assignment=id)
            for aqna in aqnas:
                # Todo: Filter QnA content in aqna.qna w.r.t. requisite version in aqna.qna_version
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
        if v is not None:
            if k == "deadline":
                filters[k] = {"$gte": v}
            elif k == "teacher":
                filters[k] = ObjectId(v)
            elif k == "grade":
                filters_klass[k] = Grade(v)
            elif k == "section" and "grade" in kwargs and kwargs["grade"] is not None:
                filters_klass[k] = Section(v)
            elif k == "subject":
                filters[k] = Subject(v)
            elif k == "state":
                filters[k] = AssignmentState(v)

    try:
        if len(filters_klass.keys()) > 0:
            klass_ids = []
            logger.bind(payload=filters_klass).debug("Searching klasses with filters:")
            klass_itr = models_school.Klass.objects(__raw__=filters_klass).only('id')
            for klass in klass_itr:
                klass_ids.append(klass.id)
            if len(klass_ids) > 0:
                filters["klass"] = {"$in": klass_ids}
            else:
                raise DoesNotExist()
        logger.bind(payload=filters).debug("Searching assignments with filters:")
        asses = models_grading.Assignment.objects(__raw__=filters).order_by('+deadline').limit(max_records)
        for ass in asses:
            out_ass = schemas_grading.Assignment.from_orm(ass)
            out_asses.append(out_ass)
    except DoesNotExist:
        logger.info("No assignments exists for given criteria")
    return out_asses


# Todo: Implement
def get_assignment_qna(get_top_answers: bool, id: Optional[str] = None, assignment: Optional[str] = None):
    out_ass_qna = []
    logger.debug("")
    try:
        pass
    except DoesNotExist:
        logger.info("No assignment qna exists with given criteria")
    return out_ass_qna


# Todo: Implement
def post_qna_submission(aqna_id: str, s_id: str, answer: schemas_grading.AnsContent):
    num_updated = models_grading.AssignmentQnASubmission.objects(student=s_id, aqna=aqna_id)


# Todo: Implement
def update_assignment_qna_facts(id: str, facts: List[Any]):
    pass


# Todo: Implement
def update_assignment_qna_submission_facts(id: str, facts: List[Any]):
    pass


# Todo: Implement
def is_submission_for_qna_complete(aqna_id: str):
    pass


# Todo: Implement
def is_students_assignment_complete(ass_id: str):
    pass


# Todo: Implement
def get_assignment_progress(ass_id: str):
    pass


def get_assignment_num_questions(ass_id: str):
    pass
