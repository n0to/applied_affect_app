from app.models.pulse import *
from app.models.school import *
from app.models.session import *
from app.models.student import *
from app.models.teacher import *
from app.models.enums import *
from app.models.user import *
from app.db import database
import random
from faker import Faker
import datetime
import os
from app.config import get_settings_from_file
import pprint

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
password = '$2b$12$lqco3yl48gjsr4Qk2T7s1.i1X//G0w.eTQE3T.5m0RwK8/1HjPUcG'
subjects = [Subject.Civics, Subject.Biology, Subject.Chemistry]


def main():
    conf = os.path.dirname(os.path.realpath(__file__)) + "/app/dev.env"
    print(f"Reading Settings: {conf}")
    settings = get_settings_from_file(conf)
    pp.pprint(settings.dict())
    print("Getting Pymongo connection")
    db = database.DbMgrPymongo.get_db(uri=settings.mongo_conn_str,
                                      db=settings.mongo_dbname)
    print("Getting Mongoengine connection")
    database.DbMgr.connect(db=settings.mongo_dbname,
                           username=settings.mongo_username,
                           password=settings.mongo_password,
                           host=settings.mongo_host)
    fake = Faker('en_IN')
    # seed_school(db)
    # cameras = seed_camera(db)
    # rooms = seed_room(db, cameras)
    # db.user.delete_many({})
    # students = seed_student(db, fake)
    # teachers = seed_teacher(db, fake)
    # seed_school_admin(db, fake)
    # seed_admin()
    # klasses = seed_klass(db, students)
    # sessions = seed_session(db, fake, teachers, klasses, rooms)
    # seed_session_attendance(db)
    seed_future_classes(db, fake)
    database.DbMgr.disconnect()


def seed_school(db):
    # Add school
    db.school.delete_many({})
    indus = School(name='Indus International School')
    indus.group_name = 'Indus International School'
    indus.location = 'Bangalore'
    indus.email = "contactus@indus.com"
    print("adding school", indus.to_mongo())
    indus.save()


def seed_camera(db):
    db.camera.delete_many({})
    camera1 = Camera(name='Intel Intellisense', stream_url='http://camera1.com')
    print("Adding camera1", camera1.to_mongo())
    camera1.save()

    camera2 = Camera(name='Intel Intellisense', stream_url='http://camera2.com')
    print("Adding camera2", camera2.to_mongo())
    camera2.save()

    return [camera1, camera2]


def seed_room(db, cameras):
    db.room.delete_many({})
    room1 = Room(name='ClassRoom 1 GF')
    room1.cameras = [cameras[0]]
    room1.save()
    room2 = Room(name='ClassRoom 2 GF')
    room2.cameras = [cameras[1]]
    room2.save()
    return [room1, room2]


def seed_student(db, fake):
    school_prefix = 'IND'
    students = []
    grade = Grade.Sixth
    curriculum = Curriculum.IB
    for i in range(1, 20):
        st_id = school_prefix + str(random.randint(100, 1000))
        st_name = fake.name()
        st_email = st_name.lower().replace(" ", "") + str(random.randint(0, 100)) + "@example.com"
        st = Student(school_id=st_id,
                     name=st_name,
                     grade=grade,
                     curriculum=curriculum,
                     email=st_email,
                     hashed_password=password)
        print("Saving Student #" + str(i) + ": details: " + st.to_json())
        st.save()
        students.append(st)

        g_name = fake.name()
        g_email = g_name.lower().replace(" ", "") + str(random.randint(0, 100)) + "@example.com"
        g_phone = str(random.randint(7777111111, 9999999999))
        guardian = Guardian(name=g_name,
                            email=g_email,
                            phone=g_phone,
                            students=[st],
                            hashed_password=password)
        print("Saving Guardian " + guardian.to_json())
        guardian.save()
    return students


def seed_teacher(db, fake):
    school_prefix = 'INDT'
    teachers = []
    for i in range(1, 2):
        t_id = school_prefix + str(random.randint(100, 1000))
        t_name = fake.name()
        t_email = t_name.lower().replace(" ", "") + str(random.randint(0, 100)) + "@indus.com"
        t_phone = str(random.randint(7777111111, 9999999999))
        teacher = Teacher(name=t_name,
                          email=t_email,
                          phone=t_phone,
                          school_id=t_id,
                          hashed_password=password)
        print("Saving Teacher " + teacher.to_json())
        teacher.save()
        teachers.append(teacher)
    return teachers


def seed_school_admin(db, fake):
    school_prefix = 'INDT'
    sa = []
    for i in range(1, 2):
        t_id = school_prefix + str(random.randint(100, 1000))
        t_name = fake.name()
        t_email = t_name.lower().replace(" ", "") + str(random.randint(0, 100)) + "@indus.com"
        t_phone = str(random.randint(7777111111, 9999999999))
        sai = SchoolAdmin(name=t_name,
                          email=t_email,
                          phone=t_phone,
                          school_id=t_id,
                          hashed_password=password)
        print("Saving Teacher " + sai.to_json())
        sai.save()
        sa.append(sai)
    return sa


def seed_admin():
    admin = Admin(name="Admin",
                  email="admin@aa.com",
                  phone="0000000000",
                  hashed_password=password).save()


def seed_klass(db, students):
    db.klass.delete_many({})
    db.student_group.delete_many({})
    grade = Grade.Sixth
    section = Section.A
    curriculum = Curriculum.IB
    sg1 = StudentGroup(name='all', members=students[:10])
    sg2 = StudentGroup(name='Top Performers', members=students[:3])
    sg3 = StudentGroup(name='Low Performers', members=students[4:8])
    klass1 = Klass(grade=grade,
                   section=section,
                   curriculum=curriculum,
                   student_groups=[sg1, sg2, sg3],
                   members=students[:10])
    klass1.save()
    print("Saving Klass " + klass1.to_json())

    grade = Grade.Sixth
    section = Section.B
    curriculum = Curriculum.IB
    sg4 = StudentGroup(name='all', members=students[10:])
    sg5 = StudentGroup(name='Top Performers', members=students[10:13])
    sg6 = StudentGroup(name='Low Performers', members=students[14:18])
    klass2 = Klass(grade=grade,
                   section=section,
                   curriculum=curriculum,
                   student_groups=[sg4, sg5, sg6],
                   members=students[10:])
    print("Saving Klass " + klass2.to_json())
    klass2.save()
    return [klass1, klass2]


def seed_session(db, fake, teachers, klasses, rooms):
    sessions = []
    db.session.delete_many({})
    subjects = [Subject.Civics, Subject.Biology, Subject.Chemistry]
    for i in range(1, 20):
        hour = random.randint(8, 14)
        e_hour = hour + 1
        year = '2020'
        month = random.randint(8, 8)
        day = random.randint(1, 23)
        st_date_str = f'{year}{month:02}{day:02} {hour:02}:00:00'
        en_date_str = f'{year}{month:02}{day:02} {e_hour:02}:00:00'
        st_time = datetime.datetime.strptime(st_date_str, "%Y%m%d %H:%M:%S")
        en_time = datetime.datetime.strptime(en_date_str, "%Y%m%d %H:%M:%S")
        klass = klasses[random.randint(0, len(klasses) - 1)]
        teacher = teachers[random.randint(0, len(teachers) - 1)]
        room = rooms[random.randint(0, len(rooms) - 1)]
        subject = subjects[random.randint(0, len(subjects) - 1)].name
        s_config = SessionConfiguration(datetime_created=st_time)
        s_scenario = SessionScenario(name=Scenario.Lecture.name, datetime_created=st_time)
        session = Session(klass=klass,
                          room=room,
                          teacher=teacher,
                          subject=subject,
                          scheduled_start_time=st_time,
                          scheduled_end_time=en_time,
                          configs=[s_config],
                          scenarios=[s_scenario],
                          state=SessionState.Ended)
        print("Saving session: ", session.to_json())
        session.save()
        sessions.append(session)
    return sessions


def seed_session_pulse_student(session, student, interval):
    print("Saving session pulse info for {} {}".format(session.id, student.name))
    for i in range(1, 3600, interval):
        time = session.actual_start_time + datetime.timedelta(seconds=i)
        SessionPulseStudent(session=session, student=student, attentiveness=random.randint(70, 100),
                            engagement=random.randint(70, 100), datetime_sequence=time).save()


def seed_session_pulse(session, student_group, interval):
    print("Saving session pulse info for {} {}:".format(session.id, student_group.name))
    for i in range(1, 3600, interval):
        time = session.actual_start_time + datetime.timedelta(seconds=i)
        SessionPulse(session=session, student_group_name=student_group.name, attentiveness=random.randint(70, 100),
                     engagement=random.randint(70, 100), datetime_sequence=time).save()


def seed_session_attendance(db):
    # Lets to attendance for a session
    db.session_attendance.delete_many({})
    db.session_pulse_student.delete_many({})
    db.session_pulse.delete_many({})
    sessions = Session.objects({})
    attendance = [True, False, True]
    for session in sessions:
        session.actual_start_time = session.scheduled_start_time
        session.actual_end_time = session.scheduled_end_time
        session.state = SessionState.Ended
        session.save()
        klass = session.klass
        for sgf in klass.student_groups:
            if sgf.name == 'all':
                students = sgf.members
                for stf in students:
                    print("Saving attendance for student: ", stf.name)
                    SessionAttendance(session=session, student=stf,
                                      is_present=attendance[random.randint(0, 2)]).save()
                    seed_session_pulse_student(session, stf, 5)
            seed_session_pulse(session, sgf, 5)


def seed_future_classes(db, fake):
    sessions = []

    teachers = []
    teachers_itr = Teacher.objects()
    for t in teachers_itr:
        teachers.append(t)

    klasses = []
    klasses_itr = Klass.objects()
    for k in klasses_itr:
        klasses.append(k)

    rooms = []
    room_itr = Room.objects()
    for r in room_itr:
        rooms.append(r)

    year = '2020'
    month = 9
    seed_day = 1
    for day_delta in range(1, 6):
        for hour in range(8, 14):
            e_hour = hour + 1
            day = (seed_day + day_delta)
            if day > 31:
                day = day - 31
                month = month + 1
            st_date_str = f'{year}{month:02}{day:02} {hour:02}:00:00'
            en_date_str = f'{year}{month:02}{day:02} {e_hour:02}:00:00'
            st_time = datetime.datetime.strptime(st_date_str, "%Y%m%d %H:%M:%S")
            en_time = datetime.datetime.strptime(en_date_str, "%Y%m%d %H:%M:%S")
            klass = klasses[random.randint(0, len(klasses) - 1)]
            teacher = teachers[random.randint(0, len(teachers) - 1)]
            room = rooms[random.randint(0, len(rooms) - 1)]
            subject = subjects[random.randint(0, len(subjects) - 1)].name
            s_config = SessionConfiguration(datetime_created=st_time)
            s_scenario = SessionScenario(name=Scenario.Lecture.name, datetime_created=st_time)
            session = Session(klass=klass,
                              room=room,
                              teacher=teacher,
                              subject=subject,
                              scheduled_start_time=st_time,
                              scheduled_end_time=en_time,
                              configs=[s_config],
                              scenarios=[s_scenario])
            print("Saving session: ", session.to_mongo())
            session.save()
            sessions.append(session)
    return sessions


main()
