from app.models.session import (
    Session,
    SessionConfiguration,
    SessionScenario
)
from app.models.pulse import SessionAttendance, SessionPulse, SessionPulseStudent

from app.models.enum_models import (
    Section,
    Subject,
    Grade
)


def get_session(session_id: str):
    session = Session.objects.get(id=session_id)
    return session


def get_session_attendance(session_id: str):
    rows = SessionAttendance.objects.get(session_id=session_id)
    return rows


def get_session_pulse(session_id: str):
    rows = SessionPulse.objects.get(session_id=session_id)
    return rows


def get_session_pulse_student(session_id: str):
    rows = SessionPulseStudent.objects.get(session_id=session_id)
    return rows


def create_session():
    pass


def update_session():
    pass

