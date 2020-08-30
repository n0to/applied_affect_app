from app.models.pulse import *
from app.models.school import *
from app.models.session import *
from app.models.student import *
from app.models.teacher import *
from app.models.enums import *
from app.models.user import *
from app.models.grading import *
from app.db import database
import random
from faker import Faker
import datetime
import os
from app.config import get_settings_from_file
import pprint
from yaml import load, dump, FullLoader


pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
subjects = [Subject.History]
teachers = []
klasses = []
grade = Grade.Sixth
curriculum = Curriculum.IB
sections = [Section.A, Section.B]
subj_data = {}
obj_data = {}
obj_questions = []
subj_questions = []


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
    read_vars()
    #seed_objective_questions()
    #seed_subjective_questions()
    read_questions()
    #seed_assignments()
    #seed_assignments_questions()
    seed_submissions()
    database.DbMgr.disconnect()


def read_questions():
    itr = SubjectiveQuestion.objects()
    for i in itr:
        subj_questions.append(i)

    itr = ObjectiveQuestion.objects()
    for i in itr:
        obj_questions.append(i)


def read_vars():
    global teachers
    global klasses
    global subj_data
    global obj_data

    teachers_itr = Teacher.objects()
    for t in teachers_itr:
        teachers.append(t)
    klasses_itr = Klass.objects()
    for k in klasses_itr:
        klasses.append(k)
    with open(r'subj_quest.yaml') as file:
        print("***************************************************")
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        subj_data = load(file, Loader=FullLoader)
        for k, v in subj_data.items():
            print(k, v)

    with open(r'obj_quest.yaml') as file:
        print("***************************************************")
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        obj_data = load(file, Loader=FullLoader)
        for k, v in obj_data.items():
            print(k, v)


def seed_objective_questions():
    print("***************************************************")
    print("seeding objective questions")
    subject = Subject(obj_data['Subject'])
    topic = obj_data['Topic']
    curriculum = Curriculum(obj_data['Curriculum'])
    grade = Grade(obj_data['Grade'])
    questions = obj_data['Questions']
    for qna, val in questions.items():
        options = val['O']
        max_score = val['S']
        content = VersionedContent(content=val['Q'], version=1)
        model_answer = ObjectiveAnswer(index=val['A']-1)
        q = ObjectiveQuestion(options=options,
                              max_score=max_score,
                              model_answer=model_answer,
                              content=content,
                              subject=subject,
                              curriculum=curriculum,
                              topic=topic,
                              grade=grade)
        q.save()
        print(q.to_mongo())


def seed_subjective_questions():
    print("***************************************************")
    print("seeding subjective questions")
    subject = Subject(subj_data['Subject'])
    topic = subj_data['Topic']
    curriculum = Curriculum(subj_data['Curriculum'])
    grade = Grade(subj_data['Grade'])
    questions = subj_data['Questions']
    for qna, val in questions.items():
        content = VersionedContent(content=val['Q'], version=1)
        ans_content = VersionedContent(content=val['A'], version=1)
        model_answer = SubjectiveAnswer(content=ans_content)
        q = SubjectiveQuestion(subject=subject,
                               topic=topic,
                               curriculum=curriculum,
                               grade=grade,
                               model_answer=model_answer,
                               content=content)
        q.save()
        print(q.to_mongo())


def seed_assignments():
    print("***************************************************")
    print(subj_questions)
    print(obj_questions)
    print(teachers)
    print(klasses)
    topic = "The Delhi Sultans"
    subject = Subject.History
    deadline_start_time = datetime.datetime.now()

    for i in range(1,10):
        timedel = datetime.timedelta(days=i)
        teacher = teachers[random.randint(0, len(teachers)-1)]
        name = "History Assignment # {}".format(random.randint(1000, 2000))
        deadline = deadline_start_time + timedel
        klass = klasses[random.randint(0, random.randint(0, len(klasses)-1))]
        ass = Assignment(topic=topic,
                         teacher=teacher,
                         name=name,
                         deadline=deadline,
                         klass=klass,
                         subject=subject)
        ass.save()
        print(ass.to_mongo())


def seed_assignments_questions():
    print("***************************************************")
    asses = Assignment.objects()
    for ass in asses:
        for ques in subj_questions:
            qna = QnA(question=ques,
                      question_version=1)
            aqna = AssignmentQnA(assignment=ass,
                                 qna=qna)

            aqna.save()
            print(aqna.to_mongo())


def get_student_answer(question, version):
    ans = question.model_answer.content.content
    return SubjectiveAnswer(content=VersionedContent(content=ans, version=1))


def seed_submissions():
    print("***************************************************")
    ass = Assignment.objects().first()
    aqnas = AssignmentQnA.objects(assignment=str(ass.id))
    print("QNAS:", aqnas)
    students = ass.klass.members
    for student in students:
        print(student.name)
        for aqna in aqnas:
            ans = get_student_answer(aqna.qna.question, aqna.qna.question_version)
            asub = AssignmentSubmission(student=student,
                                        assignment=ass,
                                        aqna=aqna,
                                        answer=ans)
            asub.save()
            print(asub.answer.content.content)


main()
