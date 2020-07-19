from mongoengine import *


class Camera(Document):
    name = StringField()


class Room(Document):
    cameras = ListField(LazyReferenceField(Camera))
    name = StringField(required=True)


class School(Document):
    name = StringField(required=True)
    group_name = StringField()
    location = StringField()
    email = StringField()


class Guardian(EmbeddedDocument):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)


class Student(Document):
    student_id = StringField(required=True)
    name = StringField()
    grade = StringField(required=True)
    curriculum = StringField(required=True)
    ref_images = ListField(URLField())
    is_opt_out_individual = BooleanField(default=False)
    is_opt_out_aggregate = BooleanField(default=False)
    guardians = ListField(EmbeddedDocumentField(Guardian), required=True)


class StudentGroup(Document):
    name = StringField(required=True)
    members = ListField(LazyReferenceField(Student))


class Teacher(Document):
    teacher_id = StringField(required=True)
    name = StringField()
    email = EmailField(required=True)


class Klass(Document):
    grade = StringField(required=True)
    section = StringField(required=True)
    student_groups = ListField(LazyReferenceField(StudentGroup))
    curriculum = StringField()


class Session(Document):
    klass = LazyReferenceField(Klass)
    room = LazyReferenceField(Room)
    teacher = LazyReferenceField(Teacher)
    subject = StringField()
    scheduled_start_time = DateTimeField()
    scheduled_end_time = DateTimeField()
    actual_start_time = DateTimeField()
    actual_end_time = DateTimeField()


class SessionConfiguration(Document):
    session = LazyReferenceField(Session)
    # Minimum students in percentage to demonstrate some behavior to trigger class intervention
    th_min_student_for_int = FloatField(default=0.5)
    # Minimum time between two interventions. In seconds
    th_min_gap_bet_int = IntField(default=300)
    # Minimum time of observation before generating a student intervention. In seconds
    th_min_gap_for_student_int = IntField(default=180)


class SessionScenario(Document):
    session = LazyReferenceField(Session)
    scenario = StringField(required=True)


class SessionAttendance(Document):
    session = LazyReferenceField(Session)
    student = LazyReferenceField(Student)
    is_present = BooleanField()


class SessionPulse(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student_group = LazyReferenceField(StudentGroup)


class SessionPulseStudent(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student = LazyReferenceField(Student)


class SessionIntervention(Document):
    pass



















