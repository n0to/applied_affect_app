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
    EmbeddedDocumentField, SequenceField, SortedListField, EmbeddedDocumentListField, FloatField)

from app.models.school import Klass
from app.models.student import Student
from app.models.teacher import Teacher


class FactContent(EmbeddedDocument):
    fact = StringField()
    sentence = StringField()
    serialized_fact = DynamicField()
    score = FloatField()


class QnA(Document):
    subject = StringField(required=True)
    topic = StringField(required=True)
    curriculum = StringField(required=True)
    grade = StringField(required=True)
    parent = ObjectIdField()
    max_score = IntField()
    created_by = ReferenceField(Teacher)
    datetime_modified = DateTimeField(default=datetime.now())

    meta = {'allow_inheritance': True}


class SubjQnAContent(EmbeddedDocument):
    statement = StringField(required=True)
    answer = StringField()
    version = SequenceField()
    datetime_modified = DateTimeField(default=datetime.now())
    facts = EmbeddedDocumentListField(FactContent)


class SubjQnA(QnA):
    content = SortedListField(EmbeddedDocumentField(SubjQnAContent), ordering='version', reverse=True, required=True)


class ObjQnAContent(EmbeddedDocument):
    statement = StringField(required=True)
    options = ListField(StringField(), required=True)
    answer = IntField()
    version = SequenceField()


class ObjQnA(QnA):
    content = SortedListField(EmbeddedDocumentField(ObjQnAContent), ordering='version', reverse=True, required=True)


class Assignment(Document):
    teacher = ReferenceField(Teacher, required=True)
    name = StringField(required=True)
    subject = StringField(required=True)
    topic = StringField(required=True)
    deadline = DateTimeField()
    klass = ReferenceField(Klass)
    datetime_modified = DateTimeField(default=datetime.now())
    state = StringField()


class AnsContent(EmbeddedDocument):
    meta = {'allow_inheritance': True}


class ObjAnsContent(AnsContent):
    answer = IntField()


class SubjAnsContent(AnsContent):
    answer = StringField()
    facts = EmbeddedDocumentListField(FactContent)


class AssignmentQnA(Document):
    assignment = ReferenceField(Assignment, required=True)
    qna = ReferenceField(QnA, required=True)
    qna_version = IntField()
    qna_readable_id = StringField()
    base_facts = EmbeddedDocumentListField(FactContent)
    max_score = IntField()


class AssignmentQnASubmission(Document):
    student = ReferenceField(Student, required=True)
    assignment = ReferenceField(Assignment, required=True)  # Assignment QnA which contains model/curated answer
    aqna = ReferenceField(AssignmentQnA, required=True)
    answer = EmbeddedDocumentField(AnsContent)
    datetime_modified = DateTimeField(default=datetime.now())
    score = IntField()
    state = StringField()
    scoring_state = StringField()


