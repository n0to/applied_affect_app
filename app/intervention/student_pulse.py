import datetime
import os
import time

import cv2.cv2 as cv2
import pandas as pd
from pandas import DataFrame
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from mongoengine import Q
from loguru import logger
# Sample usage:
# Please run this class, this will start running a scheduler which will Trigger a periodic process to
# - read the frame wise data
# - process it
# - and store the processed data back to DB
#
# This data is used to calculate the intervention when needed
# functions to interact with it otherwise:
# 1. TO Create Frame wise pulses:
# StudentPulseManager.create_pulse(session_id, frame_id, student_id, timestamp, activity, pitch, roll, yaw)
# 2. TO get intervention applicability  based on configured thresholds
# StudentPulseManager.should_intervene_session('101')
# StudentPulseManager.should_intervene_student('5f05f687ed068084942f5789', '101')
# StudentPulseManager.should_intervene_student_group('5f05f687ed068084942f5791', '101')
from app.config import get_settings
from app.db.database import DbMgr
from app.intervention.Tracker import TrackerWrapper
from app.models.pulse import SessionPulse, SessionPulseStudent, StudentIntervention, StudentGroupIntervention, \
    SessionAttendance
from app.models.pulse_events import PulseProcessing
from app.models.session import Session
from app.models.student import Student
from app.models import *
from app.models.school import Klass


class StudentPulseManager:
    INTERVENTION_PROCESS_PERIOD_SECONDS = 10
    SESSION_INTERVENTION_THRESHOLD_ENGAGEMENT = 0.6
    SESSION_INTERVENTION_THRESHOLD_ATTENTIVENESS = 0.6
    STUDENT_INTERVENTION_THRESHOLD_ENGAGEMENT = 0.5
    STUDENT_INTERVENTION_THRESHOLD_ATTENTIVENESS = 0.5
    STUDENT_GROUP_INTERVENTION_THRESHOLD_ATTENTIVENESS = 0.6
    PROCESS_PERIOD_SECONDS = 1
    INTERVENTION_DELAY = 10
    POLL_PERIOD_SECONDS = 1
    MAX_PARALLEL_RUNS = 1
    ATTENDANCE_POLL_PERIOD_SECONDS = 10
    ATTENDANCE_PROCESS_PERIOD_SECONDS = 10
    ATTENDANCE_MAX_PARALLEL_RUNS = 1
    VALID_ACTIVITIES = ['studying', 'writing', 'questioning', 'raising_hand', 'thinking']
    IOU_THRESHOLD = 0.7
    FRAMES_ALLOWED_TO_TRACK = 300

    __trackers = {}

    @staticmethod
    def pulse_as_dict(pulse):
        if pulse.session and pulse.face_detection_event:
            new_dict = {'session': pulse.session, 'frame_id': pulse.frame_number,
                        'top_left_x': pulse.face_detection_event.top_left_x,
                        'top_left_y': pulse.face_detection_event.top_left_y,
                        'bottom_right_x': pulse.face_detection_event.bottom_right_x,
                        'bottom_right_y': pulse.face_detection_event.bottom_right_y,
                        }
            if pulse.face_recognition_event:
                new_dict['student_id'] = pulse.face_recognition_event.face_id
            else:
                new_dict['student_id'] = None

            if pulse.gaze_detection_event:
                new_dict['pitch'] = pulse.gaze_detection_event.pitch
                new_dict['yaw'] = pulse.gaze_detection_event.yaw
                new_dict['roll'] = pulse.gaze_detection_event.roll
                if pulse.action_recognition_event:
                    new_dict['activity']: pulse.action_recognition_event.actions
            return new_dict
        else:
            return None

    @staticmethod
    def create_pulse(session_id, frame_id, student_id, timestamp, activity, pitch, roll, yaw):
        raw_1 = SessionPulse(session_id=session_id, student_id=student_id, timestamp=timestamp, frame_id=frame_id,
                             activity=activity)
        raw_1.pitch = pitch
        raw_1.roll = roll
        raw_1.yaw = yaw
        raw_1.save()
        return raw_1

    @staticmethod
    def get_intervention(key):
        print("Raising intervention for ", key)

    @staticmethod
    def upsert_student_level_engagement(student_id, observed_at, session_id, param):
        # print(student_id, observed_at, session_id, param)
        ssp = SessionPulseStudent.objects(
            Q(student_id=student_id) & Q(session_id=session_id) & Q(observed_at=observed_at))

        if not ssp:
            ssp_obj = SessionPulseStudent()
            ssp_obj.session_id = session_id
            ssp_obj.observed_at = observed_at
            ssp_obj.student_id = student_id
            ssp_obj.engagement = param
            ssp_obj.save()
        else:
            ssp_obj = ssp.first()
            ssp_obj.engagement = param
            ssp_obj.save()
        # print("engagement", ssp_obj.session_id, ssp_obj.observed_at, ssp_obj.student_id, ssp_obj.engagement)

    @staticmethod
    def upsert_student_level_attentiveness(student_id, observed_at, session, param):
        student = Student.objects(school_id=student_id).first()
        if student:
            # print(student_id, observed_at, session, param)
            ssp = SessionPulseStudent.objects(
                Q(student=student) & Q(session=session) & Q(datetime_sequence=observed_at))

            if not ssp:
                ssp_obj = SessionPulseStudent()
                ssp_obj.session = session
                ssp_obj.datetime_sequence = observed_at
                ssp_obj.student = student
                ssp_obj.attentiveness = param
                ssp_obj.save()
            else:
                ssp_obj = ssp.first()
                ssp_obj.attentiveness = param
                ssp_obj.save()
            # print("attentiveness", ssp_obj.session, ssp_obj.datetime_sequence, ssp_obj.student, ssp_obj.attentiveness)
        else:
            print("Unrecognised student", student_id)

    @staticmethod
    def upsert_session_level_engagement(observed_at, session_id, param):
        # print(observed_at, session_id, param)
        sp = SessionPulse.objects(Q(session_id=session_id) & Q(observed_at=observed_at))

        if not sp:
            sp_obj = SessionPulse()
            sp_obj.session_id = session_id
            sp_obj.observed_at = observed_at
            sp_obj.engagement = param
            sp_obj.save()
        else:
            sp_obj = sp.first()
            sp_obj.engagement = param
            sp_obj.save()
        # print("engagement", sp_obj.session_id, sp_obj.observed_at, sp_obj.engagement)

    @staticmethod
    def upsert_session_level_attentiveness(observed_at, session, param):
        # print(observed_at, session, param)
        sp = SessionPulse.objects(Q(session=session) & Q(datetime_sequence=observed_at))

        if not sp:
            sp_obj = SessionPulse()
            sp_obj.session = session
            sp_obj.datetime_sequence = observed_at
            sp_obj.attentiveness = param
            sp_obj.save()
        else:
            sp_obj = sp.first()
            sp_obj.attentiveness = param
            sp_obj.save()
        # print("attentiveness", sp_obj.session, sp_obj.datetime_sequence, sp_obj.attentiveness)

    @staticmethod
    def upsert_student_group_intervention(events_end_time, events_start_time, session, student_group_name,
                                          student_group_attentiveness):
        min_events_end_time = events_end_time - datetime.timedelta(seconds=StudentPulseManager.INTERVENTION_DELAY)
        sgi = StudentGroupIntervention.objects(
            Q(intervention_reason="ATTENTIVENESS") & Q(session=session) & Q(student_group_name=student_group_name) & Q(
                intervention_period_end__gte=min_events_end_time))

        if not sgi:
            sgi_obj = StudentGroupIntervention()
            sgi_obj.session = session
            sgi_obj.student_group_name = student_group_name
            sgi_obj.intervention_reason = "ATTENTIVENESS"
            sgi_obj.intervention_period_start = events_start_time
            sgi_obj.intervention_period_end = events_end_time
            sgi_obj.intervention_reason_value = student_group_attentiveness
            sgi_obj.intervention_reason_threshold = StudentPulseManager.STUDENT_GROUP_INTERVENTION_THRESHOLD_ATTENTIVENESS
            sgi_obj.datetime_sequence = events_end_time
            sgi_obj.save()
        else:
            sgi_obj = sgi.first()
            sgi_obj.intervention_reason_value = student_group_attentiveness
            sgi_obj.intervention_reason = "ATTENTIVENESS"
            sgi_obj.save()

    @staticmethod
    def upsert_student_intervention(events_end_time, events_start_time, session, student, student_attentiveness):
        min_events_end_time = events_end_time - datetime.timedelta(seconds=StudentPulseManager.INTERVENTION_DELAY)

        si_q = StudentIntervention.objects(Q(intervention_reason="ATTENTIVENESS") & Q(session=session) &
                                           Q(student=student) & Q(intervention_period_end__gte=min_events_end_time))

        if not si_q:
            si = StudentIntervention()
            si.session = session
            si.student = student
            si.intervention_reason = "ATTENTIVENESS"
            si.intervention_period_start = events_start_time
            si.intervention_period_end = events_end_time
            si.intervention_reason_value = student_attentiveness
            si.intervention_reason_threshold = StudentPulseManager.STUDENT_INTERVENTION_THRESHOLD_ATTENTIVENESS
            si.datetime_sequence = events_end_time
            si.save()
        else:
            si = si_q.first()
            si.intervention_reason_value = student_attentiveness
            si.intervention_reason = "ATTENTIVENESS"
            si.save()

    @staticmethod
    def upsert_student_group_level_engagement(observed_at, session_id, student_group_id, param):
        None
        # print(observed_at, session_id, student_group_id, param)
        # ssgp = SessionStudentGroupPulse.objects(
        #     Q(session_id=session_id) & Q(observed_at=observed_at) & Q(student_group_id=student_group_id))
        #
        # if not ssgp:
        #     ssgp_obj = SessionStudentGroupPulse()
        #     ssgp_obj.session_id = session_id
        #     ssgp_obj.student_group_id = student_group_id
        #     ssgp_obj.observed_at = observed_at
        #     ssgp_obj.engagement = param
        #     ssgp_obj.save()
        # else:
        #     ssgp_obj = ssgp.first()
        #     ssgp_obj.engagement = param
        #     ssgp_obj.save()
        # print("engagement", ssgp_obj.session_id, ssgp_obj.student_group_id, ssgp_obj.observed_at, ssgp_obj.engagement)

    @staticmethod
    def upsert_student_group_level_attentiveness(observed_at, session, student_group, param):
        # print(observed_at, session, student_group, param)
        ssgp = SessionPulse.objects(
            Q(session=session) & Q(datetime_sequence=observed_at) & Q(student_group_name=student_group.name))

        if not ssgp:
            ssgp_obj = SessionPulse()
            ssgp_obj.session = session
            ssgp_obj.student_group_name = student_group.name
            ssgp_obj.datetime_sequence = observed_at
            ssgp_obj.attentiveness = param
            ssgp_obj.save()
        else:
            ssgp_obj = ssgp.first()
            ssgp_obj.attentiveness = param
            ssgp_obj.save()
        # print("attentiveness", ssgp_obj.session, ssgp_obj.student_group_name, ssgp_obj.datetime_sequence,
        #       ssgp_obj.attentiveness)

    # @staticmethod
    # def calculate_engagement(start_time_of_events):
    #     pulses = []
    #     for pulse in SessionPulse.objects(timestamp__gte=start_time_of_events):
    #         # print('pulse for session:', pulse.session_id, pulse.student_id, pulse.pitch, pulse.yaw, pulse.roll)
    #         pulses.append(pulse)
    #     df: DataFrame = pd.DataFrame([StudentPulseManager.pulse_as_dict(x) for x in pulses])
    #     # print(df.head())
    #     StudentPulseManager.calculate_engagement_df(df)
    #
    # @staticmethod
    # def calculate_engagement_df(df):
    #     if not df.empty:
    #         unique_session_ids = df['session_id'].unique()
    #         for session_id in unique_session_ids:
    #             print("Processing Session ID ", session_id)
    #             session_df = df.loc[df['session_id'] == session_id]
    #             # print(session_df.head())
    #             unique_frame_ids = session_df['frame_id'].unique()
    #             print("unique frame IDs in the session ", unique_frame_ids)
    #
    #             # from a session's pulse pick up the relevant frames,
    #             # for each frame do an overall group by and calculate session's engagement
    #             # group by students and calculate the session_student engagement
    #             # find relevant student groups and add them to the DF
    #             # group by student groups and calculate the session_student_group engagement
    #
    #             for frame_id in unique_frame_ids:
    #
    #                 total_session_engagement_this_frame = 0
    #                 frame_df = df.loc[df['frame_id'] == frame_id]
    #                 print(frame_df.head())
    #                 for student_id in frame_df['student_id'].unique():
    #                     student_frame_df = frame_df.loc[frame_df['student_id'] == student_id].iloc[0]
    #                     if student_frame_df['activity'] in StudentPulseManager.VALID_ACTIVITIES:
    #                         StudentPulseManager.upsert_student_level_engagement(student_id,
    #                                                                             student_frame_df['timestamp'],
    #                                                                             session_id, 1)
    #                         frame_df.loc[frame_df['student_id'] == student_id, 'engagement'] = 1
    #                         total_session_engagement_this_frame = total_session_engagement_this_frame + 1
    #                     else:
    #                         StudentPulseManager.upsert_student_level_engagement(student_id,
    #                                                                             student_frame_df['timestamp'],
    #                                                                             session_id, 0)
    #                         frame_df.loc[frame_df['student_id'] == student_id, 'engagement'] = 0
    #
    #                 # updating session level engagement
    #                 total_students = frame_df['student_id'].unique().size
    #                 StudentPulseManager.upsert_session_level_engagement(frame_df.iloc[0]['timestamp'], session_id,
    #                                                                     total_session_engagement_this_frame / total_students)
    #
    #                 student_groups = StudentPulseManager.get_student_group_to_student_mapping(
    #                     frame_df['student_id'].unique())
    #
    #                 for student_group in student_groups:
    #                     student_grp_engagement = 0
    #                     students_in_frame = 0
    #                     for student in student_group.students:
    #                         if not frame_df[frame_df['student_id'] == str(student.id)].empty:
    #                             students_in_frame = students_in_frame + 1
    #                             student_grp_engagement = student_grp_engagement + \
    #                                                      frame_df[frame_df['student_id'] == str(student.id)].iloc[0][
    #                                                          'engagement']
    #
    #                     StudentPulseManager.upsert_student_group_level_engagement(frame_df.iloc[0]['timestamp'],
    #                                                                               session_id,
    #                                                                               str(student_group.id),
    #                                                                               student_grp_engagement / students_in_frame)
    @staticmethod
    def get_bbox_from_corners(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        return (
            top_left_x,
            top_left_y,
            abs(top_left_x - bottom_right_x),
            abs(top_left_y - bottom_right_y)
        )

    @staticmethod
    def bb_intersection_over_union(boxA, boxB):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)
        if iou > 0:
            print(iou)
        # return the intersection over union value
        return iou

    @staticmethod
    def get_frame_pulse_with_trackers(frame_df):

        # frame_info = frame_df

        students_present_in_frame = set([])
        tracker_keys = set(StudentPulseManager.__trackers.keys())

        bbox_dict = {}
        frame = frame_df.iloc[0]['frame_id']
        # {'session': pulse.session, 'frame_id': pulse.frame_number,
        #  'top_left_x': pulse.face_detection_event.top_left_x,
        #  'bottom_right_x': pulse.face_detection_event.bottom_right_x,
        #  'bottom_right_y': pulse.face_detection_event.bottom_right_y,
        #  }

        for index, row in frame_df.iterrows():
            if 'student_id' in frame_df.columns and row['student_id'] and row['student_id'] not in students_present_in_frame:
                processed_student_id = row['student_id']
                students_present_in_frame.add(processed_student_id)
                StudentPulseManager.__trackers[processed_student_id] = TrackerWrapper(cv2.TrackerMOSSE_create(),
                                                                                      processed_student_id,
                                                                  frame,
                                                                  StudentPulseManager.get_bbox_from_corners
                                                                  (row['top_left_x'], row['top_left_y'],
                                                                   row['bottom_right_x'],
                                                                   row['bottom_right_y']))
                print("Init/Reinit Tracker", processed_student_id)

        for lost_student in (tracker_keys - students_present_in_frame):
            tracked_success, bbox_value = StudentPulseManager.__trackers[lost_student].update_tracker(frame)
            delete_student = False
            p1 = (int(bbox_value[0]), int(bbox_value[1]))
            p2 = (int(bbox_value[0] + bbox_value[2]), int(bbox_value[1] + bbox_value[3]))
            # Frames check here
            if StudentPulseManager.__trackers[lost_student].num_frames_tracked > StudentPulseManager.FRAMES_ALLOWED_TO_TRACK:
                delete_student = True
                print("Face recog hasn't detected {} in {} frames".format(lost_student, StudentPulseManager.FRAMES_ALLOWED_TO_TRACK))
            if delete_student:
                del StudentPulseManager.__trackers[lost_student]
                continue
            # IOU Check
            lost_student_bbox = (p1[0], p1[1], p2[0], p2[1])
            for face_recog_student in students_present_in_frame:
                if not tracked_success:
                    continue
                face_recog_bbox = (
                    StudentPulseManager.__trackers[face_recog_student].object_bbox[0], StudentPulseManager.__trackers[face_recog_student].object_bbox[1],
                    StudentPulseManager.__trackers[face_recog_student].object_bbox[0] + StudentPulseManager.__trackers[face_recog_student].object_bbox[2],
                    StudentPulseManager.__trackers[face_recog_student].object_bbox[1] + StudentPulseManager.__trackers[face_recog_student].object_bbox[3])
                if StudentPulseManager.bb_intersection_over_union(lost_student_bbox, face_recog_bbox) > StudentPulseManager.IOU_THRESHOLD:
                    print(
                        "{} is clashing with {}. IOU above {}".format(lost_student, face_recog_student, StudentPulseManager.IOU_THRESHOLD))
                    delete_student = True
                    break

            if delete_student:
                del StudentPulseManager.__trackers[lost_student]
                continue

            bbox_dict[frame + str(p1[0]) + str(p1[1]) + str(p2[0]) + str(p2[1])] = StudentPulseManager.__trackers[lost_student].identifier

        for row in frame_df.iterrows():
            if 'student_id' in frame_df.columns and row['student_id'] and row['student_id'] not in students_present_in_frame:
                row['student_id'] = bbox_dict[frame+frame_df['top_left_x']+frame_df['top_left_y']+
                                                                   frame_df['bottom_right_x']+frame_df['bottom_right_y']]


    @staticmethod
    def calculate_attentiveness(start_time_of_events, end_time_of_events):
        logger.info(f"start_time_of_events:{start_time_of_events}")
        logger.info(f"end_time_of_events:{end_time_of_events}")
        pulses = []
        for pulse in PulseProcessing.objects(Q(person_detection_event__detected_at__gte=start_time_of_events) & Q(
                person_detection_event__detected_at__lt=end_time_of_events)):
            # print('pulse for session:', pulse.session_id, pulse.student_id, pulse.pitch, pulse.yaw, pulse.roll)
            pulse_dict = StudentPulseManager.pulse_as_dict(pulse)
            if pulse_dict:
                pulses.append(pulse_dict)
        df: DataFrame = pd.DataFrame(pulses)
        # print(df.head())
        StudentPulseManager.calculate_attentiveness_df(df, start_time_of_events)
        print("DONE : " + str(start_time_of_events))

    @staticmethod
    def calculate_attentiveness_df(df, start_time_of_events):
        if not df.empty:
            unique_sessions = df['session'].unique()
            for session in unique_sessions:
                student_attentiveness_dict = {}

                # print("Processing Session ID ", session)
                session_df = df.loc[df['session'] == session]
                # print(session_df.head())
                unique_frame_ids = session_df['frame_id'].unique()
                # print("unique frame IDs in the session ", unique_frame_ids)

                session_student_score = {}
                for frame_id in unique_frame_ids:
                    total_session_attentiveness_this_frame = 0
                    frame_df = df.loc[df['frame_id'] == frame_id]

                    frame_agg_df = frame_df.groupby(['frame_id'], as_index=False).agg(
                        {'yaw': {np.min, np.max, np.average},
                         'pitch': {np.min, np.max, np.average},
                         'roll': {np.min, np.max, np.average}
                         }).reset_index()

                    frame_agg_df.columns = ['_'.join(col).strip() for col in frame_agg_df.columns.values]
                    # print(frame_agg_df.head())

                    avg_frame_pitch = frame_agg_df['pitch_average'].iloc[0]
                    avg_frame_yaw = frame_agg_df['yaw_average'].iloc[0]
                    # print("Average Frame pitch is: ", avg_frame_pitch, "Average Frame yaw is: ", avg_frame_yaw)

                    # frame_df = StudentPulseManager.get_frame_pulse_with_trackers(frame_df)

                    for student_id in frame_df['student_id'].unique():

                        student_attentiveness = {}
                        if student_id in student_attentiveness_dict:
                            student_attentiveness = student_attentiveness_dict[student_id]
                        else:
                            student_attentiveness['total'] = 0
                            student_attentiveness['un_attentive'] = 0
                        student_attentiveness['total'] = student_attentiveness['total'] + 1

                        student_frame_df = frame_df.loc[frame_df['student_id'] == student_id].iloc[0]
                        if pow((student_frame_df['pitch'] - avg_frame_pitch) / 180, 2) + pow(
                                (student_frame_df['yaw'] - avg_frame_yaw) / 180, 2) > 0.03:

                            # print(
                            #     "Frame Id : " + str(frame_id) + " Student Id : " + student_id + " Student's pitch : " +
                            #     str(student_frame_df['pitch']), " Student's yaw : " + str(student_frame_df[
                            #                                                                   'yaw']) + " Frame's avg pitch : " + str(
                            #         avg_frame_pitch) + " Frame's avg yaw : " + str(avg_frame_yaw))

                            student_attentiveness['un_attentive'] = student_attentiveness['un_attentive'] + 1

                            # tic = time.perf_counter()
                            # StudentPulseManager.upsert_student_level_attentiveness(student_id,
                            #                                                        student_frame_df['timestamp'],
                            #                                                        session, 0)
                            # toc = time.perf_counter()
                            # print(f"upsert_student_level_attentiveness in {toc - tic:0.4f} seconds")

                            frame_df.loc[frame_df['student_id'] == student_id, 'attentiveness'] = 0
                        else:
                            # tic = time.perf_counter()
                            # StudentPulseManager.upsert_student_level_attentiveness(student_id,
                            #                                                        student_frame_df['timestamp'],
                            #                                                        session, 1)
                            # toc = time.perf_counter()
                            # print(f"upsert_student_level_attentiveness in {toc - tic:0.4f} seconds")
                            frame_df.loc[frame_df['student_id'] == student_id, 'attentiveness'] = 1

                            total_session_attentiveness_this_frame = total_session_attentiveness_this_frame + 1

                        student_attentiveness_dict[student_id] = student_attentiveness

                    # updating session level attentiveness
                    # total_students = frame_df['student_id'].unique().size
                    # StudentPulseManager.upsert_session_level_attentiveness(frame_df.iloc[0]['timestamp'], session,
                    #                                                        total_session_attentiveness_this_frame / total_students)

                    student_groups = session.fetch().klass.student_groups

                    # for student_group in student_groups:
                    #     student_grp_attentiveness = 0
                    #     students_in_frame = 0
                    #     for student in student_group.members:
                    #         if not frame_df[frame_df['student_id'] == str(student.school_id)].empty:
                    #             students_in_frame = students_in_frame + 1
                    #             student_grp_attentiveness = student_grp_attentiveness + \
                    #                                         frame_df[
                    #                                             frame_df['student_id'] == str(student.school_id)].iloc[
                    #                                             0][
                    #                                             'attentiveness']
                    #     if students_in_frame and students_in_frame > 0:
                    #         StudentPulseManager.upsert_student_group_level_attentiveness(frame_df.iloc[0]['timestamp'],
                    #                                                                      session,
                    #                                                                      student_group,
                    #                                                                      student_grp_attentiveness / students_in_frame)

                print(student_attentiveness_dict)
                for student_id in student_attentiveness_dict.keys():
                    student_attentiveness = (student_attentiveness_dict[student_id]['total'] -
                                             student_attentiveness_dict[student_id][
                                                 'un_attentive']) / student_attentiveness_dict[student_id]['total']
                    StudentPulseManager.upsert_student_level_attentiveness(student_id, start_time_of_events, session,
                                                                           student_attentiveness)

                student_groups = session.fetch().klass.student_groups
                for student_group in student_groups:
                    student_grp_un_attentive = 0
                    student_grp_total = 0
                    for student in student_group.members:
                        if student.school_id in student_attentiveness_dict:
                            student_grp_total += student_attentiveness_dict[student.school_id]['total']
                            student_grp_un_attentive += student_attentiveness_dict[student.school_id]['un_attentive']

                    if student_grp_total:
                        student_group_attentiveness = (student_grp_total - student_grp_un_attentive) / student_grp_total
                        StudentPulseManager.upsert_student_group_level_attentiveness(start_time_of_events, session,
                                                                                     student_group,
                                                                                     student_group_attentiveness)

    @staticmethod
    def should_intervene_session(session, events_start_time, events_end_time):

        # min_student_in_session_for_intervention = session.configs.th_min_student_for_int

        total_attentiveness_pulses = 0
        total_engagement_pulses = 0
        total_attentiveness = 0
        total_engagement = 0
        for session_pulse in SessionPulse.objects(
                Q(session=session) & Q(observed_at__gte=events_start_time) & Q(observed_at__lt=events_end_time)):

            if session_pulse.attentiveness:
                total_attentiveness += session_pulse.attentiveness
                total_attentiveness_pulses += 1

            if session_pulse.engagement:
                total_engagement += session_pulse.engagement
                total_engagement_pulses += 1

        if (total_attentiveness_pulses > 0 and (
                total_attentiveness / total_attentiveness_pulses > StudentPulseManager.SESSION_INTERVENTION_THRESHOLD_ATTENTIVENESS)) \
                or (total_engagement_pulses > 0 and (
                total_engagement / total_engagement_pulses > StudentPulseManager.SESSION_INTERVENTION_THRESHOLD_ENGAGEMENT)):
            return True
        else:
            return False

    @staticmethod
    def should_intervene_student(student_id, session_id, events_start_time, events_end_time):

        total_attentiveness_pulses = 0
        total_engagement_pulses = 0
        total_attentiveness = 0
        total_engagement = 0
        for student_pulse in SessionPulseStudent.objects(
                Q(student_id=student_id) & Q(session_id=session_id) & Q(observed_at__gte=events_start_time) & Q(
                    observed_at__lt=events_end_time)):
            if student_pulse.attentiveness:
                total_attentiveness += student_pulse.attentiveness
                total_attentiveness_pulses += 1

            # if student_pulse.engagement:
            #     total_engagement += student_pulse.engagement
            #     total_engagement_pulses += 1

        if (total_attentiveness_pulses > 0 and (
                total_attentiveness / total_attentiveness_pulses > StudentPulseManager.STUDENT_INTERVENTION_THRESHOLD_ATTENTIVENESS)) or \
                (total_engagement_pulses > 0 and (
                        total_engagement / total_engagement_pulses > StudentPulseManager.STUDENT_INTERVENTION_THRESHOLD_ENGAGEMENT)):
            return True
        else:
            return False

    @staticmethod
    def calculate_student_interventions(events_start_time, events_end_time):
        print(events_start_time)
        print(events_end_time)
        student_attentiveness_dict = {}

        for student_pulse in SessionPulseStudent.objects(
                Q(datetime_sequence__gte=events_start_time) & Q(datetime_sequence__lt=events_end_time)):
            student = student_pulse.student
            session = student_pulse.session
            student_attentiveness = {}

            if session not in student_attentiveness_dict:
                student_attentiveness_dict[session] = {}

            if student in student_attentiveness_dict[session]:
                student_attentiveness = student_attentiveness_dict[session][student]
            else:
                student_attentiveness['total'] = 0
                student_attentiveness['attentive'] = 0

            student_attentiveness['total'] = student_attentiveness['total'] + 1
            student_attentiveness['attentive'] = student_attentiveness['attentive'] + student_pulse.attentiveness

            student_attentiveness_dict[session][student] = student_attentiveness

        print(student_attentiveness_dict)

        for session in student_attentiveness_dict.keys():
            for student in student_attentiveness_dict[session].keys():
                student_attentiveness = student_attentiveness_dict[session][student]
                if student_attentiveness['attentive'] / student_attentiveness[
                    'total'] <= StudentPulseManager.STUDENT_INTERVENTION_THRESHOLD_ATTENTIVENESS:
                    StudentPulseManager.upsert_student_intervention(events_end_time, events_start_time, session,
                                                                    student,
                                                                    student_attentiveness['attentive'] /
                                                                    student_attentiveness['total'])

    @staticmethod
    def calculate_student_group_interventions(events_start_time, events_end_time):
        print(events_start_time)
        print(events_end_time)
        student_group_attentiveness_dict = {}

        for student_group_pulse in SessionPulse.objects(
                Q(datetime_sequence__gte=events_start_time) & Q(datetime_sequence__lt=events_end_time)):
            student_group = student_group_pulse.student_group_name
            session = student_group_pulse.session
            student_group_attentiveness = {}

            if session not in student_group_attentiveness_dict:
                student_group_attentiveness_dict[session] = {}

            if student_group in student_group_attentiveness_dict[session]:
                student_group_attentiveness = student_group_attentiveness_dict[session][student_group]
            else:
                student_group_attentiveness['total'] = 0
                student_group_attentiveness['attentive'] = 0

            student_group_attentiveness['total'] = student_group_attentiveness['total'] + 1
            student_group_attentiveness['attentive'] = student_group_attentiveness[
                                                           'attentive'] + student_group_pulse.attentiveness

            student_group_attentiveness_dict[session][student_group] = student_group_attentiveness

        print(student_group_attentiveness_dict)

        for session in student_group_attentiveness_dict.keys():
            for student_group in student_group_attentiveness_dict[session].keys():
                student_group_attentiveness = student_group_attentiveness_dict[session][student_group]
                if student_group_attentiveness['attentive'] / student_group_attentiveness[
                    'total'] <= StudentPulseManager.STUDENT_GROUP_INTERVENTION_THRESHOLD_ATTENTIVENESS:
                    sg_attentiveness = student_group_attentiveness['attentive'] / student_group_attentiveness['total']
                    StudentPulseManager.upsert_student_group_intervention(events_end_time, events_start_time, session,
                                                                          student_group, sg_attentiveness)

    @staticmethod
    def calculate_attendence(events_start_time, events_end_time):
        print(events_start_time)
        print(events_end_time)
        student_attendance_dict = {}

        for student_pulse in SessionPulseStudent.objects(
                Q(datetime_sequence__gte=events_start_time) & Q(datetime_sequence__lt=events_end_time)):
            student = student_pulse.student
            session = student_pulse.session

            if session not in student_attendance_dict:
                student_attendance_dict[session] = {}

            if student not in student_attendance_dict[session]:
                student_attendance_dict[session][student] = 1

        for session in student_attendance_dict.keys():
            for student in student_attendance_dict[session].keys():
                student_attendance = student_attendance_dict[session][student]
                if student_attendance:
                    StudentPulseManager.mark_student_present(session, student)

    @staticmethod
    def mark_student_present(session, student):
        attendance = SessionAttendance.objects(Q(student=student) & Q(session=session))
        if not attendance:
            ssp_obj = SessionAttendance()
            ssp_obj.session = session
            ssp_obj.student = student
            ssp_obj.is_present = True
            ssp_obj.save()


date_time_str = '2020-08-25 13:00:00'
__processing_start_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
__attendance_processing_start_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')


def process_pulse():
    global __processing_start_time
    start_time_of_events = __processing_start_time
    end_time_of_events = start_time_of_events + datetime.timedelta(
        seconds=StudentPulseManager.PROCESS_PERIOD_SECONDS)
    end_time_of_events_intervention = end_time_of_events
    start_time_of_events_intervention = end_time_of_events - datetime.timedelta(
        seconds=StudentPulseManager.INTERVENTION_PROCESS_PERIOD_SECONDS)
    __processing_start_time = end_time_of_events
    # StudentPulseManager.calculate_engagement(start_time_of_events)
    StudentPulseManager.calculate_attentiveness(start_time_of_events, end_time_of_events)
    StudentPulseManager.calculate_student_interventions(start_time_of_events_intervention,
                                                        end_time_of_events_intervention)
    StudentPulseManager.calculate_student_group_interventions(start_time_of_events_intervention,
                                                              end_time_of_events_intervention)


def process_attendance_pulse():
    global __attendance_processing_start_time
    start_time_of_events = __attendance_processing_start_time
    end_time_of_events = start_time_of_events + datetime.timedelta(
        seconds=StudentPulseManager.ATTENDANCE_PROCESS_PERIOD_SECONDS)
    __attendance_processing_start_time = end_time_of_events
    StudentPulseManager.calculate_attendence(start_time_of_events, end_time_of_events)


def start_svc():
    settings = get_settings()
    DbMgr.connect(settings.mongo_dbname,
                  settings.mongo_username,
                  settings.mongo_password,
                  settings.mongo_host)


if __name__ == '__main__':
    start_svc()
    scheduler = BackgroundScheduler()

    scheduler.add_job(process_pulse, 'interval', seconds=StudentPulseManager.POLL_PERIOD_SECONDS,
                      max_instances=StudentPulseManager.MAX_PARALLEL_RUNS)
    # scheduler.add_job(process_attendance_pulse, 'interval', seconds=StudentPulseManager.ATTENDANCE_POLL_PERIOD_SECONDS,
    #                   max_instances=StudentPulseManager.ATTENDANCE_MAX_PARALLEL_RUNS)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
