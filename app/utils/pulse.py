from datetime import datetime
from typing import Optional

from mongoengine import DoesNotExist
from loguru import logger
import app.schemas.pulse as schemas_pulse
import app.models.pulse as models_pulse
import app.models.session as models_session
import app.schemas.student as schemas_student


def get_session_attendance_aggregated(id: str):
    sat_agg = None
    try:
        student_groups = models_session.Session.objects.get(id=id).klass.student_groups
        total = None
        for sg in student_groups:
            if sg.name == "all":
                total = len(sg.members)
                break
        present = models_pulse.SessionAttendance.objects(session=id, is_present=True).count()
        sat_agg = schemas_pulse.SessionAttendanceAggregated(total=total, present=present)
    except DoesNotExist:
        sat_agg = None
    return sat_agg


def get_session_pulse(id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None):
    logger.debug("Get pulse for session:{} from:{} to {}".format(id, from_datetime, to_datetime))
    pulse = []
    try:
        student_groups_hash = {}
        student_groups = models_session.Session.objects.get(id=id).klass.student_groups
        for sg in student_groups:
            student_groups_hash[str(sg.id)] = sg.name
        logger.debug("Start fetching from Mongo")
        session_pulse_itr = models_pulse.SessionPulse.objects(session=id)
        logger.debug("Finished fetching from Mongo")
        for sess_pulse in session_pulse_itr:
            sg = schemas_student.StudentGroup(name=student_groups_hash[str(sess_pulse.student_group.id)])
            p = schemas_pulse.SessionPulse(datetime_sequence=sess_pulse.datetime_sequence,
                                           student_group=sg,
                                           attentiveness=sess_pulse.attentiveness,
                                           engagement=sess_pulse.engagement)
            pulse.append(p)
        logger.debug("Finished de-marshaling")
    except DoesNotExist:
        pulse = []
    return pulse


def get_session_pulse_student(id: str):
    pulse = []
    try:
        session_pulse_itr = models_pulse.SessionPulseStudent.objects(session=id)
        for sess_pulse in session_pulse_itr:
            p = schemas_pulse.SessionPulseStudent.from_orm(sess_pulse)
            pulse.append(p)
    except DoesNotExist:
        pulse = []
    return pulse
