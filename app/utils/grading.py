from typing import Optional, List

from bson import ObjectId
from loguru import logger
from mongoengine import DoesNotExist
from pydantic import PositiveInt
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
import app.models.school as models_school
from app.models.enums import Grade, Section, Subject, AssignmentState, SubmissionState, ScoringState
from app.utils.facts import get_facts


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
            out_sub = schemas_grading.AssignmentQnASubmission.from_orm(sub)
            out_submissions.append(out_sub)
    except DoesNotExist:
        logger.info("No submissions exists for aqna: {} and student: {}".format(aqna_id, student_id))
    return out_submissions


def get_assignment_qna(id: str):
    logger.debug("Get assignment qna: {}".format(id))
    out_assqna = None
    try:
        assqna = models_grading.AssignmentQnA.objects.get(id=id)
        out_assqna = schemas_grading.AssignmentQnA.from_orm(assqna)
    except DoesNotExist:
        logger.info("No assignment qna exists with id: {}".format(id))
    return out_assqna


def modify_assqna_base_facts(aqna_id: str, base_fact_list: List[schemas_grading.FactContentWithoutSerializedFacts]):
    logger.bind(payload=base_fact_list).debug("Updating assqna {} with base_facts scores".format(aqna_id))
    try:
        aqna = models_grading.AssignmentQnA.objects.get(id=aqna_id)
        fact_hash = {}
        for fact in base_fact_list:
            fact_hash[fact.fact_id] = fact
        num_updated = 0
        for fact in aqna.base_facts:
            if fact.fact_id in fact_hash.keys():
                logger.debug("Resetting score for fact {} with {}".format(fact.fact_id, fact_hash[fact.fact_id].score))
                fact.score = fact_hash[fact.fact_id].score
                num_updated = num_updated + 1
        aqna.save()
    except DoesNotExist:
        logger.info("No Assignment QnA exists with id {}".format(aqna_id))
    return


def modify_assqna_submission_scores(id: str, scoring_update: schemas_grading.AssignmentQnASubmissionScoringUpdate):
    logger.bind(payload=scoring_update.dict()).debug("Updating scores for submission id {}".format(id))
    num_updated = 0
    try:
        submission = models_grading.AssignmentQnASubmission.objects.get(id=id)
        if submission.final_similarity is not None:
            submission.final_similarity = scoring_update.final_similarity
        if scoring_update.score is not None:
            submission.score = scoring_update.score
            submission.scoring_state = ScoringState.Scored
        logger.debug(submission.to_mongo())
        submission.save()
        num_updated = num_updated + 1
    except DoesNotExist:
        logger.info("No such submission exists with id : {}".format(id))
    return num_updated
