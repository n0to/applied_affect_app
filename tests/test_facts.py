import unittest
from random import random

import requests
from app.config import get_settings
from app.db.database import DbMgr
import app.schemas.grading as schemas_grading
import app.models.grading as models_grading
import app.utils.grading as utils_grading
import pprint

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)

base_facts = []


class TestMongo(unittest.TestCase):

    @classmethod
    def setUp(cls):
        settings = get_settings()
        DbMgr.connect(settings.mongo_dbname,
                      settings.mongo_username,
                      settings.mongo_password,
                      settings.mongo_host)

    @classmethod
    def tearDown(cls):
        DbMgr.disconnect()

    def test_get_facts(self):
        settings = get_settings()
        print(settings.svc_fact_extraction)
        endpoint = "{}/predict".format(settings.svc_fact_extraction)
        qnasub = models_grading.AssignmentQnASubmission.objects().no_dereference().first()
        answer = qnasub.answer.answer
        meta = {
            # "assignment_id": str(qnasub.assignment.id),
            # "question_id": str(qnasub.aqna.id),
            # "student_id": str(qnasub.student.id)
        }
        payload = {
            "pipeline_run_id": "",
            "pipeline_version": "",
            "pipeline_id": "",
            "data": {
                "client_req_id": str(qnasub.id),
                "body": {
                    "text_content": answer
                },
                "meta": meta
            }
        }
        # pp.pprint(payload)
        resp = requests.post(endpoint, json=payload)
        data = resp.json()['data']
        pp.pprint(data)
        for d in data:
            facts = d["output"]["model_output"]["data"]["facts"]
            for f in facts:
                fc = schemas_grading.FactContent(**f)
                fc.score = 2
                base_facts.append(fc)
                # pp.pprint(fc.dict())
                pp.pprint("******************************************")
                fcmong = models_grading.FactContent(**fc.dict())
                pp.pprint(fcmong.to_mongo())

    def test_util_get_facts(self):
        qnasub = models_grading.AssignmentQnA.objects.get(id="5f54b6a5b4df31598e9609a3")
        answer = qnasub.qna.content[0].answer
        meta = {
        }
        facts = utils_grading.get_facts(answer, meta)
        pp.pprint(facts)

    def test_get_scoring(self):
        self.test_get_facts()
        settings = get_settings()
        print(settings.svc_fact_comparison)
        qnasub = models_grading.AssignmentQnASubmission.objects().no_dereference().first()
        endpoint = "{}/predict".format(settings.svc_fact_comparison)
        base_fact_list = []
        for fact in base_facts:
            base_fact_list.append(fact.dict())
        answer_fact_list = base_fact_list
        payload = {
            "pipeline_run_id": "",
            "pipeline_version": "",
            "pipeline_id": "",
            "data": {
                "client_req_id": str(qnasub.id),
                "body": {
                    "base_facts": base_fact_list,
                    "answer_facts": answer_fact_list
                },
                "meta": {
                    "assignment_id": str(qnasub.assignment.id),
                    "question_id": str(qnasub.aqna.id),
                    "student_id": str(qnasub.student.id)
                }
            }
        }
        # pp.pprint(payload)
        pp.pprint(payload)
        resp = requests.post(endpoint, json=payload)
        data = resp.json()['data']
        pp.pprint(data)
