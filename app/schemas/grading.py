from typing import List, Optional, Any, Union

from pydantic import BaseModel, PositiveInt
from datetime import datetime

from app.schemas.student import Student
from app.schemas.teacher import Teacher
from app.schemas.school import Klass, KlassWithoutStudentList
from app.models.enums import Subject, Grade, AssignmentState, Curriculum, ScoringState, SubmissionState

from app.schemas.mongo_helpers import ObjectIdStr


class FactContentWithoutSerializedFacts(BaseModel):
    fact: str
    sentence: str
    score: Optional[int]

    class Config:
        orm_mode = True


class FactContent(FactContentWithoutSerializedFacts):

    serialized_fact: Any

    class Config:
        orm_mode = True


class QnA(BaseModel):
    subject: Subject
    topic: str
    curriculum: Curriculum
    grade: Grade
    parent: Optional[ObjectIdStr]
    max_score: PositiveInt
    datetime_modified: datetime

    class Config:
        orm_mode = True


class QnAWithCreator(QnA):
    created_by: Teacher

    class Config:
        orm_mode = True


class AnsContent(BaseModel):
    class Config:
        orm_mode = True


class SubjAnsContent(AnsContent):
    answer: str
    facts: Optional[List[FactContentWithoutSerializedFacts]] = []

    class Config:
        orm_mode = True


class ObjAnsContent(AnsContent):
    answer: int

    class Config:
        orm_mode = True


class SubjQnAContent(BaseModel):
    statement: str
    answer: str
    version: int
    datetime_modified: datetime
    facts: Optional[List[FactContentWithoutSerializedFacts]] = None

    class Config:
        orm_mode = True


class SubjQnA(QnA):
    content: List[SubjQnAContent]

    class Config:
        orm_mode = True


class ObjQnAContent(BaseModel):
    statement: str
    options: List[str]
    answer: PositiveInt
    version: PositiveInt

    class Config:
        orm_mode = True


class ObjQnA(QnA):
    content: List[ObjQnAContent]

    class Config:
        orm_mode = True


class AssignmentQnA(BaseModel):
    id: ObjectIdStr
    qna: Union[SubjQnA, ObjQnA]
    qna_version: Optional[PositiveInt] = None
    qna_readable_id: str
    base_facts: Optional[List[FactContentWithoutSerializedFacts]] = []
    max_score: PositiveInt

    class Config:
        orm_mode = True


class AssignmentQnAInDB(AssignmentQnA):
    assignment: ObjectIdStr

    class Config:
        orm_mode = True


class AssignmentQnAWithBaseFacts(AssignmentQnA):
    base_facts: List[FactContentWithoutSerializedFacts]

    class Config:
        orm_mode = True


class Assignment(BaseModel):
    id: ObjectIdStr
    teacher: Teacher
    name: str
    subject: Subject
    topic: str
    deadline: datetime
    klass: KlassWithoutStudentList
    datetime_modified: datetime
    state: str
    qnas: List[AssignmentQnAWithBaseFacts] = []

    class Config:
        orm_mode = True


class AssignmentQnASubmissionCreate(BaseModel):
    answer: Union[ObjAnsContent, SubjAnsContent]
    state: SubmissionState

    class Config:
        orm_mode = True


class AssignmentQnASubmission(AssignmentQnASubmissionCreate):
    id: ObjectIdStr
    student: Student
    datetime_modified: datetime
    score: Optional[int]
    scoring_state: ScoringState

    class Config:
        orm_mode = True



