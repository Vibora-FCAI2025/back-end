from pymongo import MongoClient

from config import get_settings


class MongoDBConnection:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]


settings = get_settings()
database = MongoDBConnection(settings.db_uri, settings.db_name)
