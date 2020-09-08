class TrackerWrapper:
    def __init__(self, tracker, identifier, frame=None, bbox_value=None):
        self.tracker = tracker
        self.identifier = identifier
        self.num_frames_tracked = 0
        self.object_bbox = None
        self.last_seen_bbox = None
        if frame is not None and bbox_value is not None:
            self.init_tracker(frame, bbox_value)

    def init_tracker(self, frame, bbox_value):
        self.tracker.init(frame, bbox_value)
        self.num_frames_tracked = 0
        self.object_bbox = bbox_value
        self.last_seen_bbox = bbox_value

    def update_tracker(self, frame):
        self.num_frames_tracked += 1
        update_success, updated_bbox_value = self.tracker.update(frame)
        if update_success:
            self.last_seen_bbox = updated_bbox_value
            self.object_bbox = updated_bbox_value
        else:
            self.object_bbox = None
        return update_success, updated_bbox_value
