from datetime import datetime
from mongoengine import (
    Document,
    LazyReferenceField,
    BooleanField,
    IntField,
    DateTimeField,
    StringField,
    ReferenceField,
    EmbeddedDocument)


class Question(Document):
    pass


class ObjectiveQuestion(Question):
    pass


class SubjectiveQuestion(Question):
    pass


class EmbQuestion(Document):
    pass


class EmbObjectiveQuestion(Question):
    pass


class EmbSubjectiveQuestion(Question):
    pass


class Answer(EmbeddedDocument):
    pass


class SubjectiveAnswer(Document):
    pass


class ObjectiveAnswer(Document):
    pass


class Answer(Document):
    pass


class SubjectiveAnswer(Document):
    pass


class ObjectiveAnswer(Document):
    pass


class Assignment(Document):
    pass


class Submission(Document):
    pass

