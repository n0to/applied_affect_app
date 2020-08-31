from typing import List, Optional, Any, Union

from pydantic import BaseModel, PositiveInt
from datetime import datetime
from app.schemas.teacher import Teacher
from app.schemas.school import Klass, KlassWithoutStudentList
from app.models.enums import Subject, Grade, AssignmentState, Curriculum

from app.schemas.mongo_helpers import ObjectIdStr


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
    facts: Optional[List[Any]] = None

    class Config:
        orm_mode = True


class SubjQnAContent(BaseModel):
    statement: str
    answer: str
    version: int
    datetime_modified: datetime
    facts: Optional[List[Any]] = None

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
    qna: Union[SubjQnA, ObjQnA]
    qna_version: Optional[PositiveInt] = None

    class Config:
        orm_mode = True


class AssignmentQnAInDB(AssignmentQnA):
    assignment: ObjectIdStr

    class Config:
        orm_mode = True


class AssignmentQnAWithTopAnswers(AssignmentQnA):
    top_answers: List[SubjAnsContent]

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
    qnas: List[AssignmentQnA] = []

    class Config:
        orm_mode = True


class AssignmentSubmission(BaseModel):
    id: ObjectIdStr
    student: ObjectIdStr
    assignment: ObjectIdStr
    aqna: AssignmentQnA
    answer: AnsContent
    datetime_modified: datetime
    score: PositiveInt
    state: AssignmentState

    class Config:
        orm_mode = True