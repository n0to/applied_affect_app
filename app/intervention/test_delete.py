from app.config import get_settings
from app.db.database import DbMgr
from app.models.pulse import SessionIntervention
from app.models.pulse_events import PulseProcessing

settings = get_settings()
DbMgr.connect(settings.mongo_dbname,
              settings.mongo_username,
              settings.mongo_password,
              settings.mongo_host)
SessionIntervention.objects(session="5f43b06862752155f1e7da87").delete()
