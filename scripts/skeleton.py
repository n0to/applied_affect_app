import pprint
from faker import Faker
from app.config import get_settings_from_file
from app.db import database
from pathlib import Path
import app.models.school as models_school

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)

settings = None
db = None
fake = None


def setup():
    conf = str(Path(__file__).parents[1]) + "/app/dev.env"
    print(f"Reading Settings: {conf}")
    global settings, db, fake
    settings = get_settings_from_file(conf)
    pp.pprint(settings)
    print("Getting Mongoengine connection")
    database.DbMgr.connect(db=settings.mongo_dbname,
                           username=settings.mongo_username,
                           password=settings.mongo_password,
                           host=settings.mongo_host)
    fake = Faker('en_IN')


def main():
    setup()


if __name__ == '__main__':
    main()
