from typing import Optional, List, Any

from bson import ObjectId
import requests
from loguru import logger
from mongoengine import DoesNotExist, DynamicField
from pydantic import PositiveInt
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
import app.models.school as models_school
from app.config import get_settings, Settings
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
    pass


def update_assignment_qna_facts(id: str, ans_content_list: List[schemas_grading.SubjAnsContent]):
    logger.bind(payload=ans_content_list).debug("Updating AQNA {} with content: ".format(id))
    ans_emb_list = []
    for ans in ans_content_list:
        ans_emb = models_grading.SubjAnsContent(**ans.dict())
        ans_emb_list.append(ans_emb)
    num_updated = models_grading.AssignmentQnA.objects(id=id).update(top_answers=ans_emb_list)
    return num_updated


def update_assignment_qna_submission_facts(id: str, facts: List[Any]):
    logger.bind(payload=facts).debug("Updating AQNA Submission {} with facts: ".format(id))
    aqnas = models_grading.AssignmentQnASubmission.objects.get(id=id)
    aqnas.answer.facts = facts
    aqnas.save()
    return 1


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


def get_facts(content: str, metadata: dict, settings: Optional[Settings]=None):
    if settings is None: settings = get_settings()
    endpoint = "{}/predict".format(settings.svc_fact_extraction)
    logger.debug("Hitting endpoint for fact extraction: {}".format(endpoint))
    payload = {
        "pipeline_run_id": "",
        "pipeline_version": "",
        "pipeline_id": "",
        "data": {
            "client_req_id": settings.app_name,
            "body": {
                "text_content": content
            },
            "meta": metadata
        }

    }
    resp = requests.post(endpoint, json=payload)
    facts = resp.json()['data'][0]["output"]["model_output"]["data"]["facts"]
    out_facts = []
    for f in facts:
        fc = schemas_grading.FactContent(**f)
        out_facts.append(fc)
    return out_facts


def compare_facts(base_facts: [schemas_grading.FactContent], answer_facts: List[schemas_grading.FactContent], metadata,
                  settings: Optional[Settings]= None):
    if settings is None: settings = get_settings()
    endpoint = "{}/predict".format(settings.svc_fact_comparison)
    logger.debug("Hitting endpoint for fact comparison: {}".format(endpoint))
    base_fact_list = []
    for fact in base_facts:
        base_fact_list.append(fact.dict())
    ans_fact_list = []
    for fact in answer_facts:
        ans_fact_list.append(fact.dict())
    if len(ans_fact_list) > 0 and len(base_fact_list) > 0:
        payload = {
            "pipeline_run_id": "",
            "pipeline_version": "",
            "pipeline_id": "",
            "data": {
                "client_req_id": settings.app_name,
                "body": {
                    "base_facts": base_fact_list,
                    "answer_facts": ans_fact_list
                },
                "meta": metadata
            }
        }
        resp = requests.post(endpoint, json=payload)
        similarity = resp.json()['data'][0]['output']['model_output']['data']['similarity']
    else:
        similarity = -1000
    return similarity


