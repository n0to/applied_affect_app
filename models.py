from mongoengine import *


class Camera(Document):
    name = StringField()


class Room(Document):
    cameras = ListField(LazyReferenceField(Camera))
    name = StringField(required=True, unique=True)


class School(Document):
    name = StringField(required=True)
    group_name = StringField()
    location = StringField()
    email = StringField()


class User(Document):
    name = StringField(required=True)
    phone = StringField()
    email = StringField(required=True, unique=True)
    images = ListField(URLField())
    meta = {'abstract': True}


class Student(Document):
    student_id = StringField(required=True, unique=True)
    name = StringField()
    grade = StringField(required=True)
    curriculum = StringField(required=True)
    images = ListField(URLField())
    is_opt_out_individual = BooleanField(default=False)
    is_opt_out_aggregate = BooleanField(default=False)


class Guardian(User):
    students = ListField(ReferenceField(Student), required=True)


class StudentGroup(Document):
    name = StringField(required=True)
    members = ListField(LazyReferenceField(Student))


class Teacher(User):
    teacher_id = StringField(required=True, unique=True)


class Klass(Document):
    grade = StringField(required=True)
    section = StringField(required=True, unique_with='grade')
    student_groups = ListField(LazyReferenceField(StudentGroup))
    curriculum = StringField()


class Session(Document):
    klass = LazyReferenceField(Klass, required=True)
    room = LazyReferenceField(Room, required=True)
    teacher = LazyReferenceField(Teacher, required=True)
    subject = StringField(required=True)
    scheduled_start_time = DateTimeField(required=True)
    scheduled_end_time = DateTimeField(required=True)
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


class BoundingBox(EmbeddedDocument):
    x = FloatField(required=True)
    y = FloatField(required=True)
    length = FloatField(required=True)
    width = FloatField(required=True)


class FacialAnalysis(EmbeddedDocument):
    face_bbox = EmbeddedDocumentField(BoundingBox)
    roll = FloatField()
    pitch = FloatField()
    yaw = FloatField()


class SessionPulseStudentRaw(Document):
    frame_id = IntField(required=True)
    timestamp = DateTimeField(required=True)
    session = LazyReferenceField(Session, required=True)
    human_bbox = EmbeddedDocumentField(BoundingBox)
    facial_analysis = EmbeddedDocumentField(FacialAnalysis)
    detected_student = ReferenceField(Student)
    activity = StringField()


class SessionIntervention(Document):
    pass


















