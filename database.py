from pymongo import MongoClient

DATABASE_URI = env("DB_URI")
DATABASE_NAME = env("DB_NAME")


class MongoDBConnection:
    def __init__(self, db_name):
        uri = DATABASE_URI
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

database = MongoDBConnection(DATABASE_NAME)
