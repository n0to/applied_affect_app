from mongoengine import connect, disconnect
from pymongo import MongoClient


class DbMgr:

    @staticmethod
    def connect(db: str, username: str, password: str, host: str):
        connect(db=db,
                username=username,
                password=password,
                host=host)

    @staticmethod
    def disconnect():
        disconnect()


class DbMgrPymongo:
    database = None

    @staticmethod
    def get_db(uri: str, db: str):
        if DbMgrPymongo.database is None:
            DbMgrPymongo.client = MongoClient(uri)
            DbMgrPymongo.database = DbMgrPymongo.client[db]
        return DbMgrPymongo.database
