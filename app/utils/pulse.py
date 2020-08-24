from datetime import datetime
from typing import Optional

from loguru import logger
from mongoengine import DoesNotExist

import app.models.pulse as models_pulse
import app.models.session as models_session
import app.schemas.pulse as schemas_pulse


def get_session_attendance_aggregated(session_id: str):
    logger.debug("Get session attendance for session {}".format(session_id))
    session_attendance_agg = None
    try:
        present = models_pulse.SessionAttendance.objects(session=session_id, is_present=True).count()
        total = len(models_session.Session.objects.get(id=session_id).klass.members)
        session_attendance_agg = schemas_pulse.SessionAttendanceAggregated(total=total, present=present)
    except DoesNotExist:
        logger.info("No session exists with id:{}".format(session_id))
    return session_attendance_agg


def get_session_pulse(session_id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None):
    logger.debug("Get pulse for session:{} from:{} to {}".format(session_id, from_datetime, to_datetime))
    pulse = []
    try:
        if from_datetime is not None and to_datetime is not None:
            session_pulse_itr = models_pulse.SessionPulse.objects(session=session_id,
                                                                  datetime_sequence__lte=to_datetime,
                                                                  datetime_sequence__gte=from_datetime)
        else:
            session_pulse_itr = models_pulse.SessionPulse.objects(session=session_id)
        for sess_pulse in session_pulse_itr:
            p = schemas_pulse.SessionPulse.from_orm(sess_pulse)
            pulse.append(p)
    except DoesNotExist:
        logger.info("No pulse or session exists for session_id: {}".format(session_id))
    return pulse


def get_session_pulse_student(session_id: str):
    logger.debug("Get pulse at student level for session_id: {}".format(session_id))
    pulse = []
    try:
        session_pulse_itr = models_pulse.SessionPulseStudent.objects.no_dereference()(session=session_id)
        for sess_pulse in session_pulse_itr:
            p = schemas_pulse.SessionPulseStudent.from_orm(sess_pulse)
            pulse.append(p)
    except DoesNotExist:
        logger.info("No pulse at student level exists for session_id: {}".format(session_id))
    return pulse
