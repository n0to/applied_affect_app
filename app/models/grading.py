from datetime import datetime

from mongoengine import (
    Document,
    IntField,
    DateTimeField,
    StringField,
    ReferenceField,
    EmbeddedDocument,
    ListField,
    ObjectIdField,
    DynamicField,
    EmbeddedDocumentField)

from app.models.school import Klass
from app.models.student import Student
from app.models.teacher import Teacher


class Fact(EmbeddedDocument):
    content = DynamicField()


class VersionedContent(EmbeddedDocument):
    content = StringField(required=True)
    datetime_created = DateTimeField(default=datetime.now())
    version = IntField(required=True)


class Answer(EmbeddedDocument):
    content = EmbeddedDocumentField(VersionedContent, required=True)

    meta = {'allow_inheritance': True}


class SubjectiveAnswer(Answer):
    facts = ListField(EmbeddedDocumentField(Fact))


class ObjectiveAnswer(Answer):
    index = IntField(required=True)


class Question(Document):
    subject = StringField(required=True)
    topic = StringField(required=True)
    curriculum = StringField(required=True)
    grade = StringField(required=True)
    parent = ObjectIdField()
    content = EmbeddedDocumentField(VersionedContent, required=True)
    max_score = IntField()
    created_by = ReferenceField(Teacher)
    datetime_modified = DateTimeField()
    model_answer = EmbeddedDocumentField(Answer)

    meta = {'allow_inheritance': True}


class SubjectiveQuestion(Question):
    pass


class ObjectiveQuestion(Question):
    options = ListField(StringField(), required=True)


class QnA(EmbeddedDocument):
    question = ReferenceField(Question, required=True)
    question_version = IntField()
    answer = EmbeddedDocumentField(Answer)
    score = IntField()


class Assignment(Document):
    teacher = ReferenceField(Teacher, required=True)
    name = StringField(required=True)
    subject = StringField(required=True)
    topic = StringField(required=True)
    deadline = DateTimeField()
    klass = ReferenceField(Klass)
    state = StringField()
    datetime_modified = DateTimeField(default=datetime.now())


class AssignmentQnA(Document):
    assignment = ReferenceField(Assignment, required=True)
    qna = EmbeddedDocumentField(QnA, required=True)


class AssignmentSubmission(Document):
    student = ReferenceField(Student, required=True)
    assignment = ReferenceField(Assignment, required=True)
    # Reference to assignment QnA which contains model/curated answer
    qna = ReferenceField(AssignmentQnA, required=True)
    answer = EmbeddedDocumentField(Answer)  # Answer submitted by student
    datetime_modified = DateTimeField(default=datetime.now())
