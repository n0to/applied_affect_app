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
    EmbeddedDocumentField, SequenceField, SortedListField)

from app.models.school import Klass
from app.models.student import Student
from app.models.teacher import Teacher


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
    facts = ListField(DynamicField())


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


class AnsContent(EmbeddedDocument):
    meta = {'allow_inheritance': True}


class ObjAnsContent(AnsContent):
    answer = IntField()


class SubjAnsContent(AnsContent):
    answer = StringField()
    facts = ListField(DynamicField())


class AssignmentQnA(Document):
    assignment = ReferenceField(Assignment, required=True)
    qna = ReferenceField(QnA, required=True)
    qna_version = IntField()
    # This answer and facts represents the best ones submitted
    top_answers = ListField(SubjAnsContent)


class AssignmentSubmission(Document):
    student = ReferenceField(Student, required=True)
    assignment = ReferenceField(Assignment, required=True)  # Assignment QnA which contains model/curated answer
    aqna = ReferenceField(AssignmentQnA, required=True)
    answer = EmbeddedDocumentField(AnsContent)
    datetime_modified = DateTimeField(default=datetime.now())
    score = IntField()
    state = StringField()


