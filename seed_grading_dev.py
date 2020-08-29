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
from yaml import load, dump, FullLoader


pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
subjects = [Subject.Civics, Subject.Biology, Subject.Chemistry]
teachers = []
klasses = []
grade = Grade.Sixth
curriculum = Curriculum.IB
sections = [Section.A, Section.B]
subj_data = None
subj_data = None

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

    with open(r'subj_quest.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        subj_data = load(file, Loader=FullLoader)
        for k, v in subj_data.items():
            print(k, v)

    with open(r'obj_quest.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        subj_data = load(file, Loader=FullLoader)
        for k, v in obj_data.items():
            print(k, v)

    database.DbMgr.disconnect()


def read_vars():
    teachers_itr = Teacher.objects()
    for t in teachers_itr:
        teachers.append(t)
    klasses_itr = Klass.objects()
    for k in klasses_itr:
        klasses.append(k)


def seed_objective_questions():
    pass


def seed_subjective_questions():
    pass


def seed_assignment():
    pass


def seed_submission():
    pass


main()
