import app.models.session as models_session
import app.models.enum_models as models_enum_models
import app.schemas.session as schemas_session
from typing import List, Optional


def map_scenarios(scenarios: List[models_session.SessionScenario]):
    scenarios_arr = List[schemas_session.SessionScenario]
    for scenario in scenarios:
        s = schemas_session.SessionScenario(timestamp=scenario.timestamp,
                                            name=scenario.name)

def map_configs():
    pass


def get_session(id: str):
    session = models_session.Session.objects.get(id=id)
    session_out = schemas_session.Session(id=str(session.id),
                                          grade=session.klass.grade,
                                          subject=session.subject,
                                          room=session.room,
                                          section=session.klass.section,
                                          teacher_id=session.teacher.teacher_id,
                                          video_url=session.video_url,
                                          state=session.state,
                                          scenarios=map_scenarios(session.scenarios),
                                          configs = map_configs(session.configs),
                                          scheduled_start_time = session.scheduled_start_time,
                                          scheduled_end_time= session.scheduled_end_time,
                                          actual_start_time=session.actual_start_time,
                                          actual_end_time=session.actual_end_time)


def create_session():
    pass


def update_session():
    pass