from fastapi import APIRouter

import app.utils.pulse_events as utils_pulse_events
from app.schemas.pulse_events import PulseProcessing

router = APIRouter()


@router.post("/session/{session_id}/camera/{camera_id}/pulse_event", response_model=int)
def upsert_pulse_event(session_id: str, camera_id: str, event: PulseProcessing):
    num_records_upserted = utils_pulse_events.upsert_pulse_event(session_id=session_id, camera_id=camera_id, event=event)
    return num_records_upserted
