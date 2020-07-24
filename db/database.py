from mongoengine import connect, disconnect
from pymongo import MongoClient

uri = "mongodb+srv://tip_user:tip_password@aa.jiqjp.mongodb.net/test"


class DbMgr:

    @staticmethod
    def connect():
        connect(db='tip',
                username='tip_user',
                password='tip_password',
                host='mongodb+srv://aa.jiqjp.mongodb.net')

    @staticmethod
    def disconnect():
        disconnect()


class DbMgrPymongo:
    database = None

    @staticmethod
    def initialize():
        if DbMgrPymongo.database is None:
            client = MongoClient(uri)
            DbMgrPymongo.database = client['tip']

    @staticmethod
    def get_db():
        if DbMgrPymongo.database is None:
            DbMgrPymongo.client = MongoClient(uri)
            DbMgrPymongo.database = DbMgrPymongo.client['tip']
        return DbMgrPymongo.database
