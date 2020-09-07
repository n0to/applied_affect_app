from typing import Optional, List, Any, Union

from bson import ObjectId
import requests
from loguru import logger
from mongoengine import DoesNotExist, DynamicField
from pydantic import PositiveInt
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
import app.models.school as models_school
from app.config import get_settings, Settings
from app.models.enums import Grade, Section, Subject, AssignmentState, SubmissionState, ErrorCodes, ScoringState


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
def post_qna_submission(aqna_id: str, s_id: str,
                        submission: schemas_grading.AssignmentQnASubmissionCreate):
    logger.bind(payload=submission.dict()).debug("Posting aqna:{} for student: {}".format(aqna_id, s_id))
    logger.debug("Answer is of type: {}".format(type(submission.answer)))
    assignment = models_grading.AssignmentQnA.objects.only('id').get(id=aqna_id)
    if isinstance(submission.answer, schemas_grading.SubjAnsContent):
        logger.debug("Subjective answer detected")
        if submission.state == SubmissionState.Submitted:
            metadata = {}
            facts = get_facts(content=submission.answer.answer, metadata=metadata)
            submission.answer.facts = facts
        ans = models_grading.SubjAnsContent(**submission.answer.dict())
    elif isinstance(submission.answer, schemas_grading.ObjAnsContent):
        logger.debug("Objective answer detected")
        ans = models_grading.ObjAnsContent(**submission.answer.dict())
    else:
        raise NotImplemented("Unknown answer type detected")
    num_updated = models_grading.AssignmentQnASubmission.objects(student=s_id,
                                                                 aqna=aqna_id,
                                                                 assignment=str(assignment.id)).update_one(
        answer=ans,
        state=submission.state,
        upsert=True
    )
    return num_updated


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


def get_facts(content: str,
              metadata: dict = {},
              settings: Optional[Settings] = None):
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
    out_facts = []
    try:
        resp = requests.post(endpoint, json=payload)
        facts = resp.json()['data'][0]["output"]["model_output"]["data"]["facts"]
        for f in facts:
            fc = schemas_grading.FactContent(**f)
            out_facts.append(fc)
    except requests.exceptions.ConnectionError:
        logger.error("Fact extraction service is down")
    return out_facts


def compare_facts(base_facts: List[schemas_grading.FactContent],
                  answer_facts: List[schemas_grading.FactContent],
                  metadata: dict = {},
                  settings: Optional[Settings] = None):
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
        try:
            resp = requests.post(endpoint, json=payload)
            similarity = resp.json()['data'][0]['output']['model_output']['data']['similarity']
        except requests.exceptions.ConnectionError:
            logger.error("Fact comparison service is down")
            similarity = ErrorCodes.SIMILARITY_UNAVAILABLE
    else:
        similarity = ErrorCodes.SIMILARITY_UNAVAILABLE
    return similarity


def get_assignment_qna_submission(aqna_id: str, student_id: Optional[str] = None):
    out_submissions = []
    logger.debug("Getting qna submissions with aqna: {} and student: {}".format(aqna_id, student_id))
    try:
        if student_id is None:
            submissions_itr = models_grading.AssignmentQnASubmission.objects(aqna=aqna_id,
                                                                             state=SubmissionState.Submitted)
        else:
            submissions_itr = models_grading.AssignmentQnASubmission.objects(aqna=aqna_id,
                                                                             state=SubmissionState.Submitted,
                                                                             student=student_id)
        for sub in submissions_itr:
            logger.bind(payload=sub.to_mongo()).debug("From mongo")
            out_sub = schemas_grading.AssignmentQnASubmission.from_orm(sub)
            out_submissions.append(out_sub)
    except DoesNotExist:
        logger.info("No submissions exists for aqna: {} and student: {}".format(aqna_id, student_id))
    return out_submissions


def trigger_scoring(aqna_id: str):
    logger.debug("Triggering scoring for aqna: {}".format(aqna_id))
    aqnas_itr = models_grading.AssignmentQnASubmission.objects(aqna=aqna_id)
    aqna = models_grading.AssignmentQnA.objects.get(id=aqna_id)
    base_facts = aqna.base_facts
    base_fact_list = []
    for f in base_facts:
        base_fact_list.append(schemas_grading.FactContent.from_orm(f))
    num_scored = 0
    for aqnas in aqnas_itr:
        answer_facts = aqnas.answer.facts
        answer_fact_list = []
        for f in answer_facts:
            answer_fact_list.append(schemas_grading.FactContent.from_orm(f))
        similarity = compare_facts(base_fact_list)
        if similarity == ErrorCodes.SIMILARITY_UNAVAILABLE:
            state = ScoringState.Unavailable
            score = ErrorCodes.SIMILARITY_UNAVAILABLE
        else:
            score = round(similarity.aqna.max_score * similarity)
            state = ScoringState.Scored
        aqnas.score = score
        aqnas.scoring_state = state
        aqnas.save()
        num_scored = num_scored + 1
    logger.debug("Scored {} submissions for aqna: {}".format(num_scored, aqna_id))
    return num_scored

