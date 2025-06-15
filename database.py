from pymongo import MongoClient

from config import get_settings

DATABASE_URI = get_settings().db_uri
DATABASE_NAME = get_settings().db_name


class MongoDBConnection:
    def __init__(self, db_name):
        uri = DATABASE_URI
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

database = MongoDBConnection(DATABASE_NAME)
