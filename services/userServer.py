import pymongo
from databaseService import DatabaseService

class UserService:
    def __init__(self):
        self.db = DatabaseService().get() 

    def create(user):
        return self.db.get().users.insert_one(user)
