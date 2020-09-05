import os
from datetime import timedelta

from app.db import database
from app.config import get_settings_from_file
import pprint
import pickle
import app.models.pulse_events as models_pulse_events
import app.models.enums as models_enums
import app.models.session as models_session
import app.models.school as models_school
import app.models.student as models_student
import app.utils.pulse_events as utils_pulse_events

import app.schemas.pulse_events as schemas_pulse_events

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


def main():
    conf = os.path.dirname(os.path.realpath(__file__)) + "/app/dev.env"
    print(f"Reading Settings: {conf}")
    settings = get_settings_from_file(conf)
    pp.pprint(settings.dict())
    print("Getting Pymongo connection")
    db = database.DbMgrPymongo.get_db(uri=settings.mongo_conn_str,
                                      db=settings.mongo_dbname)
    print("Getting Mongoengine connection")
    database.DbMgr.connect(db=settings.mongo_dbname,
                           username=settings.mongo_username,
                           password=settings.mongo_password,
                           host=settings.mongo_host)
    # session_id = "5f4a5884ac84c57e9a43ad8f"  # Used with jijo
    # session_id = "5f43b06862752155f1e7da87"   # Used with original
    session_id = "5f43b06862752155f1e7da94"   # Used with original2

    num_del = models_pulse_events.PulseProcessing.objects(session=session_id).delete()
    pp.pprint("Num deleted {}".format(num_del))
    session = models_session.Session.objects.get(id=session_id)
    students = session.klass.members
    camera_id = str(session.room.cameras[0].id)
    camera_frame_rate = 30
    start_time = session.scheduled_start_time
    time_delta_for_frame_rate = 1
    print("Seeding for session {} and camera {}".format(session_id, camera_id))
    student_school_ids = []
    for student in students:
        student_school_ids.append(student.school_id)

    # pickle_file_path = "/home/neo/Downloads/cam_video_jijo_with_student_id_flattened_data.pkl"
    # pickle_file_path = "/home/neo/Downloads/cam_video_original_with_student_id_flattened_data.pkl"

    pickle_file_path = "/home/neo/Downloads/cam_video_original2_with_student_id_flattened_data.pkl"
    dbfile = open(pickle_file_path, 'rb')
    faces = {}
    db = pickle.load(dbfile)
    for row in db:
        if row['face_recognition_event'] is not None:
            faces[row['face_recognition_event']['face_id']] = 1
    pp.pprint(faces)
    # Assign students to faces
    ind = 0
    for k, v in faces.items():
        faces[k] = student_school_ids[ind]
        ind = ind + 1
    pp.pprint(faces)
    for row in db:
        time_delta_amount = int((row['frame_number'] / camera_frame_rate) * time_delta_for_frame_rate)
        # pp.pprint("Frame: {} Timedelta: {}".format(row['frame_number'], time_delta_amount))
        time_delta = timedelta(seconds=time_delta_amount)
        detected_at = start_time + time_delta
        for k, v in row.items():
            if '_event' in k and v is not None:
                # print("Adding date to", k)
                row[k]['detected_at'] = detected_at
            if k == 'face_recognition_event' and v is not None:
                row[k]['face_id'] = faces[row[k]['face_id']]
        obj = schemas_pulse_events.PulseProcessing(**row, frame_type="MIDDLE", image_url="http://foobar.com")
        # pp.pprint(obj.dict())
        upd = utils_pulse_events.upsert_pulse_event(session_id=session_id,
                                                    camera_id=camera_id,
                                                    event=obj)
        pp.pprint("Updated: {}".format(upd))


main()
