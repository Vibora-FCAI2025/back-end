from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from database import database

class Document:
    def __init__(self, collection: str, data=None, required_fields=None):
        self.collection = database[collection]
        self.data = data or {}
        self.required_fields = required_fields or []

    def __validate_fields(self):
        """
        Ensures that all required fields are present in the document.
        """
        missing_fields = [field for field in self.required_fields if field not in self.data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    def __update_id(self, id: ObjectId):
        """
        Updates document id to given id.
        """
        self.data['_id'] = id

    def __insert(self):
        """
        Inserts data into the database. Updates _id field if it doesn't exist.
        """
        self.__validate_fields()  # Validate before inserting
        result = self.collection.insert_one(self.data)
        if '_id' not in self.data:
            self.__update_id(result.inserted_id)
        return result

    def __update(self):
        """
        Updates data in the database
        """
        self.__validate_fields()  # Validate before updating
        return self.collection.update_one({'_id': self.data['_id']}, {'$set': self.data})

    def save(self):
        try:
            self.__insert()
        except DuplicateKeyError:
            # Update data if document with the same key exists
            self.__update()

    def delete(self):
        if '_id' in self.data:
            self.collection.delete_one({'_id': self.data['_id']})
            self.data = {}

    @classmethod
    def find(cls, collection: str, query):
        """
        Find multiple documents based on a query
        """
        documents = database[collection].find(query)
        return [cls(collection, doc) for doc in documents]

    @classmethod
    def find_one(cls, collection: str, query):
        """
        Find a single document based on a query
        """
        document = database[collection].find_one(query)
        if document:
            return cls(collection, document)
        return None
