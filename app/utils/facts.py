from typing import Optional, List

import requests
from loguru import logger
from mongoengine import DoesNotExist

from app.config import Settings, get_settings
from app.models import grading as models_grading
from app.models.enums import ScoringState
from app.schemas import grading as schemas_grading


def get_facts(content: str,
              metadata: dict = {},
              settings: Optional[Settings] = None):
    if settings is None: settings = get_settings()
    endpoint = "{}/predict".format(settings.svc_fact_extraction)
    logger.debug("Hitting endpoint for fact extraction: {}".format(endpoint))
    payload = {
        "pipeline_run_id": "",
        "pipeline_version": "",
        "pipeline_id": "",
        "data": {
            "client_req_id": settings.app_name,
            "body": {
                "text_content": content
            },
            "meta": metadata
        }

    }
    out_facts = []
    try:
        resp = requests.post(endpoint, json=payload)
        status = resp.json()['data'][0]["status"]
        if status == "SUCCESS":
            facts = resp.json()['data'][0]["output"]["model_output"]["data"]["facts"]
            for f in facts:
                fc = schemas_grading.FactContent(**f)
                out_facts.append(fc)
    except requests.exceptions.ConnectionError:
        logger.error("Fact extraction service is down")
    return out_facts


def compare_facts(base_facts: List[schemas_grading.FactContent],
                  answer_facts: List[schemas_grading.FactContent],
                  metadata: dict = {},
                  settings: Optional[Settings] = None):
    if settings is None: settings = get_settings()
    endpoint = "{}/predict".format(settings.svc_fact_comparison)
    logger.debug("Hitting endpoint for fact comparison: {}".format(endpoint))
    base_fact_list = []
    for fact in base_facts:
        base_fact_list.append(fact.dict())
    ans_fact_list = []
    for fact in answer_facts:
        ans_fact_list.append(fact.dict())
    similarity = {}
    if len(ans_fact_list) > 0 and len(base_fact_list) > 0:
        payload = {
            "pipeline_run_id": "",
            "pipeline_version": "",
            "pipeline_id": "",
            "data": {
                "client_req_id": settings.app_name,
                "body": {
                    "base_facts": base_fact_list,
                    "answer_facts": ans_fact_list
                },
                "meta": metadata
            }
        }
        try:
            resp = requests.post(endpoint, json=payload)
            status = resp.json()['data'][0]["status"]
            if status == "SUCCESS":
                resp_data = resp.json()['data'][0]['output']['model_output']['data']
                fact_level_similarity_scores = resp_data['fact_level_similarity_scores']
                for i in range(len(fact_level_similarity_scores)):
                    similarity[str(base_facts[i].fact_id)] = fact_level_similarity_scores[i]
            logger.bind(payload=similarity).debug("Similarity dictionary is :")
        except requests.exceptions.ConnectionError:
            logger.error("Fact comparison service is down")
    else:
        logger.debug("Length base_facts:{} answer_facts:{}".format(len(base_fact_list), len(ans_fact_list)))
    return similarity


def trigger_scoring(aqna_id: str, student_id: Optional[str] = None, settings: Optional[Settings] = None):
    logger.debug("Triggering scoring for aqna: {} student {}".format(aqna_id, student_id))
    num_scored = 0
    try:
        if student_id is None:
            aqnas_itr = models_grading.AssignmentQnASubmission.objects(aqna=aqna_id)
        else:
            aqnas_itr = models_grading.AssignmentQnASubmission.objects(aqna=aqna_id, student=student_id)

        aqna = models_grading.AssignmentQnA.objects.get(id=aqna_id)
        base_facts = aqna.base_facts
        base_fact_list = []
        for f in base_facts:
            base_fact_list.append(schemas_grading.FactContent.from_orm(f))
        for aqnas in aqnas_itr:
            answer_facts = aqnas.answer.facts
            answer_fact_list = []
            for f in answer_facts:
                answer_fact_list.append(schemas_grading.FactContent.from_orm(f))
            similarity = compare_facts(base_facts=base_fact_list, answer_facts=answer_fact_list, settings=settings)
            if len(similarity.keys()) == 0:
                state = ScoringState.Unavailable
            else:
                state = ScoringState.Scored
                aqnas.model_similarity = similarity
            aqnas.scoring_state = state
            aqnas.save()
            num_scored = num_scored + 1
    except DoesNotExist:
        logger.info("No submissions or aqna exists for aqna_id:{} and student {}".format(aqna_id, student_id))
    logger.debug("Scored {} submissions for aqna: {}".format(num_scored, aqna_id))
    return num_scored
