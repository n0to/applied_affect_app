import app.models.session as models_session
import app.models.teacher as models_teacher
import app.schemas.session as schemas_session
import app.schemas.teacher as schemas_teacher


def get_teacher_sessions(id: str):
    sessions = models_session.Session.objects(teacher=id).order_by('+scheduled_start_time').limit(3)
    out_sessions = []
    for session in sessions:
        out_sessions.append(schemas_session.Session.from_orm(session))
    return out_sessions


def get_teacher(id: str):
    teacher = models_teacher.Teacher.objects.get(id=id)
    return schemas_teacher.Teacher.from_orm(teacher)