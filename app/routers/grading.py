from datetime import datetime
from typing import List, Optional, Union

from fastapi import APIRouter, HTTPException
from pydantic import PositiveInt

import app.utils.facts
import app.utils.grading as utils_grading
from app.models.enums import Subject, Grade, Section, AssignmentState
from app.schemas.grading import Assignment, AssignmentQnAWithBaseFacts, AssignmentQnASubmission, SubjAnsContent, \
    ObjAnsContent, AssignmentQnASubmissionCreate, FactContentWithoutSerializedFacts, \
    AssignmentQnASubmissionScoringUpdate

router = APIRouter()


@router.get("/assignment/search", response_model=List[Assignment])
def search_assignments(teacher: Optional[str] = None,
                       subject: Optional[Subject] = None,
                       grade: Optional[Grade] = None,
                       section: Optional[Section] = None,
                       state: Optional[AssignmentState] = None,
                       deadline: Optional[datetime] = None,
                       max_records: Optional[PositiveInt] = 3):
    asses = utils_grading.search_assignments(teacher=teacher,
                                             subject=subject,
                                             grade=grade,
                                             section=section,
                                             state=state,
                                             deadline=deadline,
                                             max_records=max_records)
    if not len(asses):
        raise HTTPException(status_code=404, detail="Assignments not found")
    return asses


@router.get("/assignment/{id}", response_model=Assignment)
def get_assignment(id: str, get_qnas: Optional[bool] = False):
    ass = utils_grading.get_assignment(id=id, get_qnas=get_qnas)
    if not ass:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return ass


@router.get("/assignment_qna/{id}", response_model=AssignmentQnAWithBaseFacts)
def get_assignment_qna(id: str):
    ass_qna = utils_grading.get_assignment_qna(id=id)
    if not ass_qna:
        raise HTTPException(status_code=404, detail="No assignment qna found")
    return ass_qna


''' 
@router.put("/assignment_qna/{id}/facts")
def update_assignment_qna_facts(id: str, facts: List[Any]):
    resp = utils_grading.update_assignment_qna_facts(id, facts)
    if not resp:
        raise HTTPException("Couldn't update assignment_qna facts")
    return resp


@router.put('/assignment_qna_submission/{id}/facts')
def update_assignment_submission_facts(id: str, ans_content: List[AnsContent]):
    resp = utils_grading.update_assignment_qna_submission_facts(id, ans_content)
    if not resp:
        raise HTTPException("Couldn't update assignment qna submission facts")
    return resp
'''


@router.get('/assignment_qna/{aqna_id}/submissions', response_model=List[AssignmentQnASubmission])
def get_assignment_qna_submission(aqna_id: str, student_id: Optional[str] = None):
    resp = utils_grading.get_assignment_qna_submission(aqna_id=aqna_id, student_id=student_id)
    if not len(resp):
        raise HTTPException("Couldn't find any submissions for the assignment")
    return resp


@router.post("/assignment_qna/{aqna_id}/student/{s_id}/submission", response_model=int)
def post_submission(aqna_id: str, s_id: str, submission: AssignmentQnASubmissionCreate):
    num_updated = utils_grading.post_qna_submission(aqna_id, s_id, submission)
    if not num_updated:
        raise HTTPException("Couldn't update assignment_qna student submission")
    return num_updated


# This shouldn't be a GET. There is no other appropriate verb for it.
# Todo: Move this to a background job
@router.get("/assignment_qna/{aqna_id}/score", response_model=bool)
def trigger_scoring(aqna_id: str, s_id: Optional[str] = None):
    num_scored = app.utils.facts.trigger_scoring(aqna_id=aqna_id, student_id=s_id)
    return num_scored


@router.put("/assignment_qna/{aqna_id}/base_fact_scores", response_model=int)
def modify_assqna_base_facts(aqna_id: str, base_fact_list: List[FactContentWithoutSerializedFacts]):
    num_updated = utils_grading.modify_assqna_base_facts(aqna_id=aqna_id, base_fact_list=base_fact_list)
    return num_updated


@router.put("/assignment_qna_submission/{id}/scores", response_model=int)
def modify_assqna_submission_scores(id: str, scoring_update: AssignmentQnASubmissionScoringUpdate):
    num_updated = utils_grading.modify_assqna_submission_scores(id=id, scoring_update=scoring_update)
    return num_updated

