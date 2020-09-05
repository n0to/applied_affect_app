import pprint
import unittest
from typing import List

import app.utils.grading as utils_grading
from app.config import get_settings
from app.db.database import DbMgr
from app.schemas.grading import AnsContent, SubjAnsContent

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


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

    def test_connection(self):
        pp.pprint("Established the connection and tested it")

    def test_update_assignment_qna_facts(self):
        aqna_id = "5f4ba56670ca4ace3d2da157"
        ans_content_list = []
        ans1 = SubjAnsContent(answer="This is the answer I have submitted", facts=['fact1', 'fact2', 4])
        ans2 = SubjAnsContent(answer="This is the another answer I have submitted", facts=['fact3', 'fact4', 5])
        ans_content_list.append(ans1)
        ans_content_list.append(ans2)
        utils_grading.update_assignment_qna_facts(id=aqna_id, ans_content_list=ans_content_list)

    def test_update_assignment_qna_submission_facts(self):
        aqnas_id = "5f4ba670c557967b4cf6d333"
        facts = [{'bleh': 'bloh'}, [1, 2, 3]]
        utils_grading.update_assignment_qna_submission_facts(aqnas_id, facts)
