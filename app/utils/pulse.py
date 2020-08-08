from mongoengine import DoesNotExist

import app.schemas.pulse as schemas_pulse
import app.models.pulse as models_pulse
import app.models.session as models_session


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


def get_session_pulse(id: str):
    pulse = []
    try:
        session_pulse_itr = models_pulse.SessionPulse.objects(session=id)
        for sess_pulse in session_pulse_itr:
            p = schemas_pulse.SessionPulse.from_orm(sess_pulse)
            p.timestamp = sess_pulse.id.generation_time
            p.student_group_name = sess_pulse.student_group.name
            pulse.append(p)
    except DoesNotExist:
        pulse = []
    return pulse


def get_session_pulse_student(id: str):
    pulse = []
    try:
        session_pulse_itr = models_pulse.SessionPulseStudent.objects(session=id)
        for sess_pulse in session_pulse_itr:
            p = schemas_pulse.SessionPulseStudent.from_orm(sess_pulse)
            p.timestamp = sess_pulse.id.generation_time
            pulse.append(p)
    except DoesNotExist:
        pulse = []
    return pulse
