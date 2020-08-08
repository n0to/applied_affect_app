from mongoengine import DoesNotExist

import app.schemas.pulse as schemas_pulse
import app.models.pulse as models_pulse
import app.models.session as models_session


def get_session_attendance_aggregated(id: str):
    try:
        student_groups = models_session.Session.objects.get(id=id).klass.student_groups
        total = None
        for sg in student_groups:
            if sg.name == "all":
                total = len(sg.members)
                break
        present = models_pulse.SessionAttendance.objects(session=id, is_present=True).count()
        return schemas_pulse.SessionAttendanceAggregated(total=total, present=present)
    except DoesNotExist:
        return None


def get_session_pulse(id: str):
    pass


def get_session_pulse_student(id: str):
    pass
