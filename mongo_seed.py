import models
import database
import enum_models
import random
from faker import Faker
import datetime


def main():
    print("Getting Pymongo connection")
    database.DbMgrPymongo.initialize()
    db = database.DbMgrPymongo.get_db()
    print("Getting Mongoengine connection")
    database.DbMgr.connect()
    fake = Faker('en_IN')
    # seed_school(db)
    # cameras = seed_camera(db)
    # rooms = seed_room(db, cameras)
    # students = seed_student(db, fake)
    # teachers = seed_teacher(db, fake)
    # klasses = seed_klass(db, students)
    # sessions = seed_session(db, fake, teachers, klasses, rooms)
    seed_session_attendance(db)
    database.DbMgr.disconnect()


def seed_school(db):
    # Add school
    db.school.delete_many({})
    indus = models.School(name='Indus International School')
    indus.group_name = 'Indus International School'
    indus.location = 'Bangalore'
    indus.email = "contactus@indus.com"
    print("adding school", indus.to_mongo())
    indus.save()


def seed_camera(db):
    db.camera.delete_many({})
    camera1 = models.Camera(name='Intel Intellisense')
    print("adding camera1", camera1.to_mongo())
    camera1.save()

    camera2 = models.Camera(name='Intel Intellisense')
    print("adding camera2", camera2.to_mongo())
    camera2.save()

    return [camera1, camera2]


def seed_room(db, cameras):
    db.room.delete_many({})
    room1 = models.Room(name='ClassRoom A GF')
    room1.cameras = cameras
    room1.save()
    room2 = models.Room(name='ClassRoom B GF')
    room2.cameras = cameras
    room2.save()
    return [room1, room2]


def seed_student(db, fake):
    db.student.delete_many({})
    db.guardian.delete_many({})
    school_prefix = 'IND'
    students = []
    grade = enum_models.Grade.Sixth.name
    curriculum = enum_models.Curriculum.IB.name
    for i in range(1, 20):
        st_id = school_prefix + str(random.randint(100, 1000))
        st_name = fake.name()
        st = models.Student(student_id=st_id, name=st_name, grade=grade, curriculum=curriculum)
        print("Saving Student #" + str(i) + ": details: " + st.to_json())
        st.save()
        students.append(st)
        g_name = fake.name()
        g_email = g_name.lower().replace(" ", "") + "@example.com"
        g_phone = str(random.randint(7777111111, 9999999999))
        guardian = models.Guardian(name=g_name, email=g_email, phone=g_phone, students=[st])
        print("Saving Guardian " + guardian.to_json())
        guardian.save()
    return students


def seed_teacher(db, fake):
    school_prefix = 'INDT'
    db.teacher.delete_many({})
    teachers = []
    for i in range(1, 3):
        t_id = school_prefix + str(random.randint(100, 1000))
        t_name = fake.name()
        t_email = t_name.lower().replace(" ", "") + "@example.com"
        t_phone = str(random.randint(7777111111, 9999999999))
        teacher = models.Teacher(name=t_name, email=t_email, phone=t_phone, teacher_id=t_id)
        print("Saving Teacher " + teacher.to_json())
        teacher.save()
        teachers.append(teacher)
    return teachers


def seed_klass(db, students):
    db.klass.delete_many({})
    db.student_group.delete_many({})
    grade = enum_models.Grade.Sixth.name
    section = enum_models.Section.A.name
    curriculum = enum_models.Curriculum.IB.name
    sg1 = models.StudentGroup(name='all', members=students[:10]).save()
    sg2 = models.StudentGroup(name='Top Performers', members=students[:3]).save()
    sg3 = models.StudentGroup(name='Low Performers', members=students[4:8]).save()
    klass1 = models.Klass(grade=grade, section=section, curriculum=curriculum, student_groups=[sg1, sg2, sg3])
    klass1.save()
    print("Saving Klass " + klass1.to_json())

    grade = enum_models.Grade.Sixth.name
    section = enum_models.Section.B.name
    curriculum = enum_models.Curriculum.IB.name
    sg4 = models.StudentGroup(name='all', members=students[10:]).save()
    sg5 = models.StudentGroup(name='Top Performers', members=students[10:13]).save()
    sg6 = models.StudentGroup(name='Low Performers', members=students[14:18]).save()
    klass2 = models.Klass(grade=grade, section=section, curriculum=curriculum, student_groups=[sg4, sg5, sg6])
    print("Saving Klass " + klass2.to_json())
    klass2.save()
    return [klass1, klass2]


def seed_session(db, fake, teachers, klasses, rooms):
    sessions = []
    db.session.delete_many({})
    subjects = [enum_models.Subject.Civics, enum_models.Subject.Biology, enum_models.Subject.Chemistry]
    for i in range(1, 10):
        hour = random.randint(10, 11)
        year = '2020'
        month = '07'
        day = random.randint(20, 22)
        st_date_str = year + month + str(day) + " " + str(hour) + ":00:00"
        en_date_str = year + month + str(day) + " " + str(hour + 1) + ":00:00"
        st_time = datetime.datetime.strptime(st_date_str, "%Y%m%d %H:%M:%S")
        en_time = datetime.datetime.strptime(en_date_str, "%Y%m%d %H:%M:%S")
        klass = klasses[random.randint(0, len(klasses) - 1)]
        teacher = teachers[random.randint(0, len(teachers) - 1)]
        room = rooms[random.randint(0, len(rooms) - 1)]
        subject = subjects[random.randint(0, len(subjects) - 1)].name
        s_config = models.SessionConfiguration()
        s_scenario = models.SessionScenario(name=enum_models.Scenario.Lecture.name)
        session = models.Session(klass=klass,
                                 room=room,
                                 teacher=teacher,
                                 subject=subject,
                                 scheduled_start_time=st_time,
                                 scheduled_end_time=en_time,
                                 configs=[s_config],
                                 scenarios=[s_scenario])
        print("Saving session: ", session.to_json())
        session.save()
        sessions.append(session)
    return sessions


def seed_session_attendance(db):
    # Lets to attendance for a session
    db.session_attendance.delete_many({})
    db.session_pulse_student.delete_many({})
    db.session_pulse.delete_many({})

    sessions = models.Session.objects({})
    attendance = [True, False, True]
    for session in sessions:
        klass = session.klass.fetch()
        for sg in klass.student_groups:
            sgf = sg.fetch()
            if sgf.name == 'all':
                students = sgf.members
                for student in students:
                    stf = student.fetch()
                    print("Saving attendance for student: ", stf.name)
                    models.SessionAttendance(session=session, student=stf,
                                             is_present=attendance[random.randint(0, 2)]).save()
                    print("Saving pulse for student: ", stf.name)
                    models.SessionPulseStudent(session=session, student=stf, attentiveness=random.randint(70, 100),
                                               engagement=random.randint(70, 100)).save()
            print("Saving attendance for student group: ", sgf.name)
            models.SessionPulse(session=session, student_group=sgf, attentiveness=random.randint(70, 100),
                                engagement=random.randint(70, 100)).save()


main()
