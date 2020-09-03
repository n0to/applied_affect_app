from bson import ObjectId
from loguru import logger

import app.models.pulse_events as models_pulse_events
import app.schemas.pulse_events as schemas_pulse_events


def upsert_pulse_event(session_id: str, camera_id: str, event: schemas_pulse_events.PulseProcessing):
    logger.bind(payload=event.dict()).debug("Pulse processing with session {} and camera {}".format(session_id, camera_id))
    event = models_pulse_events.PulseProcessing.objects(person_id=event.person_id,
                                                        session=session_id,
                                                        camera=camera_id). update_one(
        **event.dict(),
        upsert=True)
    logger.debug("Num records updated {}".format(event))
    return event
