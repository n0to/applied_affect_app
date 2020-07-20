import models
import database
import enum_models
import random
from faker import Faker


def main():
    print("Getting Pymongo connection")
    database.DbMgrPymongo.initialize()
    db = database.DbMgrPymongo.get_db()
    print("Getting Mongoengine connection")
    database.DbMgr.connect()
    fake = Faker('en_IN')
    seed_school(db)
    cameras = seed_camera(db)
    seed_room(db, cameras)
    seed_student(db, fake)
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


def seed_student(db, fake):
    db.student.delete_many({})
    school_prefix = 'IND'
    students = []
    grade = enum_models.Grade.Sixth.name
    curriculum = enum_models.Curriculum.IB.name
    for i in range(1, 10):
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
    for i in range(1,3):
        tr_id = school_prefix + str(random.randint(100, 1000))
        t_name = fake.name()
        t_email = g_name.lower().replace(" ", "") + "@example.com"
        t_phone = str(random.randint(7777111111, 9999999999))
        teacher = models.Teacher(name=t_name, email=t_email, phone=t_phone, teacher_id=tr_id)
        print("Saving Teacher " + teacher.to_json())
        teacher.save()
        teachers.append([teacher])
    return teachers


def seed_klass(db, students):
    pass


def seed_session(db, fake):
    pass


main()
