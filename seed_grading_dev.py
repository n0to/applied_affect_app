import app.utils.facts
from app.models.pulse import *
from app.models.school import *
from app.models.session import *
from app.models.student import *
from app.models.teacher import *
from app.models.enums import *
from app.models.user import *
from app.models.grading import *
import app.schemas.grading as schemas_grading
from app.db import database
import random
from faker import Faker
import datetime
import os
from app.config import get_settings_from_file
import pprint
from yaml import load, dump, FullLoader
import app.utils.grading as utils_grading

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
subjects = [Subject.History]
teachers = []
klasses = []
grade = Grade.Sixth
curriculum = Curriculum.IB
sections = [Section.A, Section.B]
subj_data = {}
obj_data = {}
obj_qnas = []
subj_qnas = []


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
    # seed_objective_questions()
    # seed_subjective_questions()
    read_questions()
    # seed_assignments()
    # seed_assignments_questions(settings)
    # seed_submissions(settings)
    score_submissions(settings)
    # database.DbMgr.disconnect()


def read_questions():
    itr = SubjQnA.objects()
    for i in itr:
        subj_qnas.append(i)

    itr = ObjQnA.objects()
    for i in itr:
        obj_qnas.append(i)


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
        print(qna, val)
        teacher = teachers[random.randint(0, len(teachers) - 1)]
        max_score = val['S']
        options = val['O']
        answer = val['A'] - 1
        content = ObjQnAContent(statement=val['Q'],
                                options=options,
                                answer=answer)
        q = ObjQnA(subject=subject,
                   topic=topic,
                   curriculum=curriculum,
                   grade=grade,
                   max_score=max_score,
                   created_by=teacher,
                   content=[content])
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
        content = SubjQnAContent(statement=val['Q'], answer=val['A'])
        teacher = teachers[random.randint(0, len(teachers) - 1)]
        max_score = val['S']
        q = SubjQnA(subject=subject,
                    topic=topic,
                    curriculum=curriculum,
                    grade=grade,
                    max_score=max_score,
                    created_by=teacher,
                    content=[content])
        q.save()
        print(q.to_mongo())


def seed_assignments():
    print("***************************************************")
    print(subj_qnas)
    print(obj_qnas)
    print(teachers)
    print(klasses)
    topic = "The Delhi Sultans"
    subject = Subject.History
    deadline_start_time = datetime.datetime.now()

    for i in range(1, 10):
        timedel = datetime.timedelta(days=i)
        teacher = teachers[random.randint(0, len(teachers) - 1)]
        name = "History Assignment # {}".format(random.randint(1000, 2000))
        deadline = deadline_start_time + timedel
        klass = klasses[random.randint(0, random.randint(0, len(klasses) - 1))]
        ass = Assignment(topic=topic,
                         teacher=teacher,
                         name=name,
                         deadline=deadline,
                         klass=klass,
                         subject=subject)
        ass.save()
        print(ass.to_mongo())


def seed_assignments_questions(settings):
    print("***************************************************")
    asses = Assignment.objects()
    for ass in asses:
        i = 1
        for qna in subj_qnas:
            latest_version = qna.content[0].version
            # get facts here
            facts = app.utils.facts.get_facts(content=qna.content[0].answer, metadata={}, settings=settings)
            efacts = []
            for f in facts:
                efact = FactContent(**f.dict())
                efacts.append(efact)
            aqna = AssignmentQnA(assignment=ass,
                                 qna=qna,
                                 qna_version=latest_version,
                                 base_facts=efacts,
                                 qna_readable_id="QNA{}".format(i),
                                 max_score=qna.max_score)
            i = i + 1
            aqna.save()
            print(aqna.to_mongo())


def seed_submissions(settings):
    print("***************************************************")
    ass = Assignment.objects().first()
    aqnas = AssignmentQnA.objects(assignment=str(ass.id))
    print("QNAS:", aqnas)
    students = ass.klass.members
    submission_dir = "/home/neo/Downloads/submission/"
    ques_hash = {}
    for aqna in aqnas:
        ques_hash[aqna.qna_readable_id] = str(aqna.id)
    pp.pprint(ques_hash)
    for student in students:
        sub_file = submission_dir + student.school_id + ".yaml"
        print(sub_file)
        with open(sub_file) as file:
            print("***************************************************")
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            sub_data = load(file, Loader=FullLoader)
            questions = sub_data['Questions']
            for qna, val in questions.items():
                aqna_id = ques_hash[qna]
                ans = val['A']
                facts = app.utils.facts.get_facts(content=ans, metadata={}, settings=settings)
                efacts = []
                for f in facts:
                    efact = FactContent(**f.dict())
                    efacts.append(efact)
                answer = SubjAnsContent(answer=ans, facts=efacts)
                saqnas = AssignmentQnASubmission(student=student,
                                                 assignment=ass,
                                                 state=SubmissionState.Submitted,
                                                 aqna=aqna_id,
                                                 answer=answer,
                                                 scoring_state=ScoringState.Pending)
                pp.pprint(saqnas.to_mongo())
                saqnas.save()


def score_submissions(settings):
    print("***************************************************")
    saqnas = AssignmentQnASubmission.objects()
    for saqna in saqnas:
        aqna_id = saqna.aqna.id
        student_id = saqna.student.id
        print("Triggering scoring for {} {}".format(aqna_id, student_id))
        app.utils.facts.trigger_scoring(aqna_id=aqna_id, student_id=student_id, settings=settings)


main()
