from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import PositiveInt

import app.utils.grading as utils_grading
from app.models.enums import Subject, Grade, Section, AssignmentState
from app.schemas.grading import Assignment, AssignmentQnA, AssignmentQnAWithTopAnswers

router = APIRouter()


@router.get("/assignment/{id}", response_model=Assignment)
def get_assignment(id: str, get_qnas: Optional[bool] = False):
    ass = utils_grading.get_assignment(id=id, get_qnas=get_qnas)
    if not ass:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return ass


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


@router.get("/assignment/{id}/qna", response_model=List[AssignmentQnA])
def get_assignment_qna(id: str):
    ass_qnas = utils_grading.get_assignment_qnas(assignment=id, get_top_answers=False)
    if not len(ass_qnas):
        raise HTTPException(status_code=404, detail="No QnAs found for Assignment")
    return ass_qnas


@router.get("/assignment_qna/{id}", response_model=AssignmentQnAWithTopAnswers)
def get_assignment_qna(id: str):
    ass_qna = utils_grading.get_assignment_qna(id=id, get_top_answers=True)
    if not len(ass_qna):
        raise HTTPException(status_code=404, detail="No QnAs found")
    return ass_qna


@router.put("/assignment_qna/{id}/facts")
def update_assignment_facts(payload):
    pass

